from flask import Flask,request, jsonify
import psycopg2
import configparser
from db import get_db

config = configparser.ConfigParser()

config.read("config.ini")

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello test'

"""
Podcasts
"""
@app.route('/create_podcast', methods=['POST'])
def create_podcast():
    connection = get_db()
    cursor = connection.cursor()
    
    post_data = request.form

    podcast_name = post_data["podcast_name"]
    rating = post_data["rating"]
    genre = post_data["genre"]

    sql = """INSERT INTO podcasts (podcast_name, rating, genre)
                VALUES (%s,%s,%s)
                RETURNING id;"""

    cursor.execute(sql, (podcast_name, rating, genre))
    return_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()

    return {
        "created_podcast_id": return_id
    }

"""
Episodes
"""
@app.route('/create_episode', methods=['POST'])
def create_episode():
    connection = get_db()
    cursor = connection.cursor()
    
    post_data = request.form

    episode_name = post_data["episode_name"]
    duration = post_data["duration"]
    upload_date = post_data["upload_date"]
    location_url = post_data["location_url"]

    sql = """INSERT INTO episodes (episode_name, duration, upload_date, location_url)
                VALUES (%s,%s,%s,%s)
                RETURNING id;"""

    cursor.execute(sql, (episode_name, duration, upload_date, location_url))
    return_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()

    return {
        "created_episode_id": return_id
    }

"""
Users
"""
@app.route('/create_user', methods=['POST'])
def create_user():
    connection = get_db()
    cursor = connection.cursor()

    post_data = request.form

    username = post_data["username"]
    password = post_data["password"]
    email = post_data["email"]

    sql = """INSERT INTO users (username, password, email)
                VALUES (%s,%s,%s)
                RETURNING id;"""

    cursor.execute(sql, (username, password, email))
    return_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()

    return {
        "created_user_id": return_id
    }

@app.route('/get_user', methods=['GET'])
def get_user():
    connection = get_db()
    cursor = connection.cursor()
    args = request.args

    user_name = args.get("username")

    sql = """SELECT * FROM users WHERE username=%s;"""

    cursor.execute(sql, (user_name,))
    user = cursor.fetchone()
    cursor.close()

    return{
        "current_user" : user
    }

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    connection = get_db()
    cursor = connection.cursor()
    args = request.args

    user_name = args.get("username")

    sql = """DELETE FROM users WHERE username=%s
             RETURNING id;"""

    cursor.execute(sql, (user_name,))
    deleted_user_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()

    return{
        "deleted_user_id" : deleted_user_id
    }

if __name__ == '__main__':
    app.run()

