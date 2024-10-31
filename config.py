
import os
from dotenv import load_dotenv


load_dotenv('local.env')
load_dotenv('.env.secrets')

class Config:

    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  

    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
    RABBITMQ_VIRTUAL_HOST = os.getenv('RABBITMQ_VIRTUAL_HOST')
    
    # Other configurations
    MAILJET_API_KEY = os.getenv('MAILJET_API_KEY')
    MAILJET_API_SECRET = os.getenv('MAILJET_API_SECRET')
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    QUEUE_NAME_PREFIX = os.getenv('QUEUE_NAME_PREFIX', 'emailvault_')
    EmailServiceProcessor_QUEUE_NAME = os.getenv('EmailServiceProcessor_QUEUE_NAME', 'email_transmitter_queue')
