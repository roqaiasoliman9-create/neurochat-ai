import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

if not API_KEY:
    raise ValueError("Missing API_KEY in .env file")

if not API_URL:
    raise ValueError("Missing API_URL in .env file")

if not MODEL_NAME:
    raise ValueError("Missing MODEL_NAME in .env file")