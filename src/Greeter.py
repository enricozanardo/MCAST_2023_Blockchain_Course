import os
from dotenv import load_dotenv
from loguru import logger
from solcx import compile_source, install_solc 
from web3 import Web3
from eth_account import Account
from web3.contract import Contract

from src.User import User

load_dotenv()
Account.enable_unaudited_hdwallet_features()

SOLC_VERSION = os.getenv('SOLC_VERSION') or "0.8.0"
GOERLY_PROVIDER_URL = os.getenv('GOERLY_PROVIDER_URL')
MY_WALLET_ADDRESS = os.getenv('MY_WALLET_ADDRESS')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
GANACHE_URL = os.getenv('GANACHE_URL') or "http://127.0.0.1:8545"

install_solc(SOLC_VERSION)


class Greeter():

    def __init__(self, filename: str) -> None:
        # logger.info("Hi I'm Greeter")
        self.web3 = self.get_web3()
        self.user = self.get_owner_account()
        self.filename = filename
        self.contract_address = None

    def get_web3(self):
        # logger.info(f"start to connect to web3")
        web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
        return web3
    

    def get_owner_account(self) -> User:
        address_checksum = self.web3.to_checksum_address(MY_WALLET_ADDRESS)
        priv_key = os.getenv('MY_WALLET_PRIVATE_KEY')
        nonce = self.web3.eth.get_transaction_count(address_checksum)

        user = User(address_checksum, priv_key, nonce)

        return user
    

    def get_balance(self, wallet_address):
        balance = self.web3.eth.get_balance(wallet_address)
        ether = self.web3.from_wei(balance, 'ether')

        return ether
    

    def compile_smart_contract(self):
        cwd = os.getcwd()
        smart_contract_file = open(f"{cwd}/src/contract/{self.filename}", "r")
        smart_contract_file_text = smart_contract_file.read()
        smart_contract = compile_source(smart_contract_file_text)

        return smart_contract
    

    def get_contract(self):
        ca = Web3.to_checksum_address(self.contract_address)
        smart_contract = self.compile_smart_contract()
        contract_id, contract_interface = smart_contract.popitem()
        abi = contract_interface['abi']
        my_contract = self.web3.eth.contract(address=ca, abi=abi)

        return my_contract

        
    def deploy(self):
        smart_contract = self.compile_smart_contract()
        contract_id, contract_interface = smart_contract.popitem()

        # bytecode
        bytecode = contract_interface['bin']
        # abi
        abi = contract_interface['abi']

        greeter_smart_contract: Contract = self.web3.eth.contract(abi=abi, bytecode=bytecode)
    
        # logger.info(f"greeter_smart_contract: {greeter_smart_contract}")
        gas_estimate = greeter_smart_contract.constructor().estimate_gas()
        # logger.warning(f"gas_estimate: {gas_estimate}")


        tx = greeter_smart_contract.constructor().build_transaction({
            "gasPrice": self.web3.eth.gas_price, 
            "chainId": self.web3.eth.chain_id, 
            "from": self.user.address, 
            "nonce": self.user.nonce
            }
        )

        signed_tx = self.web3.eth.account.sign_transaction(tx, self.user.priv_key)

        # send the transactio to Blockchain
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        
        # logger.info(f"contract address: {receipt.contractAddress}")

        self.contract_address = receipt.contractAddress

    def last_greet(self):
        logger.info(f"get the last greeting..")

        contract = self.get_contract()

        message = contract.functions.greet().call()
        logger.info(f"last message: {message}")

        return message
    

    def set_greet(self, message):
        logger.info(f"set a new greeting..")

        contract = self.get_contract()

        tx = contract.functions.setGreeting(message).build_transaction()
        tx.update({ 'nonce': self.user.nonce })
        tx.update({ 'from': self.user.address })
        tx.update({ 'chainId': self.web3.eth.chain_id })
        
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.user.priv_key)
        #  Send the transaction to the Blockchain
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

        logger.info(f"receipt : {self.web3.to_hex(receipt.transactionHash)}") # 0xeedf19c20dd51d5fb6a7b27ef0e55df31202fbd59ca5b1e8e2892834cc03e0a4
        logger.info(f"blockNumber: {receipt.blockNumber}")
        logger.info(f"type: {receipt.type}")




        



        