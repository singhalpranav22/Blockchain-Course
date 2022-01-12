from brownie import accounts,network,config,Lottery,MockV3Aggregator,VRFCoordinatorMock,Contract,LinkToken

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

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token" : LinkToken
}
def get_contract(contract_name):
    """If you want to use this function, go to the brownie config and add a new entry for
    the contract that you want to be able to 'get'. Then add an entry in the variable 'contract_to_mock'.
    You'll see examples like the 'link_token'.
        This script will then either:
            - Get a address from the config
            - Or deploy a mock to use for a network that doesn't have it
        Args:
            contract_name (string): This is the name that is refered to in the
            brownie config and 'contract_to_mock' variable.
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            Contract of the type specificed by the dictonary. This could be either
            a mock or the 'real' contract on a live network.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in DEV_ENV:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        try:
            contract_address = config["networks"][network.show_active()][contract_name]
            contract = Contract.from_abi(
                contract_type._name, contract_address, contract_type.abi
            )
        except KeyError:
            print(
                f"{network.show_active()} address not found, perhaps you should add it to the config or deploy mocks?"
            )
            print(
                f"brownie run scripts/deploy_mocks.py --network {network.show_active()}"
            )
    return contract

DECIMALS = 8
INITIAL_VALUE = 300000000000
def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    print("Deploying Mock Price Feed...")
    mock_price_feed = MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    print(f"Deployed to {mock_price_feed.address}")
    print("Deploying Mock Link Token...")
    link_token = LinkToken.deploy({"from": account})
    print("Deploying Mock VRFCoordinator...")
    mock_vrf_coordinator = VRFCoordinatorMock.deploy(
        link_token.address, {"from": account}
    )
    print(f"Deployed to {mock_vrf_coordinator.address}")

def fundWithLink(contract_address,account=None,link_token=None,amount=10**17):
    if account is None:
        account = get_account()
    if link_token is None:
        link_token = get_contract("link_token")
    tx=link_token.transfer(contract_address,amount,{"from":account})
    tx.wait(1)
    print("Funded contract with LINK!")
    return tx


