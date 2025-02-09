import configparser
from db import get_db

config = configparser.ConfigParser()
config.read("config.ini")

def create_podcast(episode_post_data: dict) -> str:
    connection = get_db()
    cursor = connection.cursor()

    podcast_name = episode_post_data["podcast_name"]
    rating = episode_post_data["rating"]
    genre = episode_post_data["genre"]

    sql = """INSERT INTO podcasts (podcast_name, rating, genre)
                VALUES (%s,%s,%s)
                RETURNING id;"""

    cursor.execute(sql, (podcast_name, rating, genre))
    return_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()

    return return_id


def add_to_podcast(episode_post_data : dict, podcast_id : int) -> str:
    connection = get_db()
    cursor = connection.cursor()


    episode_name = episode_post_data["episode_name"]
    duration = episode_post_data["duration"]
    upload_date = episode_post_data["upload_date"]
    location_url = episode_post_data["location_url"]

    sql = """INSERT INTO episodes (episode_name, duration, upload_date, location_url)
                VALUES (%s,%s,%s,%s)
                RETURNING id;"""

    cursor.execute(sql, (episode_name, duration, upload_date, location_url))
    return_id = cursor.fetchone()[0]
    joining_sql = """INSERT INTO podcast_episodes (podcast_id, episode_id)
                     VALUES (%s,%s);
                     """
    cursor.execute(joining_sql, (podcast_id, return_id))
    connection.commit()
    cursor.close()

    return return_id

def get_podcast_episodes(podcast_id: int) -> [dict]:
    connection = get_db()
    cursor = connection.cursor()

    sql = """SELECT episode_id FROM podcast_episodes WHERE podcast_id=%s; """

    cursor.execute(sql,(podcast_id,))

    episode_id_arrays = cursor.fetchall()
    return_episodes = []
    for episode_id in episode_id_arrays:
        episode_id = episode_id[0]
        return_sql = """SELECT * FROM episodes WHERE id=%s;"""
        cursor.execute(return_sql, (episode_id,))
        return_episodes.append(cursor.fetchone())
    cursor.close()
    return return_episodes
