import sqlite3
import requests


def db_init():
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS baseofertas(
    user_id INTEGER,
    offer_id TEXT,
    description TEXT,
    pay_amount INTEGER,
    origin TEXT,
    destination TEXT,
    time_limit TEXT,
    created_date TEXT,
    dest_email TEXT,
    hodl_hash TEXT,
    state TEXT
    )""")
    connect.commit()
    connect.close()


def user_is_new(user_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT user_id FROM baseofertas WHERE user_id = {user_id[0]}')
    match = cursor.fetchone()
    connect.close()
    if match is None:
        return True
    else:
        return False


def add_user(user_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO baseofertas VALUES({user_id[0]}, '', '', 0, '', '', '', '', '', '', 'user_entry')")
    connect.commit()
    connect.close()


def delete_user(user_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"DELETE FROM baseofertas WHERE user_id = {user_id[0]}")
    connect.commit()
    connect.close()


def hay_ofertas():
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(
        f"SELECT offer_id, description, pay_amount, origin, destination, created_date, time_limit FROM baseofertas WHERE state = 'active'")
    ofertas = cursor.fetchall()
    connect.close()
    if len(ofertas) > 0:
        return True
    else:
        return False


def add_offer(user_id, message_id, offer, today_date):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    offer_id = f'{user_id}_{message_id}'
    data = [offer[data] for data in offer]
    cursor.execute(f"""INSERT INTO baseofertas  (user_id, offer_id, description, pay_amount, origin,
    destination, time_limit, created_date, dest_email, hodl_hash,  state) VALUES ({user_id},'{offer_id}','{data[0]}',{data[1]},'{data[2]}','{data[3]}','{data[4]}','{today_date}','{data[5]}','','active')""")
    connect.commit()
    connect.close()


def list_offers():
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(
        f"SELECT offer_id, description, pay_amount, origin, destination, created_date, time_limit FROM baseofertas WHERE state = 'active'")
    ofertas = cursor.fetchall()
    connect.close()
    return ofertas


def get_offer(offer_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT offer_id, pay_amount, user_id, description, hodl_hash FROM baseofertas WHERE state = 'active' and offer_id = '{offer_id}'")
    oferta = cursor.fetchone()
    connect.close()
    return oferta


def sats_value(amount):
    try:
        res = requests.get('https://api.opennode.co/v1/rates/')
        btcprice = int(res.json()['data']['BTCCLP']['CLP'])
        sats_value = int(amount * 100000000 / btcprice)
        return sats_value
    except:
        try:
            res = requests.get(f'https://api.yadio.io/convert/{amount}/clp/btc')
            sats_value = int(res.json()['result'] * 100000000)
            return sats_value
        except:
            return 0


def expire_offer(user_id, offer_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE baseofertas SET state = 'inactive' WHERE user_id = '{user_id}' and offer_id = '{offer_id}';")
    connect.commit()
    connect.close()
    return


def auto_expire_offers():
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"UPDATE baseofertas SET state = 'inactive' WHERE created_date < date('now','localtime');")
    # print('ofertas antiguas eliminadas')
    cursor.execute(f"UPDATE baseofertas SET hodl_hash = '' WHERE created_date < date('now','localtime');")
    connect.commit()
    connect.close()


def offer_is_active(offer_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT state FROM baseofertas WHERE offer_id = '{offer_id}'")
    offer_state = cursor.fetchone()
    if offer_state == 'active':
        return True
    else:
        return False


def take_offer(payment_hash, offer_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"UPDATE baseofertas SET hodl_hash = '{payment_hash}' WHERE offer_id = '{offer_id}';")
    # cursor.execute(f"UPDATE baseofertas SET state = 'taken' WHERE offer_id = '{offer_id}';")
    connect.commit()
    connect.close()
