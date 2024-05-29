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
