import uuid

from elevenlabs import generate, save

import config


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


def generate_audio_and_get_file_path(text: str) -> str:
    audio = generate(
        text=text,
        voice=config.ELEVENLABS_VOICE_NAME,
        model='eleven_multilingual_v2',
        api_key=config.ELEVENLABS_API_KEY
    )
    ogg_file_path = f'{config.OUTPUT_DIR}/{uuid.uuid1()}.ogg'
    save(audio, ogg_file_path)
    
    return ogg_file_path
