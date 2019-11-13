from web3_connection import web3
from importantVariables import build_path
import json
import os

# use for ganache only
web3.eth.defaultAccount = web3.eth.accounts[0]


def deploy_contract(contract_json):
    # Define contract with compiled json contract
    contract = web3.eth.contract(
        abi=contract_json['abi'],
        bytecode=contract_json['bin']
    )

    # Sign transaction with default account from ganache
    # Get transaction hash from deployed contract
    tx_hash = contract.constructor().transact()

    # Get tx receipt, print and return contract address
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print('Contract deployed to: ' + tx_receipt['contractAddress'])
    return tx_receipt['contractAddress']


# get compiled contract json from /build dir
os.chdir(build_path)
with open('PricingFactory.json') as json_file:
    data = json.load(json_file)

# exec deploy
deploy_contract(data)
