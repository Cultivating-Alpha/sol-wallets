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


sample_wallets = {
    "main": "BuouBWx5AVadDXzKFwBxaAxUnT3K5H6rRQmtAeCYGyLM",
    "devnet": "51iAWLX4niXKE2LFUCKDH1CJSrEqD1z5owcPsZpCUfGq",
}

secret = "27FBSJH6NZipnEM2M1PNDV5P9wAvnr9kca2Ds4ipMXo7nLTK5W6DSJBPZccQoq9t17hM74evEBTyQAhogSFj4Gso"
devnet_user_wallet = Wallet(network="devnet", secret=secret)


wallets = Wallets("devnet")
main_wallet = Keypair.from_base58_string(secret)


def find_missing_accounts(source_accounts, _target_accounts):
    target_accounts = [account.mint for account in _target_accounts]
    missing = []
    for account in source_accounts:
        if account.mint not in target_accounts:
            missing.append(account)
    return missing


def move():
    # bal = wallets.main_wallet.get_balance()
    # print(bal)
    # bal = wallets.main_wallet.get_token_balances()
    # print(bal)

    wallets = Wallets("devnet")
    menu = Menu("devnet", wallets, devnet_user_wallet)
    menu.return_amount_to_user()
    # menu.fund_main_wallet()

    # menu.show_menu()
    return
    helius = get_helius("devnet")
    all_active_accounts = helius.get_accounts(main_wallet)

    sub = wallets.sub_wallets[4]
    all_sub_accounts = helius.get_accounts(sub.keypair)

    # print(all_sub_accounts)
    # print(all_active_accounts[0].mint)

    missing_accounts = find_missing_accounts(all_active_accounts, all_sub_accounts)
    missing_str = ""
    for account in missing_accounts:
        missing_str += f"{account.symbol} -"
    print(f"Wallet at {sub.pubkey()} is missing the following: {missing_str}")

    # acc = all_active_accounts[0]
    # acc.get_balance

    # for account in all_active_accounts:
    #     print(account)
    #     print(account.token_account["mint"])

    return

    active_wallet = wallets.sub_wallets[4]
    accounts = helius.get_accounts(active_wallet)
    print(accounts)
    # for account in accounts:
    #     pprint(account.token_account)
    #     pprint(account.asset)
    acc = accounts[0]
    balance = acc.get_balance()
    print(balance)
    print(acc.get_token_address())
    return

    # print(wallets.sub_wallets[3].pubkey())
    # print(str(wallets.sub_wallets[3].pubkey()))
    sub = "5dhqSo9ekzQdDELQK2isLgqoAfXQnk5oApdDMc1XDwQE"
    mint = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
    spl_client = Token(
        conn=client, pubkey=mint, program_id=TOKEN_PROGRAM_ID, payer=main_wallet
    )
    dest_key = spl_client.create_account(Pubkey.from_string(sub))
    print(dest_key)
    # info = spl_client.get_account_info(Pubkey.from_string(sub))
    # print(info)
    amount = 1000000
    source_usdc = Pubkey.from_string("E9RuipUGU7NAns9t81PFyhcBNWF3Q6hHaA29yUA2ThXb")

    transaction = spl_client.transfer(
        source=source_usdc,
        dest=dest_key,
        owner=main_wallet,
        amount=amount,
        multi_signers=None,
        opts=None,
        recent_blockhash=None,
    )
    return
    accounts = helius.get_accounts(str(wallets.sub_wallets[3].pubkey()))
    for account in accounts:
        print(account.amount)
        pprint(account.token_account)
        pprint(account.asset)

    return

    mint = Pubkey.from_string("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
    spl_client = Token(
        conn=client, pubkey=mint, program_id=TOKEN_PROGRAM_ID, payer=main_wallet
    )
    source_usdc = Pubkey.from_string("E9RuipUGU7NAns9t81PFyhcBNWF3Q6hHaA29yUA2ThXb")

    # Example usage: Transfer tokens
    source = main_wallet.pubkey()
    dest = wallets.main_wallet.pubkey()

    # print("-------------------")
    # accounts = helius.get_accounts("GgCrjahYZvWVF3vZn4ybCEgCNjAnX4jWJ86kCjy34WEa")
    # for account in accounts:
    #     print(account.amount)
    #     pprint(account.token_account)
    #     pprint(account.asset)
    amount = 1000000

    dest_usdc = Pubkey.from_string("Bcyn9gkiJPc9rBqEQvBxKX84uvkvWHNjtfLoPZfbrvGy")
    transaction = spl_client.transfer(
        source=source_usdc,
        dest=dest_usdc,
        owner=main_wallet,
        amount=amount,
        multi_signers=None,
        opts=None,
        recent_blockhash=None,
    )
    print("Done")

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
