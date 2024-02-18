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

CREDENTIALS = os.getenv('CREDENTIALS')
GCP_CLOUD_STORAGE_BUCKET_NAME = os.getenv('GCP_CLOUD_STORAGE_BUCKET_NAME')

ERROR_MESSAGE = 'We are facing an issue, please try after sometimes.'
AUDIO_FILE_FORMAT = 'opus'

OUTPUT_DIR = os.path.join(
    tempfile.gettempdir(),
    'boringcrypto'
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

CREDENTIALS_FILE_PATH = os.path.join(
    OUTPUT_DIR,
    'credentials.json'
)
