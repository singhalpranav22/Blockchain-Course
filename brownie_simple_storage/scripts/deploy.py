from brownie import accounts,config,SimpleStorage,network
import os
def deploy_simple_storage():
    # account = accounts.add(config["wallets"]["from_key"])
    account = getAccount()
    simple_storage=SimpleStorage.deploy({'from': account})
    print("SimpleStorage address:",simple_storage.address)
    stored = simple_storage.retrieve()
    print(stored)  
    tx = simple_storage.store(66,{'from': account})
    tx.wait(1)
    stored = simple_storage.retrieve()
    print(stored)

def getAccount():
    if network.show_active()=='development':
        return accounts[0] 
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()