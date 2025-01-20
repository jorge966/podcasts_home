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

@app.route('/create_user', methods=['POST'])
def create_user():
    # Access the post data here, and push this information into the DB.
    post_data = request.data
    username = ... 
    password = ...
    email = ... 

    sql = """INSERT INTO users VALUES
                (%s, %s, %s);"""
    # Get the DB cursor using the conn object. (look to the seeddb.py file for examples)

    # The code below is an example of how to execute the SQL query we created on line 27.
    curr.execute(sql, (username, password, email)) 
    conn.commit()
    curr.close()
    conn.close()
    
if __name__ == '__main__':
    app.run()
