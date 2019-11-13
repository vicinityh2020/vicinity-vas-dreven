import json
import os
from web3_connection import web3
from importantVariables import factoryAddress, build_path


# fetch pricing factory abi result from compilation
os.chdir(build_path)
with open('PricingFactory.json') as json_file:
    data = json.load(json_file)

abi = data['abi']

# instantiate contract
pricingFactoryContractAddress = web3.toChecksumAddress(factoryAddress)
contract = web3.eth.contract(address=pricingFactoryContractAddress, abi=abi)


def readDeployedPricings(contract):
    return contract.functions.getAllDeployedPricings().call()


def readDeployedPricing(contract, provider):
    return contract.functions.getDeployedPricingByProvider(provider).call()


def readNrOfDeployedPricings(contract):
    return contract.functions.getNrOfDeployedPricings().call()


print("All existing contracts: " + str(readDeployedPricings(contract)))
print("Provider " + web3.eth.accounts[0] + " owns the pricing " +
      str(readDeployedPricing(contract, web3.eth.accounts[0])))
print("Existing pricing contracts: " + str(readNrOfDeployedPricings(contract)))
