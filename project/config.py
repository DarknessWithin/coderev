import os
from dotenv import load_dotenv

load_dotenv()

BITBUCKET_EMAIL = os.getenv("BITBUCKET_EMAIL")
BITBUCKET_API_TOKEN = os.getenv("BITBUCKET_API_TOKEN").strip()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")