from brownie import accounts,config,SimpleStorage
def read_contact():
    # print(SimpleStorage[0])
    simple_storage = SimpleStorage[-1]
    # brownie already knows the abi as it is required to interact with the contract
    print(simple_storage.retrieve())
    pass 

def main():
    read_contact()