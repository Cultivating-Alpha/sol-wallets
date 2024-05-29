import os
from simple_term_menu import TerminalMenu
from sol_wallets.Actions import Actions
from sol_wallets.Wallet import Wallet
from sol_wallets.Wallets import Wallets
from sol_wallets.Flow import Flow
from sol_wallets.sol_price import get_solana_price
from sol_wallets.Helpers import round_value
from tqdm import tqdm
import math
from tabulate import tabulate

from sol_wallets.Helius import Helius
from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv()


sample_wallets = {
    "main": "BuouBWx5AVadDXzKFwBxaAxUnT3K5H6rRQmtAeCYGyLM",
    "devnet": "51iAWLX4niXKE2LFUCKDH1CJSrEqD1z5owcPsZpCUfGq",
}

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
API_KEY = config["HELIUS_KEY"]
OWNER = config["MAIN_WALLET"]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


class Runner:
    min_usd_balance = 10

    def __init__(self, network: str, wallets: Wallets, main_user_wallet: Wallet):
        self.network = network
        self.main_user_wallet = main_user_wallet
        self.action = Actions(network)
        self.wallets = wallets
        pass

    def menu(self):
        options = [
            "[i] Inspect Bot's main Wallet",
            "[s] Inspect Bot's sub Wallets",
            "[d] Distribute Sol to sub wallets",
            "[a] Transfer all SOL back to main wallet",
            "[r] Return money to main user",
            "[f] Fund main bot wallet from user wallet",
            "[v] View my account balances",
            # "[s] Distribute SPL tokens",
            # "[c] Consolidate SPL tokens",
        ]
        terminal_menu = TerminalMenu(
            options, title="Main Menu", shortcut_key_highlight_style=("fg_green",)
        )
        menu_entry_index = terminal_menu.show()
        if menu_entry_index == 0:
            self.inspect_main_wallet()
        elif menu_entry_index == 1:
            self.inspect_sub_wallets()
        elif menu_entry_index == 2:
            self.distribute()
        elif menu_entry_index == 3:
            self.return_coins()
        elif menu_entry_index == 4:
            self.return_amount_to_user()
        elif menu_entry_index == 5:
            self.fund_main_wallet()
        elif menu_entry_index == 6:
            self.view_account_balances()
        print()

        user_input = input("Please Enter to continue...")
        print(user_input)

        clear()
        self.menu()

    def view_account_balances(self):
        print("Fetching token balances for owner: {OWNER}")
        helius = Helius(API_KEY)
        helius.get_accounts(OWNER)

        headers = ["Coin", "Balance", "Name"]
        table = []
        for account in helius.accounts:
            # print(f"You have {account.amount} ({account.symbol}) --> {account.name}")
            table.append([account.symbol, account.amount, account.name])
        print(tabulate(table, headers=headers, tablefmt="grid"))

    def inspect_sub_wallets(self):
        print("Inspecting the sub wallets...\n")
        table = []
        for i in tqdm(range(len(self.wallets.sub_wallets))):
            wallet = self.wallets.sub_wallets[i]
            table.append(
                [str(wallet.pubkey()), wallet.get_balance(), wallet.private_key()]
            )

        headers = ["Wallet", "Balance (SOL)", "Private Key"]
        print(tabulate(table, headers=headers, tablefmt="grid"))

    def inspect_main_wallet(self):
        print("Inspecting the main bot's balance...\n")
        balance = self.wallets.main_wallet.get_balance()

        table = [
            [wallets.main_wallet.pubkey(), balance, wallets.main_wallet.private_key()],
        ]

        headers = ["Wallet", "Balance (SOL)", "Private Key"]
        print(tabulate(table, headers=headers, tablefmt="grid"))

    def distribute(self):
        main_wallet = self.wallets.main_wallet
        balance = self.wallets.main_wallet.get_balance()
        solana_price_usd = get_solana_price()
        balance_in_usd = balance * solana_price_usd
        print(f"The main bot has {balance} SOL ({balance_in_usd:.2f}$)")
        if balance_in_usd < self.min_usd_balance:
            print("The balance is less than the min required. Please top up first!")
            return

        sub_wallets = self.wallets.sub_wallets
        count = len(sub_wallets)
        amount_per_wallet = round_value(balance / count, 0.001)
        print(f"We have {count} wallets. Each will receive {amount_per_wallet} SOL")
        print("=============================================")
        print()

        for i in tqdm(range(len(self.wallets.sub_wallets))):
            sub = self.wallets.sub_wallets[i]

            self.action.move_sol(
                main_wallet.keypair, sub.keypair, amount_per_wallet * 1_000
            )
            print()

    def return_coins(self):
        main_wallet = self.wallets.main_wallet
        for i in tqdm(range(len(self.wallets.sub_wallets))):
            sub = self.wallets.sub_wallets[i]
            balance = sub.get_balance()

            money_to_return = math.floor(balance * 1_000)
            if money_to_return != 0:
                print(f"wallet {sub.pubkey()} has {balance} SOL")
                balance_to_return = balance - 0.001
                self.action.move_sol(
                    sub.keypair, main_wallet.keypair, balance_to_return * 1_000
                )
                print()

    def return_amount_to_user(self):
        flow = Flow(self.network, self.main_user_wallet, wallets.main_wallet)
        flow.return_amount_to_user()

    def fund_main_wallet(self):
        flow = Flow(self.network, self.main_user_wallet, wallets.main_wallet)
        flow.refill_target(0.1)


secret = "27FBSJH6NZipnEM2M1PNDV5P9wAvnr9kca2Ds4ipMXo7nLTK5W6DSJBPZccQoq9t17hM74evEBTyQAhogSFj4Gso"
devnet_user_wallet = Wallet(network="devnet", secret=secret)


wallets = Wallets("devnet")


def main():
    clear()
    wallets = Wallets("devnet")
    runner = Runner("devnet", wallets, devnet_user_wallet)

    # runner.distribute()
    # runner.return_coins()
    runner.menu()
    # flow.return_amount_to_user()
    return
