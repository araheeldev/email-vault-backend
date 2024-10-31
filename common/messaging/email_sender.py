import os
from flaskapp.services.messaging_adapter import RabbitMqMessageAdapter  


email_provider = os.getenv('EMAIL_PROVIDER', 'mailjet').lower()
if email_provider == "mailjet":
    EMAIL_TRANSMITTER_QUEUE_NAME = os.getenv('QUEUE_NAME_PREFIX', 'default_prefix_') + os.getenv('EmailServiceProcessor_QUEUE_NAME', 'default_queue')
    message_adapter = RabbitMqMessageAdapter()

    def send_verification_email(user, confirmation_link):
        message = {
            "event": "USER_CREATED",
            "data": {
                "confirmation_link": confirmation_link,
                "recipient_name": user.email,
            },
            "to_emails": [user.email]
        }
        message_adapter.send_message(EMAIL_TRANSMITTER_QUEUE_NAME, message)

    def send_recovery_email(user, recovery_link):
        message = {
            "event": "PASSWORD_RECOVERY",
            "data": {
                "recovery_link": recovery_link,
                "recipient_name": user.email,
            },
            "to_emails": [user.email]
        }
        message_adapter.send_message(EMAIL_TRANSMITTER_QUEUE_NAME, message)
else:
    raise ValueError("Unsupported email provider specified.")
