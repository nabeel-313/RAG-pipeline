import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class Utilities:
    
    @staticmethod
    def get_api_key(api_key_name):
        return os.getenv(api_key_name)