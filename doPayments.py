import requests
import json
import os
import base58

with open('config.json') as json_file:
    config = json.load(json_file)

def main():
    print('reading payment file...')

    with open(config['paymentStorage']) as f:
        payments = json.load(f)

    total = 0
    for pay in payments:
        print('recipient: ' + pay['recipient'] + " amount: " + str(pay['amount'] / pow(10,8)))

        total += pay['amount']

    print('total amount to be paid: ' + str(total / pow(10,8)))

    if config['doPayment'] == 1:
        fee = 10000000 + ((len(payments) / 2) * 10000000)

        if fee < 30000000:
            fee = 30000000

        attachment = base58.b58encode(config['attachmentText'].encode('latin-1'))
        data = {
            "type": 11,
            "sender": config['address'],
            "password": config['keypair'],
            "fee": fee,
            "version": 1,
            "transfers": payments,
            "attachment": attachment
        }

        try:
            res = requests.post(config['node'] + '/transactions/signAndBroadcast', json=data, headers={'X-API-Key': config['apikey']}).json()

            print('payment passed, txid: ' + res['id'])
        except Exception as e:
            print('error during payment!')

main()