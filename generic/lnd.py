import base64, codecs, json, requests

macaroon = open('../secrets/macaroon.txt', 'r').read()
TLS_PATH = '../secrets/tls.cert'

# - LND crear invoice normal
def lnd_normal_invoice(amount_sats):
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
    # print('\npayment_hash es:', payment_hash, '\n')
    return invoice, payment_hash


# - LND checkear estado invoice TODO ver que retornar
def hodl_invoice_paid(payment_hash):
    # payment_hash = '735b0ef5ad4540236491be568ae30665cb4deceff9b3e41aa260897a32298109'
    url = f'https://umbrel.local:8080/v1/invoice/{payment_hash}'
    headers = {'Grpc-Metadata-macaroon': macaroon}
    r = requests.get(url, headers=headers, verify=TLS_PATH)
    print(r.json())

# - LND crear hodl invoice TODO ver que retornar
def create_hodl_invoice(payment_hash, amount_sats):
    # payment_hash = '780074488aa2c2a857bc24b364ec608adc65db24aabb699fe14619c0b22c60a3'
    url = 'https://umbrel.local:8080/v2/invoices/hodl'
    headers = {'Grpc-Metadata-macaroon': macaroon}
    data = {
      'memo': 'pago a joho',
      'hash': base64.b64encode(bytes.fromhex(payment_hash)).decode('utf8'),
      'value_msat': f"{amount_sats*1000}",
      'expiry': 86400,
    }
    r = requests.post(url, headers=headers, data=json.dumps(data), verify=TLS_PATH)
    print(r.json())


# - LND liquidar hodl invoice TODO ver que retornar
def settle_hodl_invoice(pre_image):
    # pre_image = 'a42e60563717d2ac78656ddd4478fa70bc0721a238bc5a933d431a6d8ebfe501'
    url = 'https://umbrel.local:8080/v2/invoices/settle'
    headers = {'Grpc-Metadata-macaroon': macaroon}
    data = {
      'preimage': base64.b64encode(bytes.fromhex(pre_image)).decode('utf8'),
    }
    r = requests.post(url, headers=headers, data=json.dumps(data), verify=TLS_PATH)
    print(r.json())



# - LND cancelar hodl invoice TODO ver que retornar
def cancel_hodl_invoice(payment_hash):
    # payment_hash = '780074488aa2c2a857bc24b364ec608adc65db24aabb699fe14619c0b22c60a3'
    url = 'https://umbrel.local:8080/v2/invoices/cancel'
    headers = {'Grpc-Metadata-macaroon': macaroon}
    data = {
      'payment_hash': base64.b64encode(bytes.fromhex(payment_hash)).decode('utf8'),
    }
    r = requests.post(url, headers=headers, data=json.dumps(data), verify=TLS_PATH)
    print(r.json())



