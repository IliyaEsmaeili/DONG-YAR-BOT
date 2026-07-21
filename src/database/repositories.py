from connection import conn

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

