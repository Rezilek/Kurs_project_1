import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent


class Config:
    API_KEY = os.getenv("API_KEY")
    STOCK_API_KEY = os.getenv("STOCK_API_KEY")
    CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
    DATA_FILE_PATH = str(BASE_DIR / "data" / "operations.xlsx")
    USER_SETTINGS_PATH = str(BASE_DIR / "user_settings.json")
