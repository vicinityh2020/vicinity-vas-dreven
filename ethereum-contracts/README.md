# Ethereum smart-contracts

This repo serves solely the purpose for the smart-contracts compilation!

**Smart-contract ---=====COMPILER====--->> ABI + Bytecode**

Contract **ABI** and **Bytecode** are necessary to deploy and interact with a contract. All contract structures are developed in path=./contracts/ and all consequent ABI and bytecodes of each contract are saved in path=./build/

compiler.py is a python3 compiler that gets __EVERY__ contract in ./contracts/, compile each and save its resulting ABI+Bytecode in a .json format file. Each JSON files contain keys 'abi' and 'bin' respectively for the contract ABI and Bytecode

solc library compiler version => py-solc-x (0.5.0)
solidity compiler version => v0.5.11

## Installation


```shell
$ python3.7 -m virtualenv MyEnv
$ . MyEnv/bin/activate
$ pip install -r requirements.txt
$ python3 -m solcx.install v0.5.11
```
## Run
```shell
$ python3 compiler.py
```

## Output
JSON file for each contract in ./contracts saved in ./build