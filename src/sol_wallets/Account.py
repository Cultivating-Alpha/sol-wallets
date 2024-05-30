from solders.keypair import Keypair
from sol_wallets.Client import get_client
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.pubkey import Pubkey


class Account:
    asset: dict = {}
    amount: int
    name: str
    symbol: str = ""
    mint: str = ""

    def __init__(self, token_account, asset, amount, network, owner):
        self.network = network
        self.client = get_client(self.network)
        self.token_account = token_account
        self.mint = token_account["mint"]
        self.asset = asset
        self.decimal = asset["token_info"]["decimals"]
        self.amount = int(amount / 10**self.decimal)
        try:
            self.symbol = asset["token_info"]["symbol"]
        except KeyError:
            pass

        try:
            self.name = asset["content"]["metadata"]["name"]
        except KeyError:
            self.name = self.symbol

        self._create_spl_client(owner)

    def _create_spl_client(self, owner):
        mint = Pubkey.from_string(self.token_account["mint"])
        self.spl_client = Token(
            conn=self.client, pubkey=mint, program_id=TOKEN_PROGRAM_ID, payer=owner
        )

    def create_token_account(self, pubkey: Pubkey = None, pubkey_str: str = ""):
        if pubkey_str != "":
            pubkey = Pubkey.from_string(pubkey_str)
        elif not pubkey:
            print("Please provide a valid pubkey or public key string")
            return
        return self.spl_client.create_account(pubkey)

    def print(self):
        print(f"You have {self.amount} ({self.symbol}) --> {self.name}")

    def get_token_address(self):
        return Pubkey.from_string(self.token_account["address"])

    def get_balance(self):
        res = self.spl_client.get_balance(self.get_token_address())
        return res.value.ui_amount
