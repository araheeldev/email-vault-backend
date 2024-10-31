from rococo.messaging import RabbitMqConnection
import os
from config import Config  

class RabbitMqMessageAdapter:
    def __init__(self):
        self.host = Config.RABBITMQ_HOST
        self.port = Config.RABBITMQ_PORT
        self.user = Config.RABBITMQ_USER
        self.password = Config.RABBITMQ_PASSWORD
        self.virtual_host = Config.RABBITMQ_VIRTUAL_HOST

    def send_message(self, queue_name, message):
        with RabbitMqConnection(
            self.host,
            self.port,
            self.user,
            self.password,
            self.virtual_host
        ) as conn:
            conn.send_message(queue_name, message)
