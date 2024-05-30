from sol_wallets.Client import get_client
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID


def get_spl_client(network, mint, payer):
    client = get_client(network)
    return Token(conn=client, pubkey=mint, program_id=TOKEN_PROGRAM_ID, payer=payer)
