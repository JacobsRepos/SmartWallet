### Code to deploy and test the Greeter smart contract ###

from web3 import Web3
from solcx import compile_source, set_solc_version
import os
from dotenv import load_dotenv

### Load in the .env file
load_dotenv()

### Set the solc compiler version, we use 0.8
set_solc_version('0.8.0')

### Local blockchain instance server, visable in the command line 
RPC_SERVER = 'HTTP://127.0.0.1:8545'
CHAIN_ID = 1337 # The ganache chain id, always 1337!

### Deploy the contract to the local blockchain instance, returns the abi and address of the contract
def deploy_Greeter(owner_address, key): 
    ### First lets connect to our local blockchain instance 
    session = Web3(Web3.HTTPProvider(RPC_SERVER))

    ### Read in the contract as a string
    with open("./Contracts/Greeter.sol", "r") as file: 
        Greeter_raw = file.read()
        file.close() 
    
    ### Compile using solcx
    Greeter_compiled = compile_source(Greeter_raw, output_values=['abi', 'bin'])

    ### Lets store and have a look at the abi 
    Greeter_abi = Greeter_compiled['<stdin>:Greeter']['abi']

    ### And now the bytecode, no point looking its not readable
    Greeter_bin = Greeter_compiled['<stdin>:Greeter']['bin']

    ### Now we create the contract instance and deploy the transaction
    Greeter = session.eth.contract(abi=Greeter_abi, bytecode=Greeter_bin)
    
    # Now we build and deploy the transaction to send to the blockchain
   
    ### First lets build the transaction
    nonce = session.eth.get_transaction_count(owner_address)
    tx = Greeter.constructor().build_transaction(
        {"chainId" : CHAIN_ID, "from" : owner_address, "nonce" : nonce, "gasPrice": session.eth.gas_price})

    ### Now lets sign the transaction
    signed_tx = session.eth.account.sign_transaction(tx, private_key=key)

    ### And lets get its hash
    tx_hash = session.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    ### And the receipt for the deployed transaction
    tx_receipt = session.eth.wait_for_transaction_receipt(tx_hash)

    ### We'll return the contract address and abi, these are whats needed to interact with the contract.
    return {'address' : tx_receipt.contractAddress, 'abi' : Greeter_abi}

def test_greeter(owner_address, contract_address, key, abi):
    # First we will test out the read only function greet() 

    ### Connect to the local blockchain instance
    session = Web3(Web3.HTTPProvider(RPC_SERVER))

    ### Create the contract instance and get the owner's nonce
    instance = session.eth.contract(address=contract_address, abi=abi)

    ### Now we can test greet() works, should output "hello" for a freshly deployed contract
    print(instance.functions.greet().call())

    # Now we'll change the greeting to Ciao, testing out our ability to write to the contract

    ### First lets build the transaction
    nonce = session.eth.get_transaction_count(owner_address)
    tx = instance.functions.setGreeting('Ciao').build_transaction(
    {'chainId' : CHAIN_ID, 'from' : owner_address, "nonce" : nonce, "gasPrice" : session.eth.gas_price})

    ### And sign
    signed_tx = session.eth.account.sign_transaction(tx, private_key=key)
    
    ### Get the hash
    tx_hash = session.eth.send_raw_transaction(signed_tx.rawTransaction)

    ### And finally lets get the receipt
    tx_receipt = session.eth.wait_for_transaction_receipt(tx_hash)

    ### Now lets see if it worked
    print(instance.functions.greet().call())

### Replace these with your wallet key/address found in the Ganache CLI
owner_address = '0x4C524A32Ce8bE25Ada9327C065AE6514ef3A0fc5'
owner_key = os.getenv('WALLET0_KEY')

### Deploy the contract, storing the contract's address and abi. 
Greeter = deploy_Greeter(owner_address=owner_address, key=owner_key)

### Test the contract works, should print "Hello" and "Ciao" respectively.
test_greeter(owner_address=owner_address, contract_address=Greeter['address'], key=owner_key, abi=Greeter['abi'])

