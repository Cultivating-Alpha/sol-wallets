import os
from solders.keypair import Keypair


class Wallets:
    wallet_file = "wallets/main_wallet.bin"
    main_wallet: Keypair
    sub_wallets: list[Keypair] = []

    def __init__(self):
        self.load_wallets()
        pass

    def load_wallets(self):
        if os.path.exists(self.wallet_file):
            self.main_wallet = self.read_wallet(self.wallet_file)
            self.sub_wallets = []
            for idx in range(25):
                self.sub_wallets.append(
                    self.read_wallet(f"wallets/sub_wallet-{idx}.bin")
                )

        else:
            print("Wallet file not found.")
            self.create_wallets()

    def read_wallet(self, file_name):
        with open(file_name, "rb") as f:
            data = f.read()
        return Keypair.from_bytes(bytes(data))

    def write_binary(self, file_name, wallet):
        with open(file_name, "wb") as binary_file:
            binary_file.write(bytes(wallet))

    def create_wallets(self):
        main_wallet = Keypair()
        self.write_binary("wallets/main_wallet.bin", main_wallet)

        sub_wallets = [Keypair() for _ in range(25)]

        for idx, sw in enumerate(sub_wallets):
            self.write_binary(f"wallets/sub_wallet-{idx}.bin", main_wallet)


wallets = Wallets()
