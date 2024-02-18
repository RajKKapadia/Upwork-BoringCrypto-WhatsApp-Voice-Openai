import os
import uuid

import openai
import requests
from requests.auth import HTTPBasicAuth
import soundfile as sf

import config

openai.api_key = config.OPENAI_API_KEY


def chat_completion(messages: list[dict]) -> str:
    try:
        completion = openai.chat.completions.create(
            model=config.GPT_MODEL,
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        print('Error at chat_completion...')
        print(e)
        return config.ERROR_MESSAGE


def transcript_audio(media_url: str) -> dict[str, str]:
    try:
        ogg_file_path = f'{config.OUTPUT_DIR}/{uuid.uuid1()}.ogg'
        auth = HTTPBasicAuth(config.TWILIO_SID, config.TWILIO_TOKEN)
        data = requests.get(url=media_url, auth=auth)
        print(data)
        with open(ogg_file_path, 'wb') as file:
            file.write(data.content)
        audio_data, sample_rate = sf.read(ogg_file_path)
        print(audio_data)
        mp3_file_path = f'{config.OUTPUT_DIR}/{uuid.uuid1()}.mp3'
        print(mp3_file_path)
        sf.write(mp3_file_path, audio_data, sample_rate)
        audio_file = open(mp3_file_path, 'rb')
        os.unlink(ogg_file_path)
        os.unlink(mp3_file_path)
        transcript = openai.audio.transcriptions.create(
            model='whisper-1', file=audio_file, response_format='text')
        print(transcript)
        return {
            'status': 1,
            'transcript': transcript
        }
    except Exception as e:
        print('Error at transcript_audio...')
        print(e)
        return {
            'status': 0,
            'transcript': config.ERROR_MESSAGE
        }


def text_to_speech(text: str) -> str:
    file_name = f'{uuid.uuid1()}.{config.AUDIO_FILE_FORMAT}'
    ogg_file_path = f'{config.OUTPUT_DIR}/{file_name}'
    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
        response_format='opus'
    )
    response.write_to_file(ogg_file_path)
    return ogg_file_path, file_name
