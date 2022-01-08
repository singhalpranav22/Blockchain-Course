from brownie import accounts,FundMe,config,network,MockV3Aggregator
from scripts.helper import get_account,deploy_mock

DEV_ENV = ['development','ganache-local']
def deploy_fund_me():
    print(network.show_active())
    account = get_account()
    chainLinkAddress = None
    # check which network is present, if not present, deploy mock on development network   
    if network.show_active() not in DEV_ENV:
        chainLinkAddress = config['networks'][network.show_active()]['eth_usd_price_feed']
    else:
        deploy_mock()
        chainLinkAddress = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(chainLinkAddress,{'from':account}) 
    print("Current price="+str(fund_me.getPrice()))

    
def main():
    deploy_fund_me()