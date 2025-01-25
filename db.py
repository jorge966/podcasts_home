from flask import g, Flask
import psycopg2
import configparser

config = configparser.ConfigParser()

config.read("config.ini")

"""
We are getting the database connection IF it hasn't already been connected to
if the database connection has not already been established we then add it to the global context
"""
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = psycopg2.connect(
            host=config['Database']['host'],
            port=config['Database']['port'],
            database=config['Database']['db_name'],
            user=config['Database']['user_name'],
            password=config['Database']['password'])
    return db

"""
And this closes the database connection
"""
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()