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

    _ = client.messages.create(
        from_=config.FROM,
        body=message,
        to=to
    )


def send_media_message(to: str, media_url: str) -> None:
    '''
    Send message to a Telegram user.
    Parameters:
        - to(str): sender whatsapp number in this whatsapp:+919558515995 form
        - media_url(str): media URL to send
    Returns:
        - None
    '''

    _ = client.messages.create(
        from_=config.FROM,
        media_url=[media_url],
        to=to
    )
