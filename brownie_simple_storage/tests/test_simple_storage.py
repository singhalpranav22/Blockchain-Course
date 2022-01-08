from brownie import accounts,SimpleStorage

def test_deploy():
    #Arrange
    account = accounts[0] 
    #Act
    simple_storage=SimpleStorage.deploy({"from":account})
    expected = 5
    starting_val = simple_storage.retrieve()
    #assert 
    assert starting_val == expected

def test_update():
    # arrange 
    account = accounts[0]
    simple_storage=SimpleStorage.deploy({"from":account})
    expected = 20 
    tx=simple_storage.store(20,{"from":account})
    assert expected == simple_storage.retrieve()

