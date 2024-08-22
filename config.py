import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_PATH = os.getenv('DB_PATH')

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided. Please set the BOT_TOKEN environment variable.")

if not DB_PATH:
    raise ValueError("No DB_PATH provided. Please set the DB_PATH environment variable.")




