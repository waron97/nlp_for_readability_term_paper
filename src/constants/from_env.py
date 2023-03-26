import os
from dotenv import load_dotenv


load_dotenv()

OPEANAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
