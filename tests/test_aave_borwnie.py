from brownie import network,config
from scripts.Aave_borwnie import get_lending_pool , get_asset_price , get_account , approve_erc20


def test_get_asset_price():
    # Arrange / Act
    asset_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    #assert
    assert asset_price > 0

def test_get_lending_pool():
    # Arrange / Act
    lending_pool = get_lending_pool()
    #assert
    assert lending_pool is not None

    
def test_approve_erc20():
    # Arrange 
    account = get_account()
    lending_pool = get_lending_pool()
    amount = 1000000000000000000
    erc20_address=config["networks"][network.show_active()]["weth_token"]
    #Act
    tx=approve_erc20(amount,lending_pool.address,erc20_address,account)
    #assert
    return tx is not True

    



