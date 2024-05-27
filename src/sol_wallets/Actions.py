from solana.transaction import Transaction
from solders.system_program import transfer, TransferParams
from sol_wallets.Client import get_client
from solders.keypair import Keypair
from solders.hash import Hash
from solders.message import MessageV0
from solders.transaction import VersionedTransaction
from solders.compute_budget import set_compute_unit_price


class Actions:
    def __init__(self, network="devnet"):
        self.client = get_client(network)

    def move_sol(self, sender: Keypair, receiver: Keypair, amount):
        print(
            f"Transfering {amount / 1_000} between:\nSender: {sender.pubkey()}\nReceiver: {receiver.pubkey()}"
        )

        ix = transfer(
            TransferParams(
                from_pubkey=sender.pubkey(),
                to_pubkey=receiver.pubkey(),
                lamports=int(1_000_000 * amount),
            )
        )
        txn = Transaction(fee_payer=sender.pubkey()).add(ix)
        self.client.send_transaction(txn, sender)


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


# # Function to transfer all SOL from sub wallets back to the main wallet
# def consolidate_sol():
#     tx = Transaction()
#     for sub_wallet in sub_wallets:
#         balance = client.get_balance(sub_wallet.public_key)["result"]["value"]
#         if balance > 0:
#             tx.add(
#                 transfer(
#                     from_pubkey=sub_wallet.public_key,
#                     to_pubkey=main_wallet.public_key,
#                     lamports=balance,
#                 )
#             )

#     response = client.send_transaction(tx, *sub_wallets)
#     print(response)


# # Function to distribute SPL tokens
# def distribute_spl_tokens(token_mint):
#     # Get the associated token address for the main wallet
#     main_token_account = get_associated_token_address(
#         main_wallet.public_key, token_mint
#     )
#     token_balance = client.get_token_account_balance(main_token_account)["result"][
#         "value"
#     ]["amount"]

#     if int(token_balance) <= 0:
#         print("Main wallet has no SPL tokens to distribute.")
#         return

#     amount_per_wallet = int(token_balance) // 25

#     tx = Transaction()
#     for sub_wallet in sub_wallets:
#         sub_wallet_token_account = get_associated_token_address(
#             sub_wallet.public_key, token_mint
#         )
#         tx.add(
#             create_associated_token_account(
#                 main_wallet.public_key, sub_wallet.public_key, token_mint
#             )
#         )
#         tx.add(
#             transfer_checked(
#                 source=main_token_account,
#                 dest=sub_wallet_token_account,
#                 owner=main_wallet.public_key,
#                 amount=amount_per_wallet,
#                 decimals=0,
#                 token_program_id=TOKEN_PROGRAM_ID,
#                 mint=token_mint,
#             )
#         )

#     response = client.send_transaction(tx, main_wallet)
#     print(response)


# # Function to consolidate SPL tokens back to the main wallet
# def consolidate_spl_tokens(token_mint):
#     tx = Transaction()
#     main_token_account = get_associated_token_address(
#         main_wallet.public_key, token_mint
#     )

#     for sub_wallet in sub_wallets:
#         sub_wallet_token_account = get_associated_token_address(
#             sub_wallet.public_key, token_mint
#         )
#         token_balance = client.get_token_account_balance(sub_wallet_token_account)[
#             "result"
#         ]["value"]["amount"]
#         if int(token_balance) > 0:
#             tx.add(
#                 transfer_checked(
#                     source=sub_wallet_token_account,
#                     dest=main_token_account,
#                     owner=sub_wallet.public_key,
#                     amount=int(token_balance),
#                     decimals=0,
#                     token_program_id=TOKEN_PROGRAM_ID,
#                     mint=token_mint,
#                 )
#             )
#     response = client.send_transaction(tx, *sub_wallets)
#     print(response)
