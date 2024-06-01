import os
import json
import base58
from mnemonic import Mnemonic
from solders.pubkey import Pubkey
from spl.token.client import Token
from solders.keypair import Keypair
from sol_wallets.Account import Account
from sol_wallets.Client import get_client
from sol_wallets.Helius import get_helius
from spl.token.constants import TOKEN_PROGRAM_ID

from sol_wallets.SPL_Actions import SPL_Actions


class NewAddress:
    def __init__(self, address, name):
        self.address = address


class Wallet:
    network = "mainnet"

    def __init__(
        self,
        network="devnet",
        _bytes: bytes = b"",
        mnemo: str = "",
        secret: str = "",
    ):
        self._raw_token_accounts = []
        self.token_accounts = {}

        if _bytes != b"":
            self.keypair = self.from_bytes(_bytes)
        elif mnemo != "":
            self.keypair = self.from_mnemo(mnemo)
        elif secret != "":
            self.keypair = self.from_secret(secret)
        else:
            print("Please provider either mnemo or secret!")

        self.client = get_client(network)
        self.network = network

        self.file_name = f"wallets/{self.network}-{self.pubkey()}-token_accounts.json"

        if os.path.exists(self.file_name):
            self.load_token_accounts()
        else:
            self.prepare_token_accounts()

    def prepare_token_accounts(self, accounts=None):
        if accounts == None:
            accounts = self.get_wallet_accounts()

        for token_account in accounts:
            self._raw_token_accounts.append(token_account)
            self.token_accounts[token_account.mint] = {
                "token_account": token_account,
                "spl_client": Token(
                    conn=self.client,
                    pubkey=Pubkey.from_string(token_account.mint),
                    program_id=TOKEN_PROGRAM_ID,
                    payer=self.keypair,
                ),
            }
        self.save_token_accounts()

    def has_token_account(self, mint):
        if mint in self.token_accounts.keys():
            return True
        return False

    def from_bytes(self, data):
        return Keypair.from_bytes(bytes(data))

    def from_mnemo(self, words: str):
        _mnemo = Mnemonic("english")
        seed = _mnemo.to_seed(words)
        return Keypair.from_seed(seed[:32])

    def from_secret(self, secret: str):
        return Keypair.from_base58_string(secret)

    def secret(self):
        return self.keypair.secret()

    def private_key(self):
        private_key_bytes = self.secret()
        public_key_bytes = bytes(self.pubkey())
        encoded_keypair = private_key_bytes + public_key_bytes
        private_key = base58.b58encode(encoded_keypair).decode()
        return private_key

    def pubkey(self):
        return self.keypair.pubkey()

    def get_balance(self):
        return self.client.get_balance(self.keypair.pubkey()).value / 1_000_000_000

    def get_token_balances(self):
        accounts = self.get_wallet_accounts()
        print(accounts)
        for account in accounts:
            balance = account.get_balance()
            print(f"You have {balance} ({account.symbol}) --> {account.mint}")

    def get_token_balance(self, mint):
        if mint in self.token_accounts.keys():
            account = self.token_accounts[mint]
            balance = account["token_account"].get_balance()
            print(account["token_account"].get_token_address())
            print(f"You have {balance} ({account['token_account'].symbol}) --> {mint}")
        else:
            print("Token account not found!")

    def get_wallet_accounts(self):
        self.accounts = get_helius(self.network).get_accounts(self.keypair)
        return self.accounts

    def get_token_account(self, mint):
        if mint in self.token_accounts.keys():
            return self.token_accounts[mint]["token_account"]
        else:
            print("Account doesn't exist, so we are creating a new one!")
            spl_client = Token(
                conn=self.client,
                pubkey=Pubkey.from_string(mint),
                program_id=TOKEN_PROGRAM_ID,
                payer=self.keypair,
            )
            addr = spl_client.create_account(owner=self.pubkey())
            return NewAddress(addr, mint)

    def transfer_tokens(self, mint, destination_wallet, amount):
        if mint in self.token_accounts.keys():
            account = self.token_accounts[mint]
            print(account)
            amount_to_send = account["token_account"].format_amount(amount)
            print(amount_to_send)
            spl_client: SPL_Actions = account["spl_client"]
            spl_client.transfer_token_to_address(destination_wallet, amount_to_send)
        else:
            print("Token account not found!")

    def save_token_accounts(self):
        accounts = []
        for account in self._raw_token_accounts:
            accounts.append(account.to_json())
        with open(self.file_name, "w") as f:
            json.dump(accounts, f)

    def load_token_accounts(self):
        self.file_name = f"wallets/{self.network}-{self.pubkey()}-token_accounts.json"
        with open(self.file_name, "r") as f:
            accounts = json.load(f)

        for account in accounts:
            token_account = Account(
                token_account=account["token_account"],
                asset=account["asset"],
                amount=account["amount"],
                network=account["network"],
                owner=self.keypair,
            )
            self._raw_token_accounts.append(token_account)
            self.token_accounts[token_account.mint] = {
                "token_account": token_account,
                "spl_client": SPL_Actions(
                    account=token_account,
                    main_wallet=self.keypair,
                    main_token_wallet=token_account.token_account,
                    network="devnet",
                ),
            }
