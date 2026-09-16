import os

from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("API KEY LOADED:", bool(OPENAI_API_KEY))