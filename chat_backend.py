from prompt_template import PromptTemplate as CustomPromptTemplate
# from llama_index.llms import Gemini
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()
gemini_api_key= os.getenv('gemini_api_key')
print(gemini_api_key)
llm = GoogleGenAI(
    model="gemini-2.5-flash",
    api_key=gemini_api_key,
)
temp_prompt= CustomPromptTemplate().MAIN_PROMPT
chat_prompt_template= PromptTemplate(temp_prompt)
def generate_respone(query:str, chat_history:list)-> str:
    "Function to generate the response using LLM."
    resp = llm.predict(chat_prompt_template, query= query, chat_history= chat_history)
    return resp

if __name__=="__main__":
    response= generate_respone("What is Rohit Sharma's birth date?")
    print(response)