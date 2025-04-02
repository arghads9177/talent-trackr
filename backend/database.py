import os
import pymysql
import bcrypt
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "talenttrackr")

connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = connection.cursor()

def create_user(firstname, lastname, email, username, password):
    # Check for duplicate username
    query = "SELECT username FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    if cursor.fetchone():
        return False, "Username already exists."

    # Hashing the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    query = "INSERT INTO users (firstname, lastname, email, username, password_hash) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (firstname, lastname, email, username, hashed_password))
    connection.commit()
    return True, "User created successfully."

def authenticate_user(username, password):
    query = "SELECT password_hash, user_id FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        stored_password_hash = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
            return {"user_id": result[1], "status": True}
    return {"status": False}

def close_connection():
    cursor.close()
    connection.close()
