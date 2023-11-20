from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # API-KEY
    GUARDIAN_API_KEY = os.getenv('GUARDIAN_API_KEY')

app_config = Config()