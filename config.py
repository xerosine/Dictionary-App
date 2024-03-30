"""pymysql connection variables configuration"""
from os import environ, path
from dotenv import load_dotenv


# Specificy a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

timeout = 10
# General Config
secret = environ.get('secret')
charset = environ.get('charset')
connect_timeout = timeout
db = environ.get('db')
host = environ.get('host')
password = environ.get('password')
read_timeout = timeout
port = environ.get('port')
user = environ.get('user')
write_timeout = timeout