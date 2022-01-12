from brownie import accounts,Lottery,config,network
from .helper import get_account,get_contract,fundWithLink
import time
def deploy_lottery():
    account = get_account()
    Lottery.deploy(get_contract("eth_usd_price_feed").address,get_contract("vrf_coordinator"),get_contract("link_token"),config["networks"][network.show_active()]["fee"],config["networks"][network.show_active()]["key_hash"],{'from':account})
    lottery = Lottery[-1]
    print(f"Deployed to {lottery.address}")

def startLottery():
    account = get_account()
    lottery = Lottery[-1]
    tx=lottery.startLottery({'from':account})
    tx.wait(1)
    print("Started the lottery!")
    

def enterLottery():
    account = get_account()
    lottery = Lottery[-1]
    tx=lottery.enter({'from':account,"value": lottery.getEntranceFee()+1000000})
    tx.wait(1)
    print("Entered the lottery with account = "+str(account))


def endLottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fundWithLink(lottery.address)
    tx.wait(1)
    end_tx = lottery.endLottery({'from':account})
    end_tx.wait(1)
    time.sleep(300)
    print(f"Ended lottery with winner = {lottery.recentWinner()}")

    

def main():
    deploy_lottery()
    startLottery()
    enterLottery()
    endLottery()
