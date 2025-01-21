from flask import Flask,request
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

@app.route('/create_user', methods=['POST'])
def create_user():
    curr = conn.cursor()
    post_data = request.form

    username = post_data["username"]
    password = post_data["password"]
    email = post_data["email"]

    sql = """INSERT INTO users (username, password, email)
                VALUES (%s,%s,%s)
                RETURNING id;"""

    curr.execute(sql, (username, password, email))
    return_id = curr.fetchone()[0]
    conn.commit()
    curr.close()
    conn.close()
    return {
        "created_user_id": return_id
    }

@app.route('/create_podcast', methods=['POST'])
def create_podcast():
    curr = conn.cursor()
    post_data = request.form

    podcast_name = post_data["podcast_name"]
    rating = post_data["rating"]
    genre = post_data["genre"]

    sql = """INSERT INTO podcasts (podcast_name, rating, genre)
                VALUES (%s,%s,%s)
                RETURNING id;"""

    curr.execute(sql, (podcast_name, rating, genre))
    return_id = curr.fetchone()[0]
    conn.commit()
    curr.close()
    conn.close()
    return {
        "created_podcast_id": return_id
    }


@app.route('/create_episode', methods=['POST'])
def create_episode():
    curr = conn.cursor()
    post_data = request.form

    episode_name = post_data["episode_name"]
    duration = post_data["duration"]
    upload_date = post_data["upload_date"]
    location_url = post_data["location_url"]

    sql = """INSERT INTO episodes (episode_name, duration, upload_date, location_url)
                VALUES (%s,%s,%s,%s)
                RETURNING id;"""

    curr.execute(sql, (episode_name, duration, upload_date, location_url))
    return_id = curr.fetchone()[0]
    conn.commit()
    curr.close()
    conn.close()
    return {
        "created_episode_id": return_id
    }

if __name__ == '__main__':
    app.run()

