from prompt_template import PromptTemplate as CustomPromptTemplate
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = st.secrets["gemini_api_key"]

llm = GoogleGenAI(
    model="gemini-2.5-flash",  # Fixed: gemini-2.5-flash is not a valid model name
    api_key=gemini_api_key,
)

temp_prompt = CustomPromptTemplate().MAIN_PROMPT
chat_prompt_template = PromptTemplate(temp_prompt)


def format_chat_history(chat_history: list) -> str:
    """Format chat history list into a clean readable string for the prompt."""
    if not chat_history:
        return "No previous conversation."
    formatted = []
    for msg in chat_history:
        role = msg.get("role", "unknown").capitalize()
        content = msg.get("content", "")
        formatted.append(f"{role}: {content}")
    return "\n".join(formatted)


def generate_respone(query: str, chat_history: list) -> str:
    """Function to generate the response using LLM."""
    try:
        formatted_history = format_chat_history(chat_history)
        resp = llm.predict(
            chat_prompt_template,
            query=query,
            chat_history=formatted_history  # Now a clean string, not a raw list
        )
        return resp
    except Exception as e:
        error_msg = str(e).lower()
        if "500" in error_msg or "server" in error_msg:
            return "Sorry, the AI service is temporarily unavailable. Please try again in a moment."
        elif "400" in error_msg or "client" in error_msg:
            return "There was an issue processing your request. Please try rephrasing your question."
        else:
            return f"An unexpected error occurred. Please try again."
