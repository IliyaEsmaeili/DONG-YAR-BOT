from .connection import conn
def execute_query( query , params ) :
    with conn.cursor() as cursor :
        cursor.execute(query , params)

def fetch_one(query , params) :
    with conn.cursor() as cursor :
        cursor.execute(query , params)
        return cursor.fetchone()

def fetch_all(query , params) :
    with conn.cursor() as cursor :
        cursor.execute(query , params)
        return cursor.fetchall()

def save_user(user):
    with conn.cursor() as cursor :
        cursor.execute("""INSERT INTO users(telegram_id, full_name) VALUES
            (%s,%s)
        """ , (user.telegram_id , user.full_name))

