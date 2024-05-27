import requests


def get_solana_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "solana", "vs_currencies": "usd"}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["solana"]["usd"]
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None
