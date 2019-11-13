from web3_connection import web3
from importantVariables import factoryAddress, build_path
import json
import os


def deployPricingCotract(factoryContract, account_address, account_privateKey, priceValue):
    nonce = web3.eth.getTransactionCount(account_address)
    txn_dict = factoryContract.functions.createPricing(priceValue).buildTransaction({
        'chainId': 4,
        'gas': 1000000,
        'gasPrice': web3.toWei('40', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = web3.eth.account.signTransaction(
        txn_dict, private_key=account_privateKey)
    result = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(result)

    return tx_receipt


# define account to deploy address
account_deployer = web3.eth.accounts[1]  # ganache account
pKey = '193e73481536a1ba3a601b38b41850ed4ffe8220afd777224fc205b3d4f5184a'

# fetch pricing factory abi result from compilation
os.chdir(build_path)
with open('PricingFactory.json') as json_file:
    data = json.load(json_file)

abi = data['abi']


# build pricingfactory from deployed address
pricingFactoryContractAddress = web3.toChecksumAddress(factoryAddress)
factoryContract = web3.eth.contract(
    address=pricingFactoryContractAddress, abi=abi)

# deploy pricing
deployPricingCotract(factoryContract, account_deployer, pKey, 2)

print("Pricing contract deployed to: {}".format(
    factoryContract.functions.getAllDeployedPricings().call()[len(
        factoryContract.functions.getAllDeployedPricings().call())-1]
))
