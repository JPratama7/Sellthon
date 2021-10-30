import os

from mysql import connector
from dotenv import load_dotenv

def logfunc(type, e):
    type = str(type).upper()
    with open("logbot.txt", "a") as log:
        log.write(f"{type} ERROR : {e}\n" )

def create_conn():
    load_dotenv()
    host = os.getenv("HOST")
    user = "root"
    password = os.getenv("PASSWORD")
    database = os.getenv("DATABASE")
    try:
        db = connector.connect(host=host, user=user, password=password, database=database, autocommit=True)
        return db
    except Exception as e:
        print(e)
        logfunc("DB CONN NOT CREATED", e)

def create_cursor():
    db = create_conn()
    try:
        cursor = db.cursor()
        return cursor
    except Exception as e:
        logfunc('CURSOR NOT CREATED', e)
