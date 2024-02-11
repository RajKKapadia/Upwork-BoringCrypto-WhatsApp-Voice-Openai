from twilio.rest import Client

import config

account_sid = config.TWILIO_SID
auth_token = config.TWILIO_TOKEN
client = Client(account_sid, auth_token)


def send_message(to: str, message: str) -> None:
    '''
    Send message to a Telegram user.
    Parameters:
        - to(str): sender whatsapp number in this whatsapp:+919558515995 form
        - message(str): text message to send
    Returns:
        - None
    '''

    response = client.messages.create(
        from_=config.FROM,
        body=message,
        to=to
    )
    print(response.sid)


def send_media_message(to: str, media_url: str) -> None:
    '''
    Send message to a Telegram user.
    Parameters:
        - to(str): sender whatsapp number in this whatsapp:+919558515995 form
        - media_url(str): media URL to send
    Returns:
        - None
    '''

    response = client.messages.create(
        from_=config.FROM,
        media_url=[media_url],
        to=to
    )
    print(response.sid)

print(send_media_message('whatsapp:+919558515995', 'https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'))