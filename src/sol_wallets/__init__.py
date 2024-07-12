from tabulate import tabulate
from sol_wallets.Wallet import Wallet
from sol_wallets.Wallets import Wallets
from sol_wallets.Menu import clear, Menu
from sol_wallets.Env import get_key
import asyncio

secret = get_key("MAIN_WALLET")
network = get_key("NETWORK")
user_wallet = Wallet(network=network, secret=secret)


def import_custom_wallet_as_main(wallet, network):
    file_name = f"wallets/{network}-main_wallet.bin"
    print(wallet.keypair)
    with open(file_name, "wb") as binary_file:
        binary_file.write(bytes(wallet.keypair))


# import_custom_wallet_as_main(user_wallet, network)


async def run():
    wallets = Wallets(network)
    menu = Menu(network, wallets, user_wallet)
    await menu.show_menu()
    return


def main():
    # Get the event loop
    loop = asyncio.get_event_loop()

    # Run the async function until completion
    loop.run_until_complete(run())

    # Close the loop
    loop.close()
