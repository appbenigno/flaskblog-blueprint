import os
import json

with open(file='/etc/config-flask.json', mode='r') as config_file:
    config = json.load(fp=config_file)

class Config:
    SECRET_KEY = config['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = config['SQLALCHEMY_DATABASE_URI']
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config['EMAIL_USER']
    MAIL_PASSWORD = config['EMAIL_PASS']
    API_KEY = config['API_KEY']
