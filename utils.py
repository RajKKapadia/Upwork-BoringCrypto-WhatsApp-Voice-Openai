from google.cloud import storage
import os

import config


if os.path.exists(config.CREDENTIALS_FILE_PATH):
    with open(config.CREDENTIALS_FILE_PATH, "r") as f:
        credentials_json = f.read()
else:
    with open(config.CREDENTIALS_FILE_PATH, "w") as f:
        f.write(config.CREDENTIALS)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.CREDENTIALS_FILE_PATH

storage_client = storage.Client()


def generate_messages(messages: list, query: str) -> list:
    formated_messages = [
        {
            'role': 'system',
            'content': 'You are a helpful assistant.'
        }
    ]
    for m in messages:
        formated_messages.append({
            'role': 'user',
            'content': m['query']
        })
        formated_messages.append({
            'role': 'system',
            'content': m['response']
        })
    formated_messages.append(
        {
            'role': 'user',
            'content': query
        }
    )

    return formated_messages


def upload_file_to_gcs(local_file_path, destination_blob_name):
    try:
        bucket = storage_client.bucket(config.GCP_CLOUD_STORAGE_BUCKET_NAME)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_file_path, predefined_acl='publicRead')
        public_url = f"https://storage.googleapis.com/{config.GCP_CLOUD_STORAGE_BUCKET_NAME}/{destination_blob_name}"
        os.unlink(local_file_path)
        return public_url
    except Exception as e:
        print(e)
