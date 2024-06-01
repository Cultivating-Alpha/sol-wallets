from solana.transaction import Transaction
from solders.system_program import transfer, TransferParams
from sol_wallets.Client import get_client, get_async_client
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
        self.async_client = get_async_client(network)
        self.helius = get_helius(network)

    async def move_sol(self, sender: Keypair, receiver: Keypair, amount):
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
        res = await self.async_client.send_transaction(txn, sender)
        print(res)

    def make_sure_account_exist(
        self, source_wallet: Wallet, destination_wallet: Wallet
    ):
        source_accounts = self.helius.get_accounts(source_wallet.keypair)
        destination_accounts = self.helius.get_accounts(destination_wallet.keypair)

        missing_accounts = SPL_Actions.find_missing_accounts(
            source_accounts, destination_accounts
        )

        for acc in missing_accounts:
            spl_action = SPL_Actions(acc, source_wallet.keypair, acc.token_account)
            addr = spl_action.create_account(destination_wallet.pubkey())
            print(addr)

    def move_tokens(self, source_wallet: Wallet, destination_wallet: Wallet, amount):
        self.make_sure_account_exist(source_wallet, destination_wallet)

        source_accounts = self.helius.get_accounts(source_wallet.keypair)
        destination_accounts = self.helius.get_accounts(destination_wallet.keypair)
