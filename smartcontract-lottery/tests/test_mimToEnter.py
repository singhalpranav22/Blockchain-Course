from brownie import accounts,Lottery  
from web3 import Web3

def test_lottery():
    account = accounts[0]
    lotteryContact=Lottery.deploy('0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419',{'from':account})
    assert Web3.toWei(0.0154, 'ether') < lotteryContact.getEntranceFee()
    assert Web3.toWei(0.0159, 'ether') > lotteryContact.getEntranceFee()
