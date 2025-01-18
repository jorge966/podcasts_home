from flask import Flask
import psycopg2
import configparser

config = configparser.ConfigParser()

config.read("config.ini")

app = Flask(__name__)

conn = psycopg2.connect(
        host=config['Database']['host'],
        port=config['Database']['port'],
        database=config['Database']['db_name'],
        user=config['Database']['user_name'],
        password=config['Database']['password'])

@app.route('/')
def hello_world():
    return 'hello test'


if __name__ == '__main__':
    app.run()