import requests

url_wallet = open('secrets/url_wallet.txt', 'r').read()
wallet_id = open('secrets/lnbits_wallet_id.txt', 'r').read()
api_read_key = open('secrets/api_read_key.txt', 'r').read()
api_admin_key = open('secrets/api_admin_key.txt', 'r').read()
admin_user_id = open('secrets/user_lnbits_admin.txt', 'r').read()

# Get balance
def get_lnbits_balance():
    url = 'http://umbrel.local:3007/api/v1/wallet'
    api_key = api_read_key
    x = requests.get(url, headers = {"X-Api-Key": f"{api_key}"})
    balance = int(x.json()['balance'])/1000
    # wallet_name = x.json()['name']
    return balance

# Decode Invoice
def decode_invoice(invoice):
    api_key = api_read_key
    url = 'http://umbrel.local:3007/api/v1/payments/decode'
    y = requests.post(url, json = {"data": f"{invoice}"}, headers = {"X-Api-Key": f"{api_key}", "Content-type": "application/json"})
    payment_hash = y.json()['payment_hash']
    amount = int(y.json()['amount_msat'])/1000
    expiration = int(y.json()['expiry'])
    # print(f"hash: {payment_hash}, amount en sats: {amount}, expiracion en: {expiration} segundos")
    return payment_hash, amount, expiration


# Pay invoice TODO ver que retornar
def pay_invoice(invoice):
    api_key = api_admin_key
    url = 'http://umbrel.local:3007/api/v1/payments'
    z = requests.post(url, json = {"out": True, "bolt11": f"{invoice}"}, headers = {"X-Api-Key": f"{api_key}", "Content-type": "application/json"})
    # return z.text
    print(z.text)


# Check invoice for Pre image
def check_invoice_pre_image(payment_hash):
    api_key = api_read_key
    url = f'http://umbrel.local:3007/api/v1/payments/{payment_hash}'
    w = requests.get(url, headers = {"X-Api-Key": f"{api_key}"})
    status_payment = w.json()['paid']
    pre_image = w.json()['preimage']
    # print(f'Invoice pagado, hash {payment_hash}, \npre_image {pre_image},\nstatus de pago: {status_payment}')
    return pre_image


# Refill wallet TODO ver que retornar
def refill_wallet(amount_sats):
    url = f'http://umbrel.local:3007/admin/api/v1/topup/?usr={admin_user_id}'
    v = requests.put(url, json = {"id": f"{wallet_id}", "amount" : f"{amount_sats}"}, headers = {"Content-type": "application/json"})
    print(v.json())

