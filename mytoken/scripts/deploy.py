from .helper import get_account
from brownie import accounts,network,config,MyToken
from web3 import Web3

def main():
    account = get_account()
    print(f"Account = {account}")
    print(f"Network = {network.show_active()}")
    tx = MyToken.deploy(Web3.toWei(3000,"ether"),{"from": account})
    print(f"Deployed to {MyToken[-1].address}")
    print(f"Balance = {MyToken[-1].balanceOf(account)}")
