import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from langchain_google_genai import ChatGoogleGenerativeAI
from ChatPDF.constants import Config

class Utilities:
    
    @staticmethod
    def get_api_key(api_key_name):
        return os.getenv(api_key_name)
    @staticmethod
    def load_LLM():
        llm = ChatGoogleGenerativeAI(
                model=Config.LLM_MODEL,
                temperature=Config.TEMP,
                google_api_key=Utilities.get_api_key("GOOGLE_API_KEY")
        )
        return llm
            