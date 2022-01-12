from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
VENV_PATH = os.getenv('VENV_PATH')

DOWNLOADS_DIR = 'downloads'
VIDEOS_DIR = os.path.join(DOWNLOADS_DIR, 'videos')
CAPTIONS_DIR = os.path.join(DOWNLOADS_DIR, 'captions')
OUTPUTS_DIR = 'outputs'
