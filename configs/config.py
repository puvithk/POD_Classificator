import os 
from dotenv import load_dotenv
load_dotenv()
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER" , "openrouter")

