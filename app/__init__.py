from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import text
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os

# print(os.getcwd())
# sys.path.append(os.path.abspath(os.getcwd()))
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

with app.app_context():
    engine = sqlalchemy.create_engine(Config().SQLALCHEMY_DATABASE_URI)  # connect to server

    with engine.connect() as conn:
        create_str = text("CREATE DATABASE IF NOT EXISTS %s ;" % ('flaskDB'))
        conn.execute((create_str))
        conn.execute(text("USE flaskDB;"))
    db = SQLAlchemy(app)
    db.create_all()
    db.session.commit()

migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes,models,errors,torch_utils,mnist_fcn

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
            mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'],app.config['MAIL_PORT']),fromaddr='no-reply@'+app.config['MAIL_SERVER'],toaddrs=app.config['ADMINS'],subject='Microblog failure',credentials=auth,secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    # Logging to a file 
    if not os.path.exists('logs'): # Create a log directory if not present
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log',maxBytes=10240,backupCount=10) # Ensures log files do not grow too large
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s : %(message)s [in %(pathname)s : %(lineno)d]')) # Format of log msgs
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog Startup')
