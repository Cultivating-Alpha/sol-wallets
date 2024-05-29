import requests
from sol_wallets.Account import Account


class Helius:
    def __init__(self, API_KEY):
        self.url = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"

    def get_accounts(self, owner):
        accounts = self.get_token_accounts(owner)

        ids = []
        amounts = []
        for account in accounts:
            ids.append(account["mint"])
            amounts.append(account["amount"])

        assets = self.get_asset(ids)
        accounts = []
        for i, asset in enumerate(assets):
            accounts.append(Account(asset, amounts[i]))

        self.accounts = accounts
        return accounts

    def get_asset(self, accounts):
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
            print(f"Request failed with status code {response.status_code}")

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
                "owner": owner,
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
            print(f"Request failed with status code {response.status_code}")
            return []
