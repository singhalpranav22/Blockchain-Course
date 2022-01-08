from brownie import accounts,network,config,MockV3Aggregator,FundMe
from scripts.helper import get_account,deploy_mock

def fund():
    fundMe = FundMe[-1]
    account = get_account()
    entranceFee = fundMe.getEntranceFee()
    print(f"The current entranceFeeprice is {entranceFee}")
    print("Funding......")
    fundMe.fund({"from":account, "value":entranceFee})

def withdraw():
    fundMe = FundMe[-1]
    account = get_account()
    print("Withdrawing......")
    fundMe.withdraw({"from":account})

def main():
    fund()
    withdraw()
