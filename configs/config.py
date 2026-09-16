import os 
from dotenv import load_dotenv
load_dotenv()


MODEL_PROVIDER = os.getenv("MODEL_PROVIDER" , "huggingface")

MODEL_API_KEY = os.getenv("HUGGING_FACE" , "")