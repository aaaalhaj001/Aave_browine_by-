from brownie import network,config,interface
from scripts.helpful_scripts import get_account
from scripts.get_Weth import get_weth
from web3 import Web3

amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    lending_pool = get_lending_pool()
    approve_tx = approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing...")
    tx = lending_pool.deposit(erc20_address,amount, account.address,0,{"from":account})
    tx.wait(1)
    print("Deposited!")
    
    borrowable_eth,total_debt_eth=get_borrowable_data(lending_pool,account)

    print("Let's borrow!")
    
    
    dai_eth_price= get_asset_price(config["networks"][network.show_active()]["dai_eth_price_feed"])
    
    amont_dai_to_borrow=(1/dai_eth_price)*(borrowable_eth*0.95)

    dai_address=config["networks"][network.show_active()]["dai_token"]
    borrow_tx=lending_pool.borrow(dai_address,Web3.toWei(amont_dai_to_borrow,"ether"),1,
    0,
    account.address,
    {"from":account})
    borrow_tx.wait(1)
    print("we borrow some DAI")
    get_borrowable_data(lending_pool,account)
    repay_all(amount, lending_pool ,account )
    print("you just deposited borrow and repayed with Python , Aave , borwine ,and Chainlink")


def repay_all(amount, lending_pool ,account ):
   approve_erc20(Web3.toWei(amount,"ether"),lending_pool,config["networks"][network.show_active()]["dai_token"],account,)
   repay_tx = lending_pool.repay( config["networks"][network.show_active()]["dai_token"],amount, 1,account.address,{"from": account},)
   repay_tx.wait(1)
   print("Repay!!!")


def get_asset_price(price_feed_address):
    dai_eth_price_feed=interface.AggregatorV3Interface(price_feed_address)
    last_price=dai_eth_price_feed.latestRoundData()[1]
    coverted_last_price=Web3.fromWei(last_price,"ether")
    print(f"The DAI/ETH Price is {coverted_last_price}")
    return float(last_price)






def get_borrowable_data(lending_pool,account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor) =lending_pool.getUserAccountData(account.address)
    available_borrow_eth=Web3.fromWei( available_borrow_eth,"ether")
    total_collateral_eth=Web3.fromWei(total_collateral_eth,"ether")
    total_debt_eth=Web3.fromWei( total_debt_eth,"ether")
    print(f"you have {total_collateral_eth} worth of ETH deposited.")
    print(f"you have {total_debt_eth} worth of ETH deposited.")
    print(f"you can borrow{available_borrow_eth} worth of ETH ")
    return (float(available_borrow_eth), float(total_debt_eth))




def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender,amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx

def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

