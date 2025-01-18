import psycopg2
import configparser

config = configparser.ConfigParser()

config.read("config.ini")


conn = psycopg2.connect(
        host=config['Database']['host'],
        port=config['Database']['port'],
        database=config['Database']['db_name'],
        user=config['Database']['user_name'],
        password=config['Database']['password'])



def create_user_table():
    curr = conn.cursor()
    curr.execute('CREATE TABLE users (id serial PRIMARY KEY, username varchar, password varchar, email varchar);')
    conn.commit()
    curr.close()



def create_podcast_table():
    curr = conn.cursor()
    curr.execute('CREATE TABLE podcasts (id serial PRIMARY KEY, podcast_name varchar, rating int, genre varchar)')
    conn.commit()
    curr.close()

def create_episode_table():
    curr = conn.cursor()
    curr.execute('CREATE TABLE episodes (id serial PRIMARY KEY, episode_name varchar, duration int, upload_date date, location_url varchar)')
    conn.commit()
    curr.close()

create_user_table()
create_episode_table()
create_podcast_table()

conn.close()