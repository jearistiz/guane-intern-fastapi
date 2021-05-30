import os
from pathlib import Path

from dotenv import load_dotenv


dotenv_path = Path(__file__).resolve().parent / '..' / '.env'

load_dotenv(dotenv_path)

sttgs = os.environ
