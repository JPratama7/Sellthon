from sqlalchemy import create_engine
import pymysql

try:
    print('create engine')
    engine = create_engine("mysql+pymysql://root:@localhost/bot",echo=True)
    print('engine created')
    print('creating connection')
    db = engine.connect()
except Exception as e:
    print(f'error : {e}')

query = select('user').values