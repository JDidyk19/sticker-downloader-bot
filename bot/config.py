import os
from dotenv import load_dotenv


if os.path.exists(os.path.join(os.getcwd(), '.env')):
    load_dotenv()

# Telegram token
TOKEN = os.getenv('TOKEN')