import base64, codecs, json, requests

macaroon = open('secrets/macaroon.txt', 'rb').read()

TLS_PATH = 'secrets/tls.cert'


# - LND crear invoice normal
def lnd_normal_invoice(amount_sats):
    # print(macaroon)
    url = 'https://umbrel.local:8080/v1/invoices'
    headers = {'Grpc-Metadata-macaroon': macaroon}
    data = {
      'memo': 'Pago a pedrito',
      'value_msat': f"{amount_sats*1000}",
      'expiry': 86400
    }
    r = requests.post(url, headers=headers, data=json.dumps(data), verify=TLS_PATH)
    invoice = r.json()['payment_request']
    r_hash = r.json()['r_hash']
    payment_hash = codecs.encode(base64.b64decode(r_hash.encode('utf-8')), 'hex').decode("utf-8")
    # print(r.json())
    # print('\ninvoice es:', invoice, '\n')
    # print('payment_hash es:', payment_hash, '\n')
    return invoice, payment_hash


# - LND checkear estado invoice
def hodl_invoice_paid(payment_hash):
    # print(macaroon)
    # payment_hash2 = '735b0ef5ad4540236491be568ae30665cb4deceff9b3e41aa260897a32298109'
    url = f'https://umbrel.local:8080/v1/invoice/{payment_hash}'
    headers = {'Grpc-Metadata-macaroon': macaroon}
    r = requests.get(url, headers=headers, verify=TLS_PATH)
    return r.json()['state'], r.json()['settled']


# - LND crear hodl invoice
def create_hodl_invoice(payment_hash, amount_sats, expiration):
    # payment_hash = '780074488aa2c2a857bc24b364ec608adc65db24aabb699fe14619c0b22c60a3'
    url = 'https://umbrel.local:8080/v2/invoices/hodl'
    headers = {'Grpc-Metadata-macaroon': macaroon}
    data = {
      'memo': 'pago a joho',
      'hash': base64.b64encode(bytes.fromhex(payment_hash)).decode('utf8'),
      'value_msat': f"{int(amount_sats)*1000}",
      'expiry': f'{expiration}',
    }
    r = requests.post(url, headers=headers, data=json.dumps(data), verify=TLS_PATH)
    return(r.json()['payment_request'])


# - LND liquidar hodl invoice retorna json vacio
def settle_hodl_invoice(pre_image):
    # pre_image = 'a42e60563717d2ac78656ddd4478fa70bc0721a238bc5a933d431a6d8ebfe501'
    url = 'https://umbrel.local:8080/v2/invoices/settle'
    headers = {'Grpc-Metadata-macaroon': macaroon}
    data = {
      'preimage': base64.b64encode(bytes.fromhex(pre_image)).decode('utf8'),
    }
    r = requests.post(url, headers=headers, data=json.dumps(data), verify=TLS_PATH)
    # print(f'el return del settling es {r.json()}')
    return(r.json())



# - LND cancelar hodl invoice retorna un json vacio
def cancel_hodl_invoice(payment_hash):
    # payment_hash = '780074488aa2c2a857bc24b364ec608adc65db24aabb699fe14619c0b22c60a3'
    url = 'https://umbrel.local:8080/v2/invoices/cancel'
    headers = {'Grpc-Metadata-macaroon': macaroon}
    data = {
      'payment_hash': base64.b64encode(bytes.fromhex(payment_hash)).decode('utf8'),
    }
    r = requests.post(url, headers=headers, data=json.dumps(data), verify=TLS_PATH)
    # print(r.json())
    return(r.json())



