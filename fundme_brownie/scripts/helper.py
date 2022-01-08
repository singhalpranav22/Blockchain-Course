from brownie import accounts,network,config,MockV3Aggregator
DEV_ENV = ['development','ganache-local','mainnet-fork-dev']
def get_account():
    print(network.show_active())
    if network.show_active() in DEV_ENV:
        return accounts[0]  
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mock():
    print("Deploying mock on development network......")
    if len(MockV3Aggregator)>0:
        print("Mock already deployed")
    else:
        print("Deploying mock on development network......")
        MockV3Aggregator.deploy(8,200000000000,{'from':get_account()})