from prompt_template import PromptTemplate as CustomPromptTemplate
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv
import os
import time

# =========================
# ✅ LOAD ENV
# =========================
load_dotenv()

# 👉 Works for both Streamlit Cloud + local
try:
    gemini_api_key = st.secrets["gemini_api_key"]
except:
    gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("API key not found. Set GEMINI_API_KEY in .env or Streamlit secrets.")

# =========================
# ✅ LLM SETUP
# =========================
llm = GoogleGenAI(
    model="gemini-1.5-flash",   # ✅ changed (stable)
    api_key=gemini_api_key,
)

# =========================
# ✅ PROMPT
# =========================
temp_prompt = CustomPromptTemplate().MAIN_PROMPT
chat_prompt_template = PromptTemplate(temp_prompt)

# =========================
# ✅ MAIN FUNCTION (FIXED)
# =========================
def generate_respone(query: str, chat_history: list) -> str:
    """Generate response using LLM safely."""

    # 🔹 Empty input
    if not query or not query.strip():
        return "Please enter a valid question."

    # 🔹 Prepare messages
    messages = []

    # ✅ System prompt (VERY IMPORTANT)
    messages.append(ChatMessage(role=MessageRole.SYSTEM, content=temp_prompt))

    # 🔹 Add last 5 chat history
    for chat in chat_history[-5:]:
        messages.append(ChatMessage(role=MessageRole.USER, content=chat.get("user", "")))
        messages.append(ChatMessage(role=MessageRole.ASSISTANT, content=chat.get("assistant", "")))

    # 🔹 Add current query
    messages.append(ChatMessage(role=MessageRole.USER, content=query))

    # 🔹 Retry logic
    for attempt in range(3):
        try:
            response = llm.chat(messages)
            return response.message.content

        except Exception as e:
            print(f"[ERROR] Attempt {attempt + 1}: {e}")
            time.sleep(2)

    # 🔹 Fallback
    return "AI service is temporarily unavailable. Please try again."


# =========================
# ✅ TEST
# =========================
if __name__ == "__main__":
    chat_history = []

    # ✅ Use finance-related query
    query = "What is a credit score?"

    response = generate_respone(query, chat_history)
    print(response)
