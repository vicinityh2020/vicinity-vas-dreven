from web3 import Web3


infura_url = 'https://kovan.infura.io/v3/3e3326511666419484f6225ae39a541d'
web3 = Web3(Web3.HTTPProvider(infura_url))

# must return true if web3 connection was succeesfull
if web3.isConnected():
    print("Web3 connection was successful!")
else:
    print("Web3 connection was not successful!")
