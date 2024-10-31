from flask import Flask
from flask_cors import CORS
from config import Config
from rococo.data import MySqlAdapter
from common.repositories.user_repository import UserRepository
from flask_jwt_extended import JWTManager
from flaskapp.services.messaging_adapter import RabbitMqMessageAdapter
from flask_migrate import Migrate
from extensions import db 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=["http://localhost:5173"])
    jwt = JWTManager(app)

   
    db_adapter = MySqlAdapter(
        host=Config.MYSQL_HOST,
        port=int(Config.MYSQL_PORT), 
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )


    message_adapter = RabbitMqMessageAdapter()


    app.db_adapter = db_adapter
    app.user_repository = UserRepository(db_adapter, message_adapter)

 
    from flaskapp.routes import register_routes
    register_routes(app)

   
    db.init_app(app)
    migrate = Migrate(app, db)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
