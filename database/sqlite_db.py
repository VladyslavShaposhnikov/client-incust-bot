import psycopg2

from config import DB_HOST, DB_NAME, DB_PASS, DB_USER


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
    cur.fetchone()
    base.commit()

# get count of all values in db table
async def sql_get_count():
    cur.execute('SELECT COUNT(*) from katalog')
    count = cur.fetchone()
    return count


#cur.close()

#base.close()