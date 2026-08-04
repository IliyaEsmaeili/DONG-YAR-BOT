from .connection import conn
from data import User , Dong
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

def save_dong(dong):
    with conn.cursor() as cursor :
        cursor.execute("""INSERT INTO dongs(group_id, creator_id) VALUES
            (%s,%s)
        """ , (dong.group_id, dong.creator_id))

def user_state_fetch(message):
    user = message.from_user
    telegram_id = user.id
    str_telegram_id = str(telegram_id)
    fetch_result = fetch_one("""SELECT * FROM users WHERE telegram_id = %s
    """ , (str_telegram_id , ))
    if fetch_result is None : return None
    return fetch_result[3]

def change_user_state(user, state) :
    telegram_id = user.id
    str_telegram_id = str(telegram_id)
    with conn.cursor() as cursor :
        cursor.execute("""UPDATE users SET state = %s WHERE telegram_id = %s 
        """ , (state , str_telegram_id))

def get_user_from_telegram_id(telegram_id):
    data = fetch_one("""SELECT * FROM users WHERE telegram_id = %s
    """ , (telegram_id , ))
    print("data = " , data)
    user = User(telegram_id = telegram_id , full_name=data[2] , state=data[3])

    dongs= fetch_all("""SELECT * FROM dongs WHERE creator_id = %s 
    """ , (telegram_id , ))
    user.dong = []
    for dong_tuple in dongs :
        dong = Dong(dong_id=dong_tuple[0], group_id=dong_tuple[5], creator_id=dong_tuple[6] , big_prompt_message=dong_tuple[4])
        user.dong.append(dong)

    return user