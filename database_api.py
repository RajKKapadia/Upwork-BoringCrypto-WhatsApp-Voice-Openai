import os
from datetime import datetime
from typing import Any
import uuid

from pymongo import MongoClient
import gridfs
import requests

import config

client = MongoClient(config.CONNECTION_STRING)
db = client[config.DATABASE_NAME]
user_collection = db[config.COLLECTION_NAME]
fs = gridfs.GridFS(db)


def update_messages(sender_id: int, query: str, response: str, message_count: int, query_audio_file_name: str = '', response_audio_file_name: str = '') -> bool:
    '''Update messages for the user and reduce the messages_count by one

    Parameters:
        - sender_id(int): user telegram id
        - response(str): response of the bot
        - query(str): query of the user

    Returns:
        - bool, 0 for failure and 1 for success
    '''
    message = {
        'query': query,
        'response': response,
        'query_audio_file_name': query_audio_file_name,
        'response_audio_file_name': response_audio_file_name,
        'createdAt': datetime.now().strftime('%d/%m/%Y, %H:%M')
    }
    result = user_collection.find_one_and_update(
        {
            'senderId': sender_id
        },
        {
            '$push': {
                'messages': message
            },
            '$set': {
                'messageCount': message_count + 1
            }
        }
    )

    if not result:
        return False
    else:
        return True


def create_user(user: dict) -> bool:
    '''Process the whole body and update the db

    Parameters:
        - data(dict): the incoming request from Telegram

    Returns:
        - bool, 0 for failure and 1 for success
    '''
    result = user_collection.insert_one(user)

    return result.acknowledged


def get_user(sender_id: str) -> Any:
    '''Get user

    Parameters:
        - sender_id(str): sender id of the user

    Returns:
        - bool, 0 for failure and 1 for success
    '''
    result = user_collection.find_one(
        {
            'senderId': sender_id
        }
    )

    if not result:
        None
    return result


def save_audio(audio_file_path: str) -> str:
    file_name = audio_file_path.split('/')[-1]
    with open(audio_file_path, 'rb') as f:
        contents = f.read()
    fs.put(contents, filename=file_name)
    os.unlink(audio_file_path)

    return file_name


def get_audio_local_file_path(file_name: str) -> str:
    for grid_out in fs.find({'filename': file_name}):
        data = grid_out.read()
    local_file_path = f'{config.OUTPUT_DIR}/{file_name}'
    with open(local_file_path, 'wb') as file:
        file.write(data)

    return local_file_path


def save_audio_from_url(audio_url: str) -> str:
    ogg_file_path = f'{config.OUTPUT_DIR}/{uuid.uuid1()}.ogg'
    data = requests.get(audio_url)
    with open(ogg_file_path, 'wb') as file:
        file.write(data.content)
    file_name = ogg_file_path.split('/')[-1]
    with open(ogg_file_path, 'rb') as f:
        contents = f.read()
    fs.put(contents, filename=file_name)
    os.unlink(ogg_file_path)

    return file_name