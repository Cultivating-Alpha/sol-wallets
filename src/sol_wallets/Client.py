from solana.rpc.api import Client


def get_client(network):
    if network == "testnet":
        return Client("https://api.testnet.solana.com")
    elif network == "devnet":
        return Client("https://api.devnet.solana.com")
    else:
        return Client("https://api.mainnet-beta.solana.com")
