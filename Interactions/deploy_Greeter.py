### Code to deploy and test the Greeter smart contract ###

### Imports
from web3 import Web3
from solcx import compile_source, set_solc_version
import os
import json
from dotenv import load_dotenv

### Load in the .env file
load_dotenv()

### Set the solc compiler version, we use 0.8.0
set_solc_version('0.8.0')

### Local blockchain instance server, visable in the command line 
RPC_SERVER = 'HTTP://127.0.0.1:8545'
CHAIN_ID = 1337 # The ganache chain id, always 1337!

### Deploy the contract to the local blockchain instance, returns the abi and address of the contract
def deploy_Greeter(address, key): 
    ### First lets connect to our local blockchain instance 
    session = Web3(Web3.HTTPProvider(RPC_SERVER))

    ### Print the initial balance of the wallet we deploy from
    initial_balance = session.eth.get_balance(address) / 10**18
    print("Balance before greet contract deployment (ETH) \n" + str(initial_balance) + "\n")

    ### Read in the contract as a string
    with open("./Contracts/Greeter.sol", "r") as file: 
        Greeter_raw = file.read()
        file.close() 
    
    ### Compile using solcx's compile_source function. See the docs to see more about how this works. 
    Greeter_compiled = compile_source(Greeter_raw, output_values=['abi', 'bin'])

    ### Store the ABI and bytecode
    # The ABI is the like an API for the contract, the bytecode is a binary file which is the "meat" of the contract. 
    Greeter_abi = Greeter_compiled['<stdin>:Greeter']['abi']
    Greeter_bin = Greeter_compiled['<stdin>:Greeter']['bin']

    ### Create the contract instance and deploy the transaction
    Greeter = session.eth.contract(abi=Greeter_abi, bytecode=Greeter_bin)
   
    ### Build the transaction, this requires the nonce for the wallet we deploy with.
    nonce = session.eth.get_transaction_count(address)
    tx = Greeter.constructor().build_transaction(
        {"chainId" : CHAIN_ID, "from" : address, "nonce" : nonce, "gasPrice": session.eth.gas_price})

    ### Sign the transaction
    signed_tx = session.eth.account.sign_transaction(tx, private_key=key)

    ### Send it to the blockchain and store its hash
    tx_hash = session.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    ### Wait for the receipt
    tx_receipt = session.eth.wait_for_transaction_receipt(tx_hash)

    ### Return the contract address and abi, these are whats needed to interact with the contract after deployment.
    Greeter_dict = {'address' : tx_receipt.contractAddress, 'abi' : Greeter_abi}

    ### Write this dict to a json file so we can use it later
    with open("./Contracts/DeployedGreeter.json", "w") as file: 
        json.dump(Greeter_dict, file)

    ### Print resulting balance and the amount of gas used 
    resulting_balance = session.eth.get_balance(address) / 10**18
    gas_used = (initial_balance - resulting_balance) * 10**18
    print("Balance after greeter contract deployment (ETH) \n" + str(resulting_balance) + "\n")
    print("Gas used to deploy the greeter contract (WEI/GWEI) \n" + str(gas_used) + " / " + str(gas_used * 10**(-9)) + "\n")