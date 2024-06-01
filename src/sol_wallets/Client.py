from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient


def get_client(network):
    if network == "testnet":
        return Client("https://api.testnet.solana.com")
    elif network == "devnet":
        return Client("https://api.devnet.solana.com")
    else:
        return Client("https://api.mainnet-beta.solana.com")


def get_async_client(network) -> AsyncClient:
    if network == "testnet":
        return AsyncClient("https://api.testnet.solana.com")
    elif network == "devnet":
        return AsyncClient("https://api.devnet.solana.com")
    else:
        return AsyncClient("https://api.mainnet-beta.solana.com")
