from secrets import token_hex
import os

FILE_NAME = 'flaskblog/.env'

SECRET_KEY = token_hex(nbytes=12)
SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
API_KEY = ''

with open(file=FILE_NAME, mode='w') as env:
    lines = [
        f'SECRET_KEY={SECRET_KEY}\n',
        f'SQLALCHEMY_DATABASE_URI={SQLALCHEMY_DATABASE_URI}\n',
        f'MAIL_USERNAME={MAIL_USERNAME}\n',
        f'MAIL_PASSWORD={MAIL_PASSWORD}\n',
        f'API_KEY={API_KEY}\n'
    ]
    env.writelines(lines)

print(f"File '{FILE_NAME}' has been created.")
