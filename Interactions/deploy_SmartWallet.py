### Code to deploy and test the SmartWallet contrac ###

from web3 import Web3 
from solcx import compile_source, set_solc_version 
import os 
from dotenv import load_dotenv 
import json

### Load in the .env file 
load_dotenv()

### Set the solc compiler version, we use 0.8.0
set_solc_version('0.8.0')

### Local blockchain instance server info
RPC_SERVER = 'HTTP://127.0.0.1:8545'
CHAIN_ID = 1337 

### Deploy the contract to the local blockchain instance 
def deploy_SmartWallet(owner_address, owner_key): 
    ### Connect to the local blockchain instance 
    session = Web3(Web3.HTTPProvider(RPC_SERVER))

    ### Check the owners initial balance in wei 
    initial_owner_balance = session.eth.get_balance(owner_address) / 10**18
    print("Owner balance before smart wallet contract deployment (ETH) \n" + str(initial_owner_balance) + "\n")

    ### Read in the contract as a string
    with open("./Contracts/SmartWallet.sol", "r") as file: 
        SmartWallet_raw = file.read()
        file.close() # Remember to always close your files!

    ### Compile using the solcx solidity compiler python wrapper
    SmartWallet_compiled = compile_source(SmartWallet_raw, output_values=['abi', 'bin'])

    ### Store the abi and bytecode 
    SmartWallet_abi = SmartWallet_compiled["<stdin>:SmartWallet"]["abi"]
    SmartWallet_bin = SmartWallet_compiled["<stdin>:SmartWallet"]["bin"]

    ### Create the contract instance 
    SmartWallet = session.eth.contract(abi=SmartWallet_abi, bytecode=SmartWallet_bin)

    ### Build the transaction that'll deploy this contract
    nonce = session.eth.get_transaction_count(owner_address) 
    tx = SmartWallet.constructor().build_transaction(
        {"chainId" : CHAIN_ID, "from" : owner_address, 
         "nonce" : nonce, "gasPrice" : session.eth.gas_price})
    
    ### Sign it 
    signed_tx = session.eth.account.sign_transaction(tx, private_key=owner_key)

    ### Get its hash 
    tx_hash = session.eth.send_raw_transaction(signed_tx.rawTransaction)

    ### Finally lets wait for its receipt 
    tx_receipt = session.eth.wait_for_transaction_receipt(tx_hash)

    ### We return the contract address & abi, these are what we need
    ### to create instances of the contract later
    SmartWallet_dict = {"address" : tx_receipt.contractAddress, "abi" : SmartWallet_abi}

    ### Write the contract address and abi to a json file for later use
    with open("./Contracts/DeployedSmartWallet.json", "w") as file: 
        json.dump(SmartWallet_dict, file)

    ### Lets see how much gas it used
    resulting_owner_balance = session.eth.get_balance(owner_address) / 10**18 
    gas_used = (initial_owner_balance - resulting_owner_balance) * 10**18
    print("Owner balance after smart wallet contract deployment (ETH) \n" + str(resulting_owner_balance) + "\n")
    print("Gas used to deploy the smart wallet contract (WEI/GWEI) \n" + str(gas_used) + " / " + str(gas_used * 10**(-9)) + "\n")