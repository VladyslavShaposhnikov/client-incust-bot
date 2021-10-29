""" import psycopg2
import sqlalchemy
from sqlalchemy import create_engine

from config import DB_HOST, DB_NAME, DB_PASS, DB_USER, ENG


engine = create_engine('sqlite:///sqlite3.db')


# connection to db
def sql_start():
    global base, cur
    base = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = base.cursor()
    if base:
        print('DB connected success')
    cur.execute('CREATE TABLE IF NOT EXISTS katalog(id SERIAL PRIMARY KEY, name TEXT, u_id TEXT, title TEXT, description TEXT, media TEXT)')
    base.commit()

# add value to db table
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO katalog (name, u_id, title, description, media) VALUES (%s, %s, %s, %s, %s)', tuple(data.values()))
        base.commit()

# show all values
async def sql_all():
    cur.execute('SELECT * FROM katalog')
    set_of_ivents = cur.fetchall()
    return set_of_ivents

# latest id in db table
async def sql_latest_id():
    cur.execute('SELECT MAX(id) FROM katalog')
    last_id = cur.fetchone()
    return last_id

# get first 2 items for katalog
async def sql_read(limit):
    cur.execute('SELECT * FROM katalog LIMIT (%s)',(limit,))
    set_of_ivents = cur.fetchall()
    return set_of_ivents

# get items for pagination
async def sql_read2(last_id, limit):
    cur.execute('SELECT * FROM katalog WHERE id > (%s) LIMIT (%s)',(last_id, limit))
    set_of_ivents = cur.fetchall()
    return set_of_ivents

# get event
async def sql_get_ivent(id):
    cur.execute('SELECT * FROM katalog WHERE id = (%s)', (id,))
    ivent = cur.fetchone()
    return ivent

# delete event
async def sql_del_ivent(id):
    cur.execute('DELETE FROM katalog WHERE id = (%s)', (id,))
    #cur.fetchone()
    base.commit()

# get count of all values in db table
async def sql_get_count():
    cur.execute('SELECT COUNT(*) from katalog')
    count = cur.fetchone()
    return count


#cur.close()

#base.close() """

""" 
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Column, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import sessionmaker

from config import ENG

#engine = create_engine(ENG)
engine = create_engine('sqlite:///sqlite3.db')
meta = MetaData()

#katalog = sqlalchemy.Table('Katalog', meta,
#Column('id', Integer, primary_key=True),
#Column('name', String(100)),
#Column('i_id', String(20)),
#Column('title', String(100)),
#Column('description', String(250)))

#meta.create_all(engine)

#conn = engine.connect()

# connection to db
def sql_start():
    global base, katalog
    base = engine.connect()
    if base:
        print('DB connected success')

    katalog = sqlalchemy.Table('Katalog', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(100)),
    Column('i_id', String(20)),
    Column('title', String(100)),
    Column('description', String(250)),
    Column('media', String(250)))

    meta.create_all(engine)

# add value to db table
async def sql_add_command(state):
    async with state.proxy() as data:
        values = katalog.insert().values(name=data['ivent_name'], i_id=data['u_id'], title=data['ivent_title'], description=data['ivent_description'], media=data['ivent_media'])
        base.execute(values)
        
# show all values
async def sql_all():
    query = katalog.select()
    num = 0
    for i in base.execute(query):
        num += 1
    return num

# get first 2 items for katalog
async def sql_read(limit):
    query = katalog.select().limit(limit)
    return base.execute(query)

# latest id in db table
async def sql_latest_id():
    max_id = func.max(katalog.id)
    query = katalog.select().where(id=max_id)
    return base.execute(query)

# get items for pagination
async def sql_read2(last_id, limit):
    query = katalog.select().where(id > last_id).limit(limit)
    return base.execute(query)

# get event
async def sql_get_ivent(id):
    ivent = katalog.select().where(id=id)
    return base.execute(ivent)

# delete event
async def sql_del_ivent(id):
    ivent = katalog.delete().where(id=id)
    return base.execute(ivent) """




import sqlalchemy
from sqlalchemy import create_engine, MetaData, Column, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///sqlite3.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Katalog(Base):
    __tablename__ = 'katalog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    i_id = Column(String(20))
    title = Column(String(50))
    description = Column(String(255))
    media = Column(String(255))



def sql_start():
    Base.metadata.create_all(engine)

session = Session()

# add value to db table
async def sql_add_command(state):
    async with state.proxy() as data:
        values = Katalog(name=data['ivent_name'], i_id=data['u_id'], title=data['ivent_title'], description=data['ivent_description'], media=data['ivent_media'])
        session.add(values)
        session.commit()
        
# show all values
async def sql_all():
    num = 0
    for i in session.query(Katalog).order_by(Katalog.id).all():
        num += 1
    return num

# get first 2 items for katalog
async def sql_read(limit):
    q = session.query(Katalog).order_by(Katalog.id).limit(limit)
    return q.all()

# latest id in db table
async def sql_latest_id():
    max_id = session.query(func.max(Katalog.id))
    #q = session.query(Katalog).filter(id=max_id)
    #return q.first()
    return max_id.first()[0]

# get items for pagination
async def sql_read2(last_id, limit):
    q = session.query(Katalog).filter(Katalog.id > last_id).limit(limit)
    if limit == 1:
        return q.first()
    return q.all()

# get event
async def sql_get_ivent(id):
    ivent = session.query(Katalog).get(id)
    return ivent

# delete event
async def sql_del_ivent(id):
    session.query(Katalog).filter(id=id).delete()
    session.commit()
