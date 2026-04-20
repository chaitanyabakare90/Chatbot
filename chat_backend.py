from prompt_template import PromptTemplate as CustomPromptTemplate
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv
import time

load_dotenv()

gemini_api_key = st.secrets["gemini_api_key"]

llm = GoogleGenAI(
    model="gemini-2.5-flash",   
    api_key=gemini_api_key,
)


temp_prompt = CustomPromptTemplate().MAIN_PROMPT
chat_prompt_template = PromptTemplate(temp_prompt)

def generate_respone(query: str, chat_history: list) -> str:
    """Generate response using LLM safely."""

    if not query or not query.strip():
        return "Please enter a valid question."

    
    chat_history = chat_history[-5:] if chat_history else []

    
    for attempt in range(3):
        try:
            response = llm.predict(
                chat_prompt_template,
                query=query,
                chat_history=chat_history
            )
            return response

        except Exception as e:
            print(f"[ERROR] Attempt {attempt + 1}: {e}")
            time.sleep(2)

    return "AI service is temporarily unavailable. Please try again."

if __name__ == "__main__":
    chat_history = []
    response = generate_respone(
        "What is Rohit Sharma's birth date?",
        chat_history
    )
    print(response)
