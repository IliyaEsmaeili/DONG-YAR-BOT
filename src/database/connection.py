import os

import  psycopg2
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER_NAME = os.getenv("DB_USER_NAME")

conn = psycopg2.connect(host = DB_HOST , database = DB_NAME , user = DB_USER_NAME , port = DB_PORT)
conn.autocommit = True

