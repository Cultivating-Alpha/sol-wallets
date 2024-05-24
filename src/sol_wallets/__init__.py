from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.system_program import transfer
from solana.rpc.types import TxOpts
from spl.token.constants import TOKEN_PROGRAM_ID
from simple_term_menu import TerminalMenu
from spl.token.instructions import (
    transfer_checked,
    get_associated_token_address,
    create_associated_token_account,
)
import json

from sol_wallets.Wallets import wallets


# Initialize the Solana client
client = Client("https://api.mainnet-beta.solana.com")


main_wallet = wallets.main_wallet


def main():
    print(main_wallet.pubkey())
    balance = client.get_balance(main_wallet.pubkey()).value
    print(balance)


# balance = client.get_balance(main_wallet.public_key)["result"]["value"]
# print(balance)


# # Function to equally distribute SOL from the main wallet to sub wallets
# def distribute_sol():
#     # Get the balance of the main wallet
#     balance = client.get_balance(main_wallet.public_key)["result"]["value"]
#     if balance <= 0:
#         print("Main wallet has no SOL to distribute.")
#         return

#     # Calculate the amount to transfer to each sub wallet
#     amount_per_wallet = balance // 25

#     # Create and send the transactions
#     tx = Transaction()
#     for sub_wallet in sub_wallets:
#         tx.add(
#             transfer(
#                 from_pubkey=main_wallet.public_key,
#                 to_pubkey=sub_wallet.public_key,
#                 lamports=amount_per_wallet,
#             )
#         )

#     response = client.send_transaction(tx, main_wallet)
#     print(response)


# # # Function to transfer all SOL from sub wallets back to the main wallet
# # def consolidate_sol():
# #     tx = Transaction()
# #     for sub_wallet in sub_wallets:
# #         balance = client.get_balance(sub_wallet.public_key)["result"]["value"]
# #         if balance > 0:
# #             tx.add(
# #                 transfer(
# #                     from_pubkey=sub_wallet.public_key,
# #                     to_pubkey=main_wallet.public_key,
# #                     lamports=balance,
# #                 )
# #             )

# #     response = client.send_transaction(tx, *sub_wallets)
# #     print(response)


# # # Function to distribute SPL tokens
# # def distribute_spl_tokens(token_mint):
# #     # Get the associated token address for the main wallet
# #     main_token_account = get_associated_token_address(
# #         main_wallet.public_key, token_mint
# #     )
# #     token_balance = client.get_token_account_balance(main_token_account)["result"][
# #         "value"
# #     ]["amount"]

# #     if int(token_balance) <= 0:
# #         print("Main wallet has no SPL tokens to distribute.")
# #         return

# #     amount_per_wallet = int(token_balance) // 25

# #     tx = Transaction()
# #     for sub_wallet in sub_wallets:
# #         sub_wallet_token_account = get_associated_token_address(
# #             sub_wallet.public_key, token_mint
# #         )
# #         tx.add(
# #             create_associated_token_account(
# #                 main_wallet.public_key, sub_wallet.public_key, token_mint
# #             )
# #         )
# #         tx.add(
# #             transfer_checked(
# #                 source=main_token_account,
# #                 dest=sub_wallet_token_account,
# #                 owner=main_wallet.public_key,
# #                 amount=amount_per_wallet,
# #                 decimals=0,
# #                 token_program_id=TOKEN_PROGRAM_ID,
# #                 mint=token_mint,
# #             )
# #         )

# #     response = client.send_transaction(tx, main_wallet)
# #     print(response)


# # # Function to consolidate SPL tokens back to the main wallet
# # def consolidate_spl_tokens(token_mint):
# #     tx = Transaction()
# #     main_token_account = get_associated_token_address(
# #         main_wallet.public_key, token_mint
# #     )

# #     for sub_wallet in sub_wallets:
# #         sub_wallet_token_account = get_associated_token_address(
# #             sub_wallet.public_key, token_mint
# #         )
# #         token_balance = client.get_token_account_balance(sub_wallet_token_account)[
# #             "result"
# #         ]["value"]["amount"]
# #         if int(token_balance) > 0:
# #             tx.add(
# #                 transfer_checked(
# #                     source=sub_wallet_token_account,
# #                     dest=main_token_account,
# #                     owner=sub_wallet.public_key,
# #                     amount=int(token_balance),
# #                     decimals=0,
# #                     token_program_id=TOKEN_PROGRAM_ID,
# #                     mint=token_mint,
# #                 )
# #             )

# #     response = client.send_transaction(tx, *sub_wallets)
# #     print(response)


# # # Function to check for user input and perform actions
# def run():
#     options = [
#         "[d] Distribute Sol",
#         "[a] Transfer all SOL back to main wallet",
#         "[s] Distribute SPL tokens",
#         "[c] Consolidate SPL tokens",
#     ]
#     terminal_menu = TerminalMenu(options)
#     menu_entry_index = terminal_menu.show()
#     print(menu_entry_index)
#     print(options[menu_entry_index])
#     print(f"You have selected {options[menu_entry_index]}!")
#     while True:

#         user_input = (
#             input(
#                 "Press D to distribute SOL, A to transfer all SOL back to the main wallet, S to distribute SPL tokens, C to consolidate SPL tokens: "
#             )
#             .strip()
#             .upper()
#         )
#         if user_input == "D":
#             distribute_sol()
#         elif user_input == "A":
#             consolidate_sol()
#         elif user_input == "S":
#             token_mint = input("Enter the token mint address: ").strip()
#             distribute_spl_tokens(token_mint)
#         elif user_input == "C":
#             token_mint = input("Enter the token mint address: ").strip()
#             consolidate_spl_tokens(token_mint)


# def main() -> int:
#     run()
#     return 0
