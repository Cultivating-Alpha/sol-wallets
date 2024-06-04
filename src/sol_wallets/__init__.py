from sol_wallets.Wallet import Wallet
from sol_wallets.Wallets import Wallets
from sol_wallets.Menu import clear, Menu
from sol_wallets.Env import get_key

sample_wallets = {
    "main": "BuouBWx5AVadDXzKFwBxaAxUnT3K5H6rRQmtAeCYGyLM",
    "devnet": "51iAWLX4niXKE2LFUCKDH1CJSrEqD1z5owcPsZpCUfGq",
}


secret = get_key("MAIN_WALLET")
network = get_key("NETWORK")
devnet_user_wallet = Wallet(network=network, secret=secret)


async def run():
    # clear()
    wallets = Wallets(network)
    menu = Menu(network, wallets, devnet_user_wallet)
    await menu.show_menu()
    return


import asyncio


def main():
    # Get the event loop
    loop = asyncio.get_event_loop()

    # Run the async function until completion
    loop.run_until_complete(run())

    # Close the loop
    loop.close()
