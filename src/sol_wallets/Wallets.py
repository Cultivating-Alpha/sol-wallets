import os
from solders.keypair import Keypair

from sol_wallets import Wallet


class Wallets:
    main_wallet: Wallet
    sub_wallets: list[Wallet] = []
    number_of_sub_wallets: int = 3

    def __init__(self, network):
        self.wallet_file = f"wallets/{network}-main_wallet.bin"
        self.network = network
        self.load_wallets()
        pass

    def load_wallets(self):
        dir_path = "wallets"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if os.path.exists(self.wallet_file):
            self.main_wallet = self.read_wallet(self.wallet_file)
            self.sub_wallets = []
            for idx in range(self.number_of_sub_wallets):
                self.sub_wallets.append(
                    self.read_wallet(f"wallets/{self.network}-sub_wallet-{idx}.bin")
                )

        else:
            print("Wallet file not found. Creating new wallets!")
            self.create_wallets()
            self.load_wallets()

    def read_wallet(self, file_name):
        with open(file_name, "rb") as f:
            data = f.read()
        return Wallet(network=self.network, _bytes=data)

    def write_binary(self, file_name, wallet):
        with open(file_name, "wb") as binary_file:
            binary_file.write(bytes(wallet))

    def create_wallets(self):
        main_wallet = Keypair()
        self.write_binary(f"wallets/{self.network}-main_wallet.bin", main_wallet)

        sub_wallets = [Keypair() for _ in range(self.number_of_sub_wallets)]

        for idx, sw in enumerate(sub_wallets):
            self.write_binary(f"wallets/{self.network}-sub_wallet-{idx}.bin", sw)

    def reset_saved_data(self):
        self.main_wallet.prepare_token_accounts()
        for sub in self.sub_wallets:
            sub.prepare_token_accounts()
