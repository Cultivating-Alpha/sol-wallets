from solders.pubkey import Pubkey
from sol_wallets.Client import get_client
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID


class SPL_Actions:
    def __init__(self, account, main_wallet, main_token_wallet, network="devnet"):
        client = get_client(network)
        self.account = account
        self.main_token_wallet = main_token_wallet
        self.main_wallet = main_wallet

        self.spl_client = Token(
            conn=client,
            pubkey=account.mint,
            program_id=TOKEN_PROGRAM_ID,
            payer=main_wallet,
        )

    def transfer_token_to_address(self, dest, amount):
        source = Pubkey.from_string(self.main_token_wallet["address"])
        print(
            f"Transfering {amount / 10**self.account.decimal} {self.account.name} between:\nSender: {source}\nReceiver: {dest}"
        )

        self.spl_client.transfer(
            source=source,
            dest=dest,
            owner=self.main_wallet.keypair,
            amount=amount,
            multi_signers=None,
            opts=None,
            recent_blockhash=None,
        )

    @staticmethod
    def find_missing_accounts(source_accounts, _target_accounts):
        target_accounts = [account.mint for account in _target_accounts]
        missing = []
        for account in source_accounts:
            if account.mint not in target_accounts:
                missing.append(account.mint)
        return missing
