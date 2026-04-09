import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Securely fetch the API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"
MAX_ITERATIONS = 6