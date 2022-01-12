from brownie import accounts,network,config

DEV_ENV = ['development','ganache-local','ganache-cli']
FORK_ENV = ['mainnet-fork','mainnet-fork-dev']
def get_account(index=None,id=None):
    if index is not None:
        return accounts[index]
    if network.show_active() in DEV_ENV or network.show_active() in FORK_ENV:
        return accounts[0]
    if id is not None:
        return accounts.load(id)
    return accounts.add(config['wallets']['from_key'])