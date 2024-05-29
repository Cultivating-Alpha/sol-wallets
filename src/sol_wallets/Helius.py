import requests
import json

from sol_wallets.pprint import pprint

API_KEY = "c0732911-8b66-4cf4-943c-298543f46544"
url = f"https://devnet.helius-rpc.com/?api-key={API_KEY}"
owner = "51iAWLX4niXKE2LFUCKDH1CJSrEqD1z5owcPsZpCUfGq"

url = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"
owner = "3AKTArakTTSERVCFSeonxTa21YrEjwufhKQUYy1sgcKj"


class Account:
    asset: dict = {}
    amount: int
    name: str
    symbol: str = ""

    def __init__(self, asset, amount):
        self.asset = asset
        decimal = asset["token_info"]["decimals"]
        self.amount = int(amount / 10**decimal)
        try:
            self.name = asset["content"]["metadata"]["name"]
        except:
            self.name = asset["token_info"]["symbol"]

        try:
            self.symbol = asset["token_info"]["symbol"]
        except:
            pass


def helius():
    accounts = get_accounts(owner)

    ids = []
    amounts = []
    for account in accounts:
        ids.append(account["mint"])
        amounts.append(account["amount"])

    assets = get_asset(ids)
    accounts = []
    for i, asset in enumerate(assets):
        accounts.append(Account(asset, amounts[i]))

    for account in accounts:
        print(f"You have {account.amount} ({account.symbol}) --> {account.name}")

    # pprint(account)
    # amount = account["amount"] / 100_000
    # asset = get_asset(account["mint"])
    # # pprint(asset)
    # name = asset["content"]["metadata"]["name"]
    # print(f"You have {amount} of token {name}")


def get_asset(accounts):
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": "my-id",
        "method": "getAssetBatch",
        "params": {
            "ids": accounts,
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        result = data.get("result")
        # print(json.dumps(result, indent=4))
        return result
    else:
        print(f"Request failed with status code {response.status_code}")


def get_accounts(owner):
    headers = {"Content-Type": "application/json"}

    payload = {
        "jsonrpc": "2.0",
        "method": "getTokenAccounts",
        "id": "helius-test",
        "params": {
            "page": 1,
            "limit": 100,
            "displayOptions": {
                "showZeroBalance": False,
            },
            "owner": owner,
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()

        if not data.get("result"):
            print("No result in the response", data)
            return []
        else:
            return data["result"]["token_accounts"]
    else:
        print(f"Request failed with status code {response.status_code}")
        return []
