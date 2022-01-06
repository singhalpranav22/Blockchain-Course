from solcx import compile_standard
import solcx
import json
from web3 import Web3
with open("SimpleStorage.sol","r") as f:
    simple_storage_file = f.read()
solcx.install_solc('0.8.0')
compiled_sol = compile_standard(
     {
     "language" : "Solidity",
     "sources" : {"SimpleStorage.sol" : {"content" : simple_storage_file}},
     "settings" : {
         "outputSelection" : {
             "*" : {"*" : ["abi","metadata","evm.bytecode","evm.sourceMap"]}
         }
     }
     },
     solc_version="0.8.0",

 )
with open("compiled_code.json","w") as f:
    json.dump(compiled_sol, f)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
# connecting rinkbey blockchain using infura
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/9d5669beb67742cd86cd37258d8a3a70"))
chain_id = 4
my_address = "0x752C222B61a0b420B979103Db733522Cc2dcE15e"
private_key = "0x21fcde96703d87e1815ed7574a05905a2c6cf983e88954b1bb6e4cff5f4908b1"

# create contract in python 
SimpleStorage = w3.eth.contract(abi=abi,bytecode=bytecode)
# get the latest transaction 
nonce = w3.eth.getTransactionCount(my_address)
# steps:
# 1. create the transaction
# 2. sign the transaction
# 3. send the transaction
transaction = SimpleStorage.constructor().buildTransaction({"chainId":chain_id,"nonce":nonce,"from":my_address,"gasPrice":w3.eth.gas_price})
signedTxn = w3.eth.account.signTransaction(transaction,private_key)
print("Deploying contract.....")
tx_hash = w3.eth.sendRawTransaction(signedTxn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# working with the contract  
# contract abi   
# contract address 
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)
print(simple_storage.functions.retrieve().call())
nonce = w3.eth.getTransactionCount(my_address)
print("Updating the contract.....")
store_transation = simple_storage.functions.store(20).buildTransaction({"chainId":chain_id,"nonce":nonce,"from":my_address,"gasPrice":w3.eth.gas_price})
signedTxn = w3.eth.account.signTransaction(store_transation,private_key)
tx_hash = w3.eth.sendRawTransaction(signedTxn.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(simple_storage.functions.retrieve().call())
