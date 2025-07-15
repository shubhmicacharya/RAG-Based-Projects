import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp_message(message_body):
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

    from_whatsapp = os.getenv("TWILIO_WHATSAPP_NUMBER")
    to_whatsapp = os.getenv("TO_WHATSAPP_NUMBER")

    message = client.messages.create(
        body=message_body,
        from_=from_whatsapp,
        to=to_whatsapp
    )

    print(f"✅ WhatsApp message sent. SID: {message.sid}")
