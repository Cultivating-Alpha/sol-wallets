import os
from termcolor import colored, cprint
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
from sol_wallets.Env import get_key
from sol_wallets.SPL_Actions import SPL_Actions


from sol_wallets.Helius import get_helius


def clear():
    os.system("cls" if os.name == "nt" else "clear")


class Menu:
    min_usd_balance = 10
    selected_token_account = None

    def __init__(self, network: str, wallets: Wallets, main_user_wallet: Wallet):
        self.network = network
        self.main_user_wallet = main_user_wallet
        self.action = Actions(network)
        self.wallets = wallets
        self.helius = get_helius(network)
        pass

    def show_menu(self):
        clear()
        cprint("MAIN MENU", "red", attrs=["bold"])
        if self.selected_token_account is not None:
            account = self.selected_token_account
            print(
                f"Currently selected token account: {account.symbol} -- {account.mint}"
            )
        print()

        options = [
            "[i] Inspect Bot's main Wallet",
            "[ ] Inspect Bot's sub Wallets",
            # "[ ] Inspect USER Wallets",
            "",
            "[c] Choose token to transfer",
            "",
            "[t] Distribute Token to sub wallets",
            "[s] Distribute Sol to sub wallets",
            "",
            "[a] Transfer all SOL back to main wallet",
            "",
            "[r] Return money to main user",
            "[f] Fund main bot wallet from user wallet",
            # "[v] View my account balances",
            # "[s] Distribute SPL tokens",
            # "[c] Consolidate SPL tokens",
        ]
        terminal_menu = TerminalMenu(
            options, shortcut_key_highlight_style=("fg_green",), skip_empty_entries=True
        )
        menu_entry_index = terminal_menu.show()
        if type(menu_entry_index) != int:
            return
        result = options[menu_entry_index]

        if result == "[i] Inspect Bot's main Wallet":
            self.inspect_main_wallet()
            self.view_account_balances()
        elif result == "[ ] Inspect Bot's sub Wallets":
            self.inspect_sub_wallets()
        elif result == "[ ] Inspect USER Wallets":
            self.inspect_user_wallets()
        elif result == "[c] Choose token to transfer":
            self.choose_token()
        elif result == "[s] Distribute Sol to sub wallets":
            self.distribute_sol()
        elif result == "[a] Transfer all SOL back to main wallet":
            self.return_coins()
        elif result == "[r] Return money to main user":
            self.return_amount_to_user()
        elif result == "[f] Fund main bot wallet from user wallet":
            self.fund_main_wallet()

        # elif menu_entry_index == 6:
        #     self.view_account_balances()
        print()

        if result != "[c] Choose token to transfer":
            user_input = input("Please Enter to continue...")
            print(user_input)

        self.show_menu()

    def inspect_main_wallet(self):
        print("Inspecting the main bot's balance...\n")
        balance = self.wallets.main_wallet.get_balance()

        table = [
            [
                self.wallets.main_wallet.pubkey(),
                balance,
                self.wallets.main_wallet.private_key(),
            ],
        ]

        headers = ["Wallet", "Balance (SOL)", "Private Key"]
        print(tabulate(table, headers=headers, tablefmt="grid"))

    def view_account_balances(self):
        print()
        print(
            f"Fetching token balances for owner: {self.wallets.main_wallet.pubkey()}..."
        )
        self.helius.get_accounts(self.wallets.main_wallet.keypair)

        headers = ["Mint", "Balance", "Name"]
        table = []
        for account in self.helius.accounts:
            # print(f"You have {account.amount} ({account.symbol}) --> {account.name}")
            table.append([account.mint, account.amount, account.name])
        print(tabulate(table, headers=headers, tablefmt="grid"))

    def choose_token(self):
        self.helius.get_accounts(self.wallets.main_wallet.keypair)

        options = []
        for account in self.helius.accounts:
            options.append(f"{account.mint} --> {account.name} ({account.symbol})")
        terminal_menu = TerminalMenu(
            options, shortcut_key_highlight_style=("fg_green",)
        )
        menu_entry_index = terminal_menu.show()

        if type(menu_entry_index) != int:
            return
        self.selected_token_account = self.helius.accounts[menu_entry_index]

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

    def distribute_sol(self):
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
        flow = Flow(self.network, self.main_user_wallet, self.wallets.main_wallet)
        flow.return_amount_to_user()

        source_wallet = self.wallets.main_wallet
        destination_wallet = self.main_user_wallet
        action = Actions(self.network)
        action.move_tokens(source_wallet, destination_wallet, 1)

    def fund_main_wallet(self):
        # flow = Flow(self.network, self.main_user_wallet, self.wallets.main_wallet)
        # flow.refill_target(0.1)

        source_wallet = self.main_user_wallet
        destination_wallet = self.wallets.main_wallet
        action = Actions(self.network)
        action.move_tokens(source_wallet, destination_wallet, 1)
