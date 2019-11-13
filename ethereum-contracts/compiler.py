import os
import json
import shutil
from os import listdir, path
from solcx import compile_files

path_to_contracts = "./contracts/"
array_of_contracts_to_compile = []
c_json = ""

# gets all contracts .sol in contracts dir
files = [f for f in listdir(path_to_contracts) if path.isfile(path.join(path_to_contracts, f))]

for f in files:
    if f.split('.')[1] == 'sol':
        array_of_contracts_to_compile.append(path_to_contracts+f)

#   deletes dir build + its files and creates an empty new one
if os.path.exists("build"):
    shutil.rmtree('build')
os.mkdir('build')


# compiles all contracts in folder ./contracts
compiled_contracts = compile_files(array_of_contracts_to_compile)

# for each compiled contract, create json file inside build directory
# contains abi and bytecode of each contract
for c in compiled_contracts:
    c_json = json.dumps(compiled_contracts[c],  indent=2)
    f = open(r"./build/" + str(c.split(':')[1]) + ".json", "w+")
    f.write(c_json)

