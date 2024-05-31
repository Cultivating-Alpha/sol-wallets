import math

from sol_wallets.Actions import Actions
from sol_wallets.Wallet import Wallet


class Flow:
    def __init__(self, network, user_wallet: Wallet, target_wallet: Wallet):
        self.action = Actions(network)
        self.network = network
        self.user_wallet = user_wallet
        self.target_wallet = target_wallet

    def refill_target(self, min_amount: float):
        balance = self.target_wallet.get_balance()
        if balance < min_amount:
            missing_amount = math.floor(100 - balance * 1000)
            if missing_amount == 0:
                print("There is a missing amount, but it's too small. Passing!")
                return
            print(
                f"Target Wallet's balance needs {missing_amount / 1_000} SOL -- its balance is {balance}"
            )

            self.action.move_sol(
                self.user_wallet.keypair, self.target_wallet.keypair, missing_amount
            )

    def return_amount_to_user(self):
        balance = self.target_wallet.get_balance()
        money_to_return = math.floor(balance * 1_000) - 1
        if money_to_return == 0:
            print("SOL to return is too small. Passing")
            return
        print(
            f"Target Wallet has {balance} SOL. It needs to return {money_to_return / 1_000}"
        )
        print("")
        self.action.move_sol(
            self.target_wallet.keypair, self.user_wallet.keypair, money_to_return
        )
