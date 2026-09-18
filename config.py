import os
from dotenv import load_dotenv

load_dotenv()

environment = os.environ.get("APP_ENV", "dev")

def get_db_url():
    if environment == "dev":
        return "sqlite:///app/database.db"
    elif environment == "test":
        return "sqlite:///test.db"

    return ""
