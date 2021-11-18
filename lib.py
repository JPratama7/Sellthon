import os

from mysql import connector
from dotenv import load_dotenv, find_dotenv
from os.path import join, dirname


load_dotenv()

def logfunc(type, e):
    type = str(type).upper()
    with open("logbot.txt", "a") as log:
        log.write(f"{type} ERROR : {e}\n" )

def create_conn():
    host = os.environ.get("HOST")
    user = "root"
    password = os.environ.get("PASSWORD")
    database = os.environ.get("DATABASE")
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


def checkuser(telegramid):
    cursor = create_cursor()
    cursor.execute(f"SELECT COUNT(*) FROM user WHERE tele_id ={telegramid}")
    user = cursor.fetchone()
    cursor.close()
    if user[0] != 0:
        return True
    else:
        return False


def idorder(idbarang, idorang):
    now = datetime.datetime.now()
    seq = now.strftime("%Y%m%d%H%M")
    stridorang = str(idorang)
    stridbarang = str(idbarang)
    idorder = int(seq + stridorang + stridbarang)
    return idorder
