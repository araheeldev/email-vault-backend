
import builtins
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
builtins.SQLAlchemy = SQLAlchemy
