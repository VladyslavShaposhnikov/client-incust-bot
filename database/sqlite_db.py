from sqlalchemy import create_engine, Column, func
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
    session.query(Katalog).filter_by(id=id).delete()
    session.commit()
