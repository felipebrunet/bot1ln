
# TODO implementar notificacion y cobro a oferente GRANDE
# TODO implementar notificacion email a destinatario GRANDE


import telebot
from datetime import date
from time import sleep
from generic.functions import add_user, user_is_new, db_init, hay_ofertas
from generic.functions import add_offer, list_offers, get_offer, sats_value, expire_offer, auto_expire_offers
from generic.lnbits import get_lnbits_balance, decode_invoice
from generic.lnbits import pay_invoice, check_invoice_pre_image, refill_wallet
from generic.lnd import lnd_normal_invoice, hodl_invoice_paid, create_hodl_invoice
from generic.lnd import settle_hodl_invoice, cancel_hodl_invoice

BOT_TOKEN = open('secrets/bot_token.txt', 'r').read()
bot = telebot.TeleBot(BOT_TOKEN)

settlear_invoice = False
invoice_moto = 'lntb31u1pjhvjf8pp5cpn7kj0qq26q9sxdcfuwt7890ggzq00ctkzk5a7m2nzph8wgw9dsdqqcqzzsxqyz5vqsp58tmucy9hdnujcjdyjnp83q32nzz8whxaq5hag2zjnk60gqqjm0ts9qyyssqp44tdfjruskz5mu42zpm64fktxnu35j4vwgp73w2wt7kuuzd8edksvazznn8x0y2sv3cmzuzyk8jnqxqczzc728wesvnlv2yft4vfagpuxea7g'
payment_hash, amount, _ = decode_invoice(invoice_moto)
# sleep(2)
# cancel_hodl_invoice(payment_hash)
print(f'El payment hash del pago moto es {payment_hash}')
sleep(2)
print('Creando hodl invoice')
sleep(2)
hodl_invoice = create_hodl_invoice(payment_hash, amount, 2000)
print(f"el hodl invoice es: {hodl_invoice}")
sleep(2)
print('wallet externa pagara hodl invoice')
sleep(2)
hodl_invoice_pending = True
while hodl_invoice_pending:
    sleep(2)
    status_hodl, _ = hodl_invoice_paid(payment_hash)
    print(f'El estatus del hodl invoice es {status_hodl}')
    if status_hodl == 'ACCEPTED':
        hodl_invoice_pending = False
sleep(2)
print('hodl invoice fue aceptado, ahora corresponde pagar invoice moto')
print('pagando invoice moto')
pay_invoice(invoice_moto)
sleep(2)
print('Ahora que se ha pagado el invoice moto, obtenemos el pre image del invoice pagado')
sleep(2)
pre_image = check_invoice_pre_image(payment_hash)
print(f'Pre imagen es {pre_image}')
sleep(2)
if settlear_invoice:
    print('dado que settlear invoice esta en True, pagamos hodl invoice')
    settle_hodl_invoice(pre_image)
    sleep(2)
else:
    print('dado que settlear invoice esta en False, anulamos el hodl invoice, devolvemos el monto y perdemos plata')
    cierre_hodl_invoice = cancel_hodl_invoice(payment_hash)
    if cierre_hodl_invoice == {}:
        print('hodl invoice ha sido cancelado')

bot.state = None
DESCRIPTION = 1
AMOUNT = 2
ORIGIN = 3
DESTINATION = 4
LIMIT_TIME = 5
DEST_EMAIL = 6
CONFIRMATION = 7
SELECTOFFER = 8
ENTERINVOICE = 9


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        db_init()
        user_id = [message.chat.id]
        if user_is_new(user_id):
            add_user(user_id)
            bot.send_message(message.chat.id, 'Usuario se ha creado')


@bot.message_handler(commands=['ofertas'])
def listar_ofertas(message):
    if message.chat.type == 'private':
        auto_expire_offers()
        if hay_ofertas():
            bot.send_message(message.chat.id, 'Estas son las ofertas')
            ofertas = list_offers()
            for oferta in ofertas:
                sep = '+'
                dir_origen = sep.join(oferta[3].replace(',', '').split())
                dir_destino = sep.join(oferta[4].replace(',', '').split())
                recorrido = f"<a href='https://www.google.com/maps/dir/{dir_origen}/{dir_destino}?entry=ttu'>Ver Distancia</a>"
                bot.send_message(message.chat.id, f"Oferta: {oferta[0]}\nDescripcion: {oferta[1]}\nMonto: ${oferta[2]}\nDesde: {oferta[3]}\nHasta: {oferta[4]}\nFecha: {oferta[5]}\nHora: {oferta[6]}\nVer Distancia: {recorrido}", parse_mode="HTML")
            # expire_offer(message.chat.id, '676140835_317')

        else:
            bot.send_message(message.chat.id, 'No hay ofertas disponibles')


@bot.message_handler(commands=['aceptar'])
def listar_ofertas(message):
    if message.chat.type == 'private':
        auto_expire_offers()
        global offer_data
        offer_data = {'offer_id': ''}
        if hay_ofertas():
            bot.send_message(message.chat.id, 'Indicar codigo oferta')
            bot.state = SELECTOFFER
        else: bot.send_message(message.chat.id, 'No hay ofertas disponibles')

@bot.message_handler(func=lambda msg: bot.state == SELECTOFFER)
def select_offer(message):
    if message.chat.type == 'private':
        try:
            offer_data['offer_id'] = str(message.text)
            offer = get_offer(offer_data['offer_id'])
            offer_sats_value = sats_value(offer[1])
            bot.send_message(message.chat.id, f'Oferta {offer_data["offer_id"]} seleccionada.')
            bot.send_message(message.chat.id, f'Favor Pegar Invoice por {offer_sats_value} sats, con expiracion de 24h')
            bot.state = ENTERINVOICE
        except:
            bot.send_message(message.chat.id, 'Error de ingreso')
            bot.send_message(message.chat.id, 'Indicar codigo oferta:')

@bot.message_handler(func=lambda msg: bot.state == ENTERINVOICE)
def save_invoice(message):
    if message.chat.type == 'private':
        offer_value = get_offer(offer_data["offer_id"])[1]
        offer_sats_value = sats_value(offer_value)
        try:
            invoice = str(message.text)
            invoice_hash, invoice_sats, invoice_exp = decode_invoice(invoice)
            if abs(int(offer_sats_value) - int(invoice_sats))/int(offer_sats_value) > 0.005:
                bot.send_message(message.chat.id, 'Error de monto')
                bot.send_message(message.chat.id, f'Favor Pegar Invoice por {offer_sats_value} sats')
            elif int(invoice_exp) < 86400:
                bot.send_message(message.chat.id, 'Error de expiracion. Se necesita expiracion de 24h (86.400 seg)')
                bot.send_message(message.chat.id, f'Favor Pegar Invoice por {offer_sats_value} sats, con expiracion de 24h')

            else:
                bot.send_message(message.chat.id, 'Invoice guardado. Espere confirmacion de oferente')
                bot.send_message(message.chat.id, 'Cuando oferente confirme, el pago quedara asegurado en la aplicacion')

                bot.state = None
        except:
            bot.send_message(message.chat.id, f'Error de ingreso')
            bot.send_message(message.chat.id, f'Favor Pegar Invoice por {offer_sats_value} sats, con expiracion de 24h')




# -----------------------------------------------------------------------------------------
# RUTINA PARA INGRESAR OFERTA
# -----------------------------------------------------------------------------------------
@bot.message_handler(commands=['anunciar'])
def anunciar_oferta(message):
    if message.chat.type == 'private':
        global offer
        offer = {'description': '', 'amount': 0, 'origin': '', 'destination': '', 'limit_time': '', 'dest_email': ''}
        bot.send_message(message.chat.id, 'Creando Oferta:')
        bot.send_message(message.chat.id, 'Ingrese descripcion (ej. Pedido Claudio restaurant BitpointBurger:')
        bot.state = DESCRIPTION




@bot.message_handler(commands=['cancel'])
def cancelar(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, 'canceled')
        bot.state = None


@bot.message_handler(func=lambda msg: bot.state == DESCRIPTION)
def get_descripcion(message):
    if message.chat.type == 'private':
        try:
            desc = str(message.text)
            bot.send_message(message.chat.id, f'Descripcion: {desc}\nIngrese el monto en pesos (CLP):')
            offer['description'] = desc
            bot.state = AMOUNT
        except:
            bot.send_message(message.chat.id, f'Error de ingreso')
            bot.send_message(message.chat.id, f'Ingrese descripcion:')


@bot.message_handler(func=lambda msg: bot.state == AMOUNT)
def get_monto(message):
    if message.chat.type == 'private':
        try:
            amount = int(message.text)
            bot.send_message(message.chat.id, f'Monto: ${amount} CLP\nIngrese direccion origen:')
            offer['amount'] = amount
            bot.state = ORIGIN
        except:
            bot.send_message(message.chat.id, 'Error de ingreso')
            bot.send_message(message.chat.id, f'Ingrese el monto en pesos (CLP):')


@bot.message_handler(func=lambda msg: bot.state == ORIGIN)
def get_origen(message):
    if message.chat.type == 'private':
        try:
            origin = str(message.text)
            bot.send_message(message.chat.id, f'Origen: {origin}\nIngrese direccion Destino:')
            offer['origin'] = origin
            bot.state = DESTINATION
        except:
            bot.send_message(message.chat.id, 'Error de ingreso')
            bot.send_message(message.chat.id, f'Ingrese direccion origen:')


@bot.message_handler(func=lambda msg: bot.state == DESTINATION)
def get_destino(message):
    if message.chat.type == 'private':
        try:
            destination = str(message.text)
            bot.send_message(message.chat.id, f'Destino: {destination}\nIngrese hora de retiro hoy:')
            offer['destination'] = destination
            bot.state = LIMIT_TIME
        except:
            bot.send_message(message.chat.id, 'Error de ingreso')
            bot.send_message(message.chat.id, f'Ingrese direccion Destino:')


@bot.message_handler(func=lambda msg: bot.state == LIMIT_TIME)
def get_tiempo(message):
    if message.chat.type == 'private':
        try:
            limit_time = str(message.text)
            bot.send_message(message.chat.id, f'Hora de retiro: {limit_time}\nIngrese email destinatario:')
            offer['limit_time'] = limit_time
            bot.state = DEST_EMAIL
        except:
            bot.send_message(message.chat.id, 'Error de ingreso')
            bot.send_message(message.chat.id, f'Ingrese hora de retiro hoy:')


@bot.message_handler(func=lambda msg: bot.state == DEST_EMAIL)
def get_tiempo(message):
    if message.chat.type == 'private':
        try:
            dest_email = str(message.text)
            bot.send_message(message.chat.id, f'Email destinatario: {dest_email}')
            offer['dest_email'] = dest_email
            bot.send_message(message.chat.id, f'Confirmar Orden: (si / no)')
            bot.send_message(message.chat.id, f'Descripcion: {offer["description"]}\nValor: {offer["amount"]}\nOrigen: {offer["origin"]}\nDestino: {offer["destination"]}\nRetirar a las: {offer["limit_time"]}\nEmail destinatario: {offer["dest_email"]}')
            bot.state = CONFIRMATION
        except:
            bot.send_message(message.chat.id, 'Error de ingreso')
            bot.send_message(message.chat.id, f'Ingrese email destinatario:')

@bot.message_handler(func=lambda msg: bot.state == CONFIRMATION)
def confirmar_oferta(message):
    if message.chat.type == 'private':
        try:
            resp = str(message.text)
            if resp.lower() == 'si':
                bot.send_message(message.chat.id, f'Orden Confirmada y publicada, gracias.')
                bot.state = None
                today_date = date.today().strftime("%Y-%m-%d")
                add_offer(message.chat.id, message.id, offer, today_date)
                # print(message.chat.id, message.id, offer)

                # print(offer)
            else:
                bot.send_message(message.chat.id, f'Orden descartada.')
                bot.state = None
        except:
            bot.send_message(message.chat.id, 'Error de respuesta')
            bot.send_message(message.chat.id, f'Confirmar Orden: (si / no)')


if __name__ == '__main__':
    print('bot started')
    bot.polling()


