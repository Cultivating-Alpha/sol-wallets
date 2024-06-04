from typing import Literal
import requests
from solders.keypair import Keypair
from sol_wallets.Account import Account
from sol_wallets.Env import get_key


class Helius:
    network: str = "mainnet"
    accounts: list[Account] = []

    def __init__(self, API_KEY, network="mainnet"):
        self.network = network
        self.url = f"https://{network}.helius-rpc.com/?api-key={API_KEY}"

    def get_accounts(self, owner: Keypair):
        owner_pubkey = owner.pubkey()
        token_accounts = self.get_token_accounts(owner_pubkey)

        ids = []
        amounts = []
        for account in token_accounts:
            ids.append(account["mint"])
            amounts.append(account["amount"])

        assets = self.get_assets(ids)
        accounts = []
        for i, asset in enumerate(assets):
            accounts.append(
                Account(token_accounts[i], asset, amounts[i], self.network, owner)
            )

        self.accounts = accounts
        return accounts

    def get_assets(self, accounts):
        headers = {"Content-Type": "application/json"}
        payload = {
            "jsonrpc": "2.0",
            "id": "my-id",
            "method": "getAssetBatch",
            "params": {
                "ids": accounts,
            },
        }

        response = requests.post(self.url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            result = data.get("result")
            # print(json.dumps(result, indent=4))
            return result
        else:
            print(f"Failed to get assets. Status code {response.status_code}")
            return []

    def get_asset(self, id):
        headers = {"Content-Type": "application/json"}
        # Define the payload
        payload = {
            "jsonrpc": "2.0",
            "id": "test",
            "method": "getAsset",
            "params": {"id": id},
        }

        # Make the POST request
        response = requests.post(self.url, headers=headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            return data
        else:
            print(f"Failed to get single asset. Status code {response.status_code}")

    def get_token_accounts(self, owner):
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
                "owner": str(owner),
            },
        }

        response = requests.post(self.url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()

            if not data.get("result"):
                print("No result in the response", data)
                return []
            else:
                return data["result"]["token_accounts"]
        else:
            print(f"Failed to get token accounts. Status code {response.status_code}")
            return []


def get_helius(network: Literal["mainnet", "testnet", "devnet"]):
    return Helius(get_key("HELIUS_KEY"), network=network)
