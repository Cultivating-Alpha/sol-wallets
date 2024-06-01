from sol_wallets.Wallet import Wallet
from sol_wallets.Wallets import Wallets
from sol_wallets.pprint import pprint
from spl.token.client import Token

from sol_wallets.Helius import get_helius
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import transfer_checked, TransferCheckedParams
from sol_wallets.Menu import clear, Menu
from solders.pubkey import Pubkey
from solders.keypair import Keypair

from spl.token.client import Token

sample_wallets = {
    "main": "BuouBWx5AVadDXzKFwBxaAxUnT3K5H6rRQmtAeCYGyLM",
    "devnet": "51iAWLX4niXKE2LFUCKDH1CJSrEqD1z5owcPsZpCUfGq",
}


def find_missing_accounts(source_accounts, _target_accounts):
    target_accounts = [account.mint for account in _target_accounts]
    missing = []
    for account in source_accounts:
        if account.mint not in target_accounts:
            missing.append(account)
    return missing


usdc_devnet_mint = "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU"


def move():
    secret = "27FBSJH6NZipnEM2M1PNDV5P9wAvnr9kca2Ds4ipMXo7nLTK5W6DSJBPZccQoq9t17hM74evEBTyQAhogSFj4Gso"
    wallets = Wallets("devnet")
    devnet_user_wallet = Wallet(network="devnet", secret=secret)
    devnet_user_wallet.prepare_token_accounts()
    balance = devnet_user_wallet.get_balance()
    print(balance)
    balance = devnet_user_wallet.get_token_balances()
    print(balance)
    # print(devnet_user_wallet.keypair.pubkey())
    return

    main_wallet = wallets.main_wallet
    # balance =main_wallet.get_token_balance(usdc_devnet_mint)

    source_token_account = main_wallet.get_token_account(usdc_devnet_mint)
    print(source_token_account)
    print(devnet_user_wallet.token_accounts)
    destination_wallet = devnet_user_wallet.get_token_account(usdc_devnet_mint)

    main_wallet.transfer_tokens(usdc_devnet_mint, destination_wallet.address, 7.9)
    return

    # Token.create_account(
    #     owner=Pubkey.from_string("51iAWLX4niXKE2LFUCKDH1CJSrEqD1z5owcPsZpCUfGq")
    # )

    return

    # print(main_wallet.pubkey())
    # print()
    # print(devnet_user_wallet.pubkey())

    # print(main_wallet.get_token_balance(usdc_devnet_mint))
    # print()
    # print(devnet_user_wallet.get_token_balance(usdc_devnet_mint))
    # print()
    # print(wallets.sub_wallets[0].get_token_balance(usdc_devnet_mint))

    return

    # print(destination_wallet)

    return


def main():
    move()
    return
    clear()
    wallets = Wallets("devnet")
    runner = Menu("devnet", wallets, devnet_user_wallet)

    # runner.distribute()
    # runner.return_coins()
    runner.menu()
    # flow.return_amount_to_user()
    return
