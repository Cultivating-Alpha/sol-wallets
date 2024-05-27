import base58
from solders.keypair import Keypair
from mnemonic import Mnemonic

from sol_wallets.Client import get_client


class Wallet:
    def __init__(
        self,
        network="devnet",
        _bytes: bytes = b"",
        mnemo: str = "",
        secret: str = "",
    ):
        if _bytes != b"":
            self.keypair = self.from_bytes(_bytes)
        elif mnemo != "":
            self.keypair = self.from_mnemo(mnemo)
        elif secret != "":
            self.keypair = self.from_secret(secret)
        else:
            print("Please provider either mnemo or secret!")

        self.client = get_client(network)

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
