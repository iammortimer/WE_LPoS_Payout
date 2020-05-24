import requests
import json
import os
import base58
import time

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

    #do actual payment
    if config['doPayment'] == 1:
        url = '/transactions/signAndBroadcast'
    else:
        url = '/transactions/sign'
        print('doing testpayment, no funds are actually transferred...')

    fee = 10000000 + ((len(payments)+1 / 2) * 10000000)

    if fee < 30000000:
        fee = 30000000

    # if fee > 30000000 and fee < 60000000:
    #     fee = 60000000

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

    paymentDone = False
    try:
        res = requests.post(config['node'] + url, json=data, headers={'X-API-Key': config['apikey']}).json()

        print('payment passed, txid: ' + res['id'])
        paymentDone = True
    except Exception as e:
        print('error during payment!')
        print('failed with this transfer data: ')
        print(data)
        print('result was: ')
        print(res)

    #move remaining balance to other account
    if paymentDone and config['moveRemainder'] == 1:
        time.sleep(120)
        balance = requests.get(config['node'] + '/addresses/balance/' + config['address']).json()['balance']
        print('remaining balance after payout: ' + str(balance / pow(10,8)))

        print('moving remaining balance to: ' + config['addressCosts'])
        fee = 10000000
        amount = balance - fee
        data = {
            "type": 4,
            "version": 2,
            "sender": config['address'],
            "password": config['keypair'],
            "recipient": config['addressCosts'],
            "amount": round(amount),
            "fee": fee
        }
        try:
            res = requests.post(config['node'] + url, json=data, headers={'X-API-Key': config['apikey']}).json()

            print('payment passed, txid: ' + res['id'])
        except Exception as e:
            print('error during payment!')
            print('failed with this transfer data: ')
            print(data)
            print('result was: ')
            print(res)


main()