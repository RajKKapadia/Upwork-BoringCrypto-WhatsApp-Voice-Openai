import os
import tempfile

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GPT_MODEL = os.getenv('GPT_MODEL')

TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_SID = os.getenv('TWILIO_SID')
FROM = os.getenv('FROM')

REPLY_TYPE = os.getenv('REPLY_TYPE')

CONNECTION_STRING = os.getenv('CONNECTION_STRING')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
ELEVENLABS_VOICE_NAME = os.getenv('ELEVENLABS_VOICE_NAME')

BASE_URL = os.getenv('BASE_URL')

ERROR_MESSAGE = 'We are facing an issue, please try after sometimes.'

OUTPUT_DIR = os.path.join(
    tempfile.gettempdir(),
    'boringcrypto',
    'audio'
)

os.makedirs(OUTPUT_DIR, exist_ok=True)
