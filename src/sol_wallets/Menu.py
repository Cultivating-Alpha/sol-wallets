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

    async def show_menu(self):
        if self.selected_token_account is None:
            self.choose_token()
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
            "[d] Distribute Sol to sub wallets",
            "[ ] Distribute Token to sub wallets",
            "[t] Transfer all SOL back to main wallet",
            "[ ] Transfer all Tokens back to main wallet",
            "",
            "[r] Return money to main user",
            "[f] Fund main bot wallet from user wallet",
            "",
            "[o] Reset saved data",
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
        elif result == "[c] Choose token to transfer":
            self.choose_token()
        elif result == "[d] Distribute Sol to sub wallets":
            await self.distribute_sol(self.selected_token_account.mint)
        elif result == "[ ] Distribute Token to sub wallets":
            await self.distribute_tokens(self.selected_token_account.mint)
        elif result == "[t] Transfer all SOL back to main wallet":
            await self.return_coins(self.selected_token_account.mint)
        elif result == "[ ] Transfer all Tokens back to main wallet":
            await self.return_tokens(self.selected_token_account.mint)
        elif result == "[r] Return money to main user":
            await self.return_amount_to_user(self.selected_token_account.mint)
        elif result == "[f] Fund main bot wallet from user wallet":
            await self.fund_main_wallet(self.selected_token_account.mint, 5)
        elif result == "[o] Reset saved data":
            self.wallets.reset_saved_data()

        # elif menu_entry_index == 6:
        #     self.view_account_balances()
        print()

        if result != "[c] Choose token to transfer":
            user_input = input("Please Enter to continue...")
            print(user_input)

        await self.show_menu()

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
        raw_token_accounts = self.wallets.main_wallet._raw_token_accounts
        if len(raw_token_accounts) == 0:
            print(
                "The main bot's wallet doesn't contain any tokens. Please, send at least one."
            )
            print(
                f"The pubkey of the main bot wallet is: {self.wallets.main_wallet.pubkey()}"
            )
            print(
                f"The secret to use with phantom of the main bot wallet is: {self.wallets.main_wallet.private_key()}"
            )
            print()
            user_input = input("Please Enter to continue...")
            print(user_input)
            return

        options = []
        for account in raw_token_accounts:
            options.append(f"{account.mint} --> {account.name} ({account.symbol})")

        print("Please choose the token (mint-address) to be used")
        terminal_menu = TerminalMenu(
            options, shortcut_key_highlight_style=("fg_green",)
        )
        menu_entry_index = terminal_menu.show()

        if type(menu_entry_index) != int:
            return
        self.selected_token_account = raw_token_accounts[menu_entry_index]

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

    async def distribute_sol(self, mint):
        main_wallet = self.wallets.main_wallet
        balance = self.wallets.main_wallet.get_balance()
        print(f"The main bot has {balance} SOL")

        number_of_sub_wallets = len(self.wallets.sub_wallets)
        sol_per_wallet = balance / number_of_sub_wallets - 0.001
        print(f"We will distribute {sol_per_wallet} SOL for each subwallet")

        for i in tqdm(range(len(self.wallets.sub_wallets))):
            sub = self.wallets.sub_wallets[i]

            await self.action.move_sol(
                main_wallet.keypair, sub.keypair, sol_per_wallet * 1_000
            )
            print()

    async def distribute_tokens(self, mint):
        main_wallet = self.wallets.main_wallet
        token_balance = self.wallets.main_wallet.get_token_balance(
            self.selected_token_account.mint
        )
        print(
            f"The main bot has {token_balance} {self.selected_token_account.mint} balance"
        )

        number_of_sub_wallets = len(self.wallets.sub_wallets)
        token_per_wallet = token_balance / number_of_sub_wallets
        print(f"We will distribute {token_per_wallet} of the selected token")

        for i in tqdm(range(len(self.wallets.sub_wallets))):
            sub = self.wallets.sub_wallets[i]
            main_wallet.transfer_tokens(
                mint, sub.get_token_account(mint).address, token_per_wallet
            )

    async def return_tokens(self, mint):
        solana_price = get_solana_price()
        main_wallet = self.wallets.main_wallet
        for i in tqdm(range(len(self.wallets.sub_wallets))):
            print("--------------------------")
            sub = self.wallets.sub_wallets[i]
            print(sub.pubkey())

            token_balance = sub.get_token_balance(self.selected_token_account.mint)
            print(
                f"The sub wallet  has {token_balance} {self.selected_token_account.mint} balance"
            )
            sub.transfer_tokens(
                mint, main_wallet.get_token_account(mint).address, token_balance
            )

            print()

    async def return_coins(self, mint):
        solana_price = get_solana_price()
        main_wallet = self.wallets.main_wallet
        for i in tqdm(range(len(self.wallets.sub_wallets))):
            print("--------------------------")
            sub = self.wallets.sub_wallets[i]

            balance = sub.get_balance()
            balance_in_usd = balance * get_solana_price()
            if balance_in_usd < 1:
                continue
            balance = balance - 0.001
            print(f"The sub wallet  has {balance} SOL")

            await self.action.move_sol(
                sub.keypair, main_wallet.keypair, balance * 1_000
            )
            print()

    async def return_amount_to_user(self, mint):
        flow = Flow(self.network, self.main_user_wallet, self.wallets.main_wallet)
        await flow.return_amount_to_user()

        print()
        print()

        amount = self.wallets.main_wallet.get_token_balance(mint)
        if amount > 0.0:
            self.wallets.main_wallet.transfer_tokens(
                mint, self.main_user_wallet.get_token_account(mint).address, amount
            )

    async def fund_main_wallet(self, mint, amount):
        flow = Flow(self.network, self.main_user_wallet, self.wallets.main_wallet)
        await flow.refill_target(0.5)

        print()
        print()
        _amount = self.main_user_wallet.get_token_balance(mint)
        if _amount < amount:
            print("Wallet does not contain enough")
            return

        self.main_user_wallet.transfer_tokens(
            mint, self.wallets.main_wallet.get_token_account(mint).address, amount
        )
