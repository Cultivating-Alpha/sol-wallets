from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv()
config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}


def get_key(key):
    return config[key]
