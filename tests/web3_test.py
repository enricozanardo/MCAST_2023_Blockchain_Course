import os
from dotenv import load_dotenv
from loguru import logger

from solcx import compile_source, install_solc 

from web3.contract import Contract


from web3 import Web3
from eth_account import Account
from src.User import User

load_dotenv()
Account.enable_unaudited_hdwallet_features()

SOLC_VERSION = os.getenv('SOLC_VERSION') or "0.8.0"
GOERLY_PROVIDER_URL = os.getenv('GOERLY_PROVIDER_URL')
CONTRACT_ADDRESS=os.getenv('CONTRACT_ADDRESS')

MY_WALLET_ADDRESS = os.getenv('MY_WALLET_ADDRESS')

GANACHE_URL = os.getenv('GANACHE_URL') or "http://127.0.0.1:8545"

install_solc(SOLC_VERSION)


# def test_solc_version():
#     logger.info(f"start to check solc version that must be {SOLC_VERSION}")
#     assert SOLC_VERSION == "0.8.0"


def test_web3():
    logger.info(f"start to connect to web3")
    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    is_connected = web3.is_connected()

    # chain_id = web3.eth.chain_id

    # logger.info(f"chain id: {chain_id}")

    assert is_connected == True


# def test_create_account():
#     text = "John milk cat dog window"

#     logger.info(f"start to create an account")
#     # 0x0b87EB4eEC7634aB135DdA829d2f961279ebEAb1
#     # 0xdabe48001b852fe364491b0f6a5a86473cb1edb843868b4924f569366b388053
#     # acct = Account.create(text)
#     # address = acct.address
#     # address_checksum = Web3.to_checksum_address(address)
#     web3 = Web3(Web3.HTTPProvider(GOERLY_PROVIDER_URL))
#     # key = web3.to_hex(acct._private_key)
#     add = "0xFAbA6eB0Ec80b4447bAcA6B90AF13188Dae150a6"

#     account_balance = web3.eth.get_balance(add) 

#     # logger.info(f"Address: {address}")
#     # logger.info(f"key: {key}")
#     logger.info(f"balace: {account_balance}")



def test_get_smart_contract():
    logger.info(f"get smart contract")
    smart_contract_file = open("greeter.sol", "r")
    smart_contract_file_text = smart_contract_file.read()
    smart_contract = compile_source(smart_contract_file_text)

    # logger.info(f"smart contract: {smart_contract}")

    assert smart_contract != None

# def get_contract():
#     ca = Web3.to_checksum_address(CONTRACT_ADDRESS)

#     smart_contract_file = open("greeter.sol", "r")
#     smart_contract_file_text = smart_contract_file.read()
#     smart_contract = compile_source(smart_contract_file_text)

#     contract_id, contract_interface = smart_contract.popitem()
#     abi = contract_interface['abi']

#     web3 = Web3(Web3.HTTPProvider(GOERLY_PROVIDER_URL))
#     my_contract: Contract = web3.eth.contract(address=ca, abi=abi)

#     return my_contract

def get_owner_account() -> User:
    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    address_checksum = web3.to_checksum_address(MY_WALLET_ADDRESS)
    priv_key = os.getenv('MY_WALLET_PRIVATE_KEY')
    nonce = web3.eth.get_transaction_count(address_checksum)

    user = User(address_checksum, priv_key, nonce)

    return user


def test_deploy():
        smart_contract_file = open("greeter.sol", "r")
        smart_contract_file_text = smart_contract_file.read()
        smart_contract = compile_source(smart_contract_file_text)
        contract_id, contract_interface = smart_contract.popitem()

        # bytecode
        bytecode = contract_interface['bin']
        # abi
        abi = contract_interface['abi']

        # logger.info(f"bytecode: {bytecode}")
        # logger.info(f"abi: {abi}")

        web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

        greeter_smart_contract: Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    
        user = get_owner_account()

        tx = greeter_smart_contract.constructor().build_transaction({
            "gasPrice": web3.eth.gas_price, 
            "chainId": web3.eth.chain_id, 
            "from": user.address, 
            "nonce": user.nonce
            }
        )

        signed_tx = web3.eth.account.sign_transaction(tx, user.priv_key)

        # # send the transactio to Blockchain
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        logger.info(f"contract address: {receipt.contractAddress}")

        # contract_address = receipt.contractAddress
        assert receipt.contractAddress != None


def get_contract():
    ca = Web3.to_checksum_address(CONTRACT_ADDRESS)
    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

    smart_contract_file = open("greeter.sol", "r")
    smart_contract_file_text = smart_contract_file.read()
    smart_contract = compile_source(smart_contract_file_text)
    contract_id, contract_interface = smart_contract.popitem()

    abi = contract_interface['abi']
    my_contract = web3.eth.contract(address=ca, abi=abi)

    return my_contract



def test_last_greet():
    logger.info(f"get smart contract")

    smart_contract = get_contract()

    message = smart_contract.functions.greet().call()
    logger.info(f"last message: {message}")

    assert message != None


# def test_public_variable():
#     logger.info(f"Read the public variable...")

#     smart_contract = get_contract()

#     public_variable = smart_contract.functions.public_string().call()
#     logger.info(f"Public string: {public_variable}")

#     assert public_variable == "ciao"



# # def test_public_string():
# #     logger.info(f"public string")

# #     smart_contract_file = open("greeter.sol", "r")
# #     smart_contract_file_text = smart_contract_file.read()
# #     smart_contract = compile_source(smart_contract_file_text)

# #     message = smart_contract.functions.greet().call();
# #     logger.info(f"last message: {message}")

# #     return message