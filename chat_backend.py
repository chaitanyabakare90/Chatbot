from prompt_template import PromptTemplate as CustomPromptTemplate
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.llms import ChatMessage, MessageRole
import streamlit as st
from dotenv import load_dotenv
import os
import time

# =========================
# ✅ LOAD ENV
# =========================
load_dotenv()

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
    model="gemini-2.5-flash",
    api_key=gemini_api_key,
)

# =========================
# ✅ PROMPT
# =========================
temp_prompt = CustomPromptTemplate().MAIN_PROMPT

# =========================
# ✅ MAIN FUNCTION (FIXED)
# =========================
def generate_response(query: str, chat_history: list) -> str:
    """Generate response using LLM safely."""

    if not query or not query.strip():
        return "Please enter a valid question."

    # ✅ Format chat history as readable string for the prompt
    formatted_history = ""
    for chat in chat_history[-5:]:
        formatted_history += f"User: {chat.get('user', '')}\nAssistant: {chat.get('assistant', '')}\n"

    # ✅ Fill in the placeholders in the prompt template
    filled_system_prompt = temp_prompt.format(
        query=query,
        chat_history=formatted_history if formatted_history else "No previous conversation."
    )

    # ✅ Build messages list with the filled prompt
    messages = [
        ChatMessage(role=MessageRole.SYSTEM, content=filled_system_prompt),
        ChatMessage(role=MessageRole.USER, content=query),
    ]

    # 🔹 Retry logic
    for attempt in range(3):
        try:
            response = llm.chat(messages)
            return response.message.content
        except Exception as e:
            print(f"[ERROR] Attempt {attempt + 1}: {e}")
            time.sleep(2)

    return "AI service is temporarily unavailable. Please try again."

# =========================
# ✅ TEST
# =========================
if __name__ == "__main__":
    chat_history = []
    query = "What is a credit score?"
    response = generate_response(query, chat_history)
    print(response)
