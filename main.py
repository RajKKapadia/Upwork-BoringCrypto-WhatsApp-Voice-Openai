from datetime import datetime

from flask import Flask, request, send_file

from database_api import create_user, save_audio_from_url, update_messages, get_user, save_audio, get_audio_local_file_path
from utils import generate_messages, generate_audio_and_get_file_path
from openai_api import chat_completion, transcript_audio
from twilio_api import send_message, send_media_message
import config

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():

    return 'OK', 200


@app.route('/get/audio/<file_name>', methods=['GET'])
def get_audio(file_name: str):
    local_file_path = get_audio_local_file_path(file_name)

    return send_file(local_file_path, mimetype='audio/ogg')


@app.route('/twilio', methods=['POST'])
def twilio():
    try:
        print('A new twilio request...')
        data = request.form.to_dict()
        sender_id = data['From']
        user_name = data['ProfileName']

        user = get_user(sender_id)

        query_audio_file_name = ''
        response_audio_file_name = ''

        if 'MediaUrl0' in data.keys():
            transcript = transcript_audio(data['MediaUrl0'])
            if transcript['status'] == 1:
                query = transcript['transcript'].strip()
                query_audio_file_name += save_audio_from_url(data['MediaUrl0'])
            else:
                response = 'Format a message in a polite tone that we are facing an issue at this moment.'
        else:
            query = data['Body']

        # create chat_history from the previous conversations
        if user:
            messages = generate_messages(user['messages'][-3:], query)
        else:
            messages = generate_messages([], query)

        print(query)
        print(sender_id)
        print(messages)

        response = chat_completion(messages)

        print(response)

        if config.REPLY_TYPE == 'TEXT':
            send_message(sender_id, response)
        else:
            '''TODO
            [ ] generate audio from the response
            [ ] save the audio on mongodb
            [ ] send the media url 
            '''
            ogg_file_path = generate_audio_and_get_file_path(response)
            file_name = save_audio(ogg_file_path)
            response_audio_file_name += file_name
            media_url = f'{config.BASE_URL}/get/audio/{file_name}'
            send_media_message(sender_id, media_url)

        if user:
            update_messages(sender_id, query, response,
                            user['messageCount'], query_audio_file_name, response_audio_file_name)
        else:
            # if not create
            message = {
                'query': query,
                'response': response,
                'createdAt': datetime.now().strftime('%d/%m/%Y, %H:%M'),
                'query_audio_file_name': query_audio_file_name,
                'response_audio_file_name': response_audio_file_name
            }
            user = {
                'userName': user_name,
                'senderId': sender_id,
                'messages': [message],
                'messageCount': 1,
                'mobile': sender_id.split(':')[-1],
                'channel': 'WhatsApp',
                'is_paid': False,
                'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M')
            }
            create_user(user)

        print('Request success.')
    except:
        print('Request failed.')
        pass

    return 'OK', 200
