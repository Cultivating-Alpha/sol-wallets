from solana.transaction import Transaction
from solders.system_program import transfer, TransferParams
from sol_wallets.Client import get_client
from solders.keypair import Keypair
from solders.hash import Hash
from solders.message import MessageV0
from solders.transaction import VersionedTransaction
from solders.compute_budget import set_compute_unit_price

from sol_wallets.Helius import get_helius
from sol_wallets.SPL_Actions import SPL_Actions
from sol_wallets.Wallet import Wallet


class Actions:
    def __init__(self, network="devnet"):
        self.client = get_client(network)
        self.helius = get_helius(network)

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

    def move_tokens(self, source_wallet: Wallet, destination_wallet: Wallet, amount):
        print(destination_wallet.keypair.pubkey())
        source_accounts = self.helius.get_accounts(source_wallet.keypair)
        destination_accounts = self.helius.get_accounts(destination_wallet.keypair)
        print(source_accounts)
        print(destination_accounts)
        missing_accounts = SPL_Actions.find_missing_accounts(
            source_accounts, destination_accounts
        )
        print(missing_accounts)

        # dest_key = spl_client.create_account(Pubkey.from_string(sub))
        return
        # print("There are no missing accounts")
        # print(destination_accounts)

        for acc in source_accounts:
            balance = acc.get_balance()
            spl_action = SPL_Actions(acc, source_wallet, acc.token_account)

            amount = acc.format_amount(balance)

            destination_acc = None
            print(acc.mint)
            for _acc in destination_accounts:
                print(_acc.mint)
                if _acc.mint == acc.mint:
                    destination_acc = _acc
                    break
            print(destination_acc)
            if destination_acc is not None:
                # print(destination_acc)
                # print(destination_acc.address)
                # print(destination_acc.pubkey)
                # destination_token_accounts = acc.token_account
                spl_action.transfer_token_to_address(destination_acc.pubkey, amount)
            break
