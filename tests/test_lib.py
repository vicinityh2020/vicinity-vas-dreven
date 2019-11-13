from ethereum.web3_connection import web3
import json

ABI_PATH = './ethereum/'
ABI_MULTISIG = 'multisig_abi.json'
ABI_EC20 = 'ERC20_abi.json'
ABI_PRICING_FACTORY = 'pricing_factory_abi.json'
ABI_PRICING = 'pricing_abi.json'
DAI_ADDRESS = '0xC4375B7De8af5a38a93548eb8453a498222C4fF2'

with open(ABI_PATH + ABI_MULTISIG) as json_file:
        multisig_abi = json.load(json_file)

with open(ABI_PATH + ABI_EC20) as json_file:
        erc20_abi = json.load(json_file)

with open(ABI_PATH + ABI_PRICING_FACTORY) as json_file:
        pricing_factory_abi = json.load(json_file)

with open(ABI_PATH + ABI_PRICING) as json_file:
        pricing_abi = json.load(json_file)

def get_balance(addr):
    contract = web3.eth.contract(address=DAI_ADDRESS, abi=erc20_abi)
    balance = contract.functions.balanceOf(addr).call()

    return balance

#set_balance('0xA627B30DDD00137ADFA9B74D14213BB77F7352B5E863F9C407BBD58FCCD86C4A', '0x81987B7C6E80160EEB1DEC5D5FACF91F0D314160E702932F1687352AB0A8E787', '0xA627B30DDD00137ADFA9B74D14213BB77F7352B5E863F9C407BBD58FCCD86C4A', '0xacA22D92063494216f526Be56cf403016093B537','0x3d859547ef7e007BE7cE4c51123ba222F4B2Fab2', 5)
def set_balance(privatekey_that_has_DAI, privatekey_provider, privatekey_client, multisig_addr, pricing_addr, ammount):
    dai_contract = web3.eth.contract(address=DAI_ADDRESS, abi=erc20_abi)
    multisig_contract = web3.eth.contract(address=multisig_addr, abi=multisig_abi)

    multisig_balance = get_balance(multisig_addr)

    set_price_to_one(privatekey_provider, pricing_addr)
    sign(privatekey_client, multisig_addr)

    if multisig_balance == ammount:
        return multisig_balance

    elif multisig_balance > ammount:

        provider = web3.eth.account.privateKeyToAccount(privatekey_provider)
        txn = multisig_contract.functions.chargeEndUser((multisig_balance-ammount)//get_price(multisig_addr)).buildTransaction({
            'nonce': web3.eth.getTransactionCount(provider.address),
            'gas': 300000   #164867 + 100000
            })

        txn_signed = web3.eth.account.signTransaction(txn, privatekey_provider)
        txn_hash = web3.eth.sendRawTransaction(txn_signed.rawTransaction)
        web3.eth.waitForTransactionReceipt(txn_hash)

        return get_balance(multisig_addr)

    else:
        account = web3.eth.account.privateKeyToAccount(privatekey_that_has_DAI)
        amount_to_send = ammount-multisig_balance
        txn = dai_contract.functions.transfer(multisig_addr, amount_to_send).buildTransaction({
            'nonce': web3.eth.getTransactionCount(account.address)
            })

        txn_signed = web3.eth.account.signTransaction(txn, privatekey_that_has_DAI)
        txn_hash = web3.eth.sendRawTransaction(txn_signed.rawTransaction)
        web3.eth.waitForTransactionReceipt(txn_hash)

        return get_balance(multisig_addr)



def sign(private_key, multisig_addr):
    contract = web3.eth.contract(address=multisig_addr, abi=multisig_abi)

    client = web3.eth.account.privateKeyToAccount(private_key)

    txn = contract.functions.sign().buildTransaction({
            'nonce': web3.eth.getTransactionCount(client.address),
            'gas': 100000   #34306 + 6000
            })

    txn_signed = web3.eth.account.signTransaction(txn, private_key)
    txn_hash = web3.eth.sendRawTransaction(txn_signed.rawTransaction)
    web3.eth.waitForTransactionReceipt(txn_hash)

def get_price(multisig_addr):
    contract = web3.eth.contract(address=multisig_addr, abi=multisig_abi)
    price_rate = contract.functions.getPrice().call()
    return price_rate

def set_price_to_one(privatekey_provider, pricing_addr):
    #factory = web3.eth.contract(address=pricing_factory_addr, abi=pricing_factory_abi)
    #pricing_addr = factory.functions.getDeployedPricingByProvider(provider.address).call()

    pricing = web3.eth.contract(address=pricing_addr, abi=pricing_abi)
    provider = web3.eth.account.privateKeyToAccount(privatekey_provider)
    txn = pricing.functions.adjustPricing(1).buildTransaction({
            'nonce': web3.eth.getTransactionCount(provider.address),
            'gas': 100000   #34306 + 6000
            })

    txn_signed = web3.eth.account.signTransaction(txn, privatekey_provider)
    txn_hash = web3.eth.sendRawTransaction(txn_signed.rawTransaction)
    web3.eth.waitForTransactionReceipt(txn_hash)


