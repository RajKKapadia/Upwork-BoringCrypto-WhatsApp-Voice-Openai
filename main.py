from datetime import datetime

from flask import Flask, request

from database_api import create_user, update_messages, get_user
from utils import generate_messages, upload_file_to_gcs
from openai_api import chat_completion, transcript_audio, text_to_speech
from twilio_api import send_message, send_media_message
import config

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():

    return 'OK', 200


@app.route('/twilio', methods=['POST'])
def twilio():
    try:
        print('A new twilio request...')
        data = request.form.to_dict()
        sender_id = data['From']
        user_name = data['ProfileName']

        user = get_user(sender_id)

        query_audio_url = ''
        response_audio_url = ''

        if 'MediaUrl0' in data.keys():
            print(data['MediaUrl0'])
            transcript = transcript_audio(data['MediaUrl0'])
            if transcript['status'] == 1:
                query = transcript['transcript'].strip()
                query_audio_url += data['MediaUrl0']
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
            ogg_file_path, file_name = text_to_speech(response)
            print(ogg_file_path)
            media_url = upload_file_to_gcs(ogg_file_path, file_name)
            response_audio_url += media_url
            print(media_url)
            send_media_message(sender_id, media_url)

        if user:
            update_messages(sender_id, query, response,
                            user['messageCount'], query_audio_url, response_audio_url)
        else:
            # if not create
            message = {
                'query': query,
                'response': response,
                'createdAt': datetime.now().strftime('%d/%m/%Y, %H:%M'),
                'query_audio_file_name': query_audio_url,
                'response_audio_file_name': response_audio_url
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
    finally:
        return 'OK', 200
