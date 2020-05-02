# WE_LPoS_Payout
Waves Enterprise payout script for lessors

Based on <https://github.com/jansenmarc/WavesLPoSDistributer> but rewritten in Python.

## Installation
This script uses Pyton version 3.

To install the required dependencies please run the following command:
```
pip3 install -r requirements.txt
```
or 
```
pip install -r requirements.txt
```

## Configuration
Now we need to configure the settings for the script. For this we need to edit the config.json file:
```
{
    "node": enter your node address, for example: "http://localhost:6862",
    "address" : enter the WE address of your node,
    "addressCosts" : enter the WE address where you wawnt to move remaining funds to,
    "startBlock" : starting block of the calculations (usually the endBlock from the last time it was run or 1 if it's the first time),
    "endBlock" : ending block for the calculations to run to (enter 0 if you want to use the current last block),
    "apikey" : enter your api key for use with swagger,
    "keypair" : enter your keypair password to be able to do transfers,
    "percentageOfFeesToDistribute" : percentage of fees you want to distribute to your lessers, 
    "minAmounttoPay" : minimum amount to pay to lessors,
    "blockStorage": filename to store the processed blocks in,
    "paymentStorage": filename to store the payments in,
    "attachmentText" : text you want to attach to the payment to your lessors,
    "doPayment" : enter 0 or 1, 0 will do a testrun of the payments, 1 will do the actual payments,
    "moveRemainder" : enter 0 or 1, 0 will do nothing, 1 will move remaining funds after the payout to the address in addressCosts
}
```

Here's an example of a filled out file:
```
{
    "node": "http://192.168.16.236:6862",
    "address" : "3NmDCwY6oi2yu7EMDNqmnJvy7ZLAK76hFgy",
    "addressCosts" : "3Nsowj5JUjdPwQUMhfbjq4xEGTThBsnBfvE",
    "startBlock" : 1,
    "endBlock" : 0,
    "apikey" : "thisismyapikey",
    "keypair" : "thisismykeypairpassword",
    "percentageOfFeesToDistribute" : 90, 
    "minAmounttoPay" : 0,
    "blockStorage": "blocks.json",
    "paymentStorage": "payments.json",
    "attachmentText" : "thank you for supporting Morty's node",
    "doPayment" : 1,
    "moveRemainder" : 1
}
```

## Execution
When you finished editing the config.json you are ready to run the script. This consists out of 2 (or 3) parts:
1. Create the payment file.
2. (this is optional) Do a testrun of the actual payment.
3. Do the payment

To creat the payment file you need to execute the calcPayments.py:
```
python calcPayments.py
```
It will show you what's happening. The saving of the block file could take a few minutes, so don't worry if it seems nothing is happening when it says 'saving blockfile...'.

Once the script is completed (it will show you some statistics about this run, like forged blocks, number of leases, stuff like that) you can either do a testrun of the payment (set the doPayment in config.json to 0) or do the actual payment (set the doPayment in config.json to 1) by executing the following command:
```
python doPayments.py
```

And your done. 

After your first run make sure you set the startBlock in the config.json to the correct block you left off in your previous run.
