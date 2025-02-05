from dbm import error

from flask import Flask,request, jsonify
import psycopg2
import configparser
from db import get_db
from services import podcasts

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
    post_data = request.form
    response = podcasts.create_podcast(post_data)

    return {
        "created_podcast_id": response
    }

@app.route('/get_podcast_by_name', methods=['GET'])
def get_podcast_by_name():
    connection = get_db()
    cursor = connection.cursor()
    args = request.args

    podcast_name = args.get("podcast_name")

    sql = """SELECT * FROM podcasts WHERE podcast_name=%s;"""

    cursor.execute(sql, (podcast_name,))
    current_podcast = cursor.fetchone()
    cursor.close()

    return{
        "current_podcast" : current_podcast
    }
@app.route('/get_podcast_by_genre', methods=['GET'])
def get_podcast_by_genre():
    connection = get_db()
    cursor = connection.cursor()
    args = request.args

    podcast_by_genre = args.get("genre")

    sql = """SELECT * FROM podcasts WHERE genre=%s;"""

    cursor.execute(sql, (podcast_by_genre,))
    current_podcast_genre = cursor.fetchone()
    cursor.close()

    return{
        "current podcast(s) by genre" : current_podcast_genre
    }

@app.route('/get_podcast_by_id', methods=['GET'])
def get_podcast_by_id():
    connection = get_db()
    cursor = connection.cursor()
    args = request.args

    podcast_id = args.get("id")

    sql = """SELECT * FROM podcasts WHERE id=%s;"""

    cursor.execute(sql, (podcast_id,))
    current_id = cursor.fetchone()
    cursor.close()

    return{
        "current_podcast" : current_id
    }

@app.route('/delete_podcast', methods=['DELETE'])
def delete_podcast():
    connection = get_db()
    cursor = connection.cursor()
    args = request.args

    podcast_name = args.get("podcasts")

    sql = """DELETE FROM podcasts WHERE podcast_name=%s
             RETURNING id;"""

    cursor.execute(sql, (podcast_name,))
    deleted_podcast_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()

    return{
        "deleted_episode_id" : deleted_podcast_id
    }

@app.route('/get_podcast_episodes', methods=['GET'])
def get_podcast_episodes():

    args = request.args

    podcast_id = args.get("id")
    response = podcasts.get_podcast_episodes(int(podcast_id))

    return response

"""
Episodes
"""
@app.route('/create_episode', methods=['POST'])
def create_episode():

    
    post_data = request.form
    podcast_id = post_data.get("podcast_id", None)
    if podcast_id is None:
        return  {
            "Error": "Podcast Id not found"
        }
    elif podcast_id.isdigit():
        podcast_id = int(podcast_id)
    else:
        return {
            "Error": "Podcast Id is invalid"
        }

    response = podcasts.add_to_podcast(post_data,podcast_id)

    return {
        "created_episode_id": response
    }

@app.route('/get_episode', methods=['GET'])
def get_episode():
    connection = get_db()
    cursor = connection.cursor()
    args = request.args

    episode_name = args.get("episode_name")

    sql = """SELECT * FROM episodes WHERE episode_name=%s;"""

    cursor.execute(sql, (episode_name,))
    current_episode = cursor.fetchone()
    cursor.close()

    return{
        "current_episode" : current_episode
    }

@app.route('/get_episode_by_id', methods=['GET'])
def get_episode_by_id():
    connection = get_db()
    cursor = connection.cursor()
    args = request.args

    episode_id = args.get("id")

    sql = """SELECT * FROM episodes WHERE id=%s;"""

    cursor.execute(sql, (episode_id,))
    current_id = cursor.fetchone()
    cursor.close()

    return{
        "current_episode" : current_id
    }

@app.route('/delete_episode', methods=['DELETE'])   #to delete potential duplicates
def delete_episode():
    connection = get_db()
    cursor = connection.cursor()
    args = request.args

    episode_name = args.get("episodes")

    sql = """DELETE FROM episodes WHERE episode_name=%s
             RETURNING id;"""

    cursor.execute(sql, (episode_name,))
    deleted_episode_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()

    return{
        "deleted_episode_id" : deleted_episode_id
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

@app.route('/get_user_by_id', methods=['GET'])
def get_user_by_id():
    connection = get_db()
    cursor = connection.cursor()
    args = request.args

    user_id = args.get("id")

    sql = """SELECT * FROM users WHERE id=%s;"""

    cursor.execute(sql, (user_id,))
    current_id = cursor.fetchone()
    cursor.close()

    return{
        "current_user" : current_id
    }

@app.route('/update_user_by_id', methods=['PUT'])
def update_user_by_id():
    connection = get_db()
    cursor = connection.cursor()
    post_data = request.form

    user_id = post_data["id"]


    sql = """SELECT * FROM users WHERE id=%s;"""

    cursor.execute(sql, (user_id,))
    current_user = cursor.fetchone()
    if current_user is None:
        return {
            "error": "id not found"
        }
    user = {
        "id":current_user[0], "username":current_user[1],"password":current_user[2],"email":current_user[3]
    }

    if "username" in post_data:
        user["username"] = post_data["username"]
    if "password" in post_data:
        user["password"] = post_data["password"]
    if "email" in post_data:
        user["email"] = post_data["email"]

    update_sql = """UPDATE users
                    SET username=%s, password=%s, email=%s
                    WHERE id=%s;"""
    cursor.execute(update_sql,(user["username"],user["password"],user["email"],user_id))
    connection.commit()
    cursor.close()

    return user

if __name__ == '__main__':
    app.run()

