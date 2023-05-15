from loguru import logger


class User():

    def __init__(self, address, priv_key, nonce) -> None:
        self.address = address
        self.priv_key = priv_key
        self.nonce = nonce
        