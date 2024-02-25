### Code to test out the deployed Greeter contract ###

### Imports
from web3 import Web3
from dotenv import load_dotenv

### Load in the .env file
load_dotenv()

### Local blockchain instance server, visable in the command line 
RPC_SERVER = "HTTP://127.0.0.1:8545"
CHAIN_ID = 1337 # The ganache chain id, always 1337. If you're using a different blockchain google it :) 

### Replace these with your wallet key/address found in the Ganache CLI

### This will test every facet of the Greeter contract.
def test_Greeter(address, key, contract_address, abi):
    # First we will test out the read only function greet() 

    ### Connect to the local blockchain instance
    session = Web3(Web3.HTTPProvider(RPC_SERVER))

    ### Create the contract instance and get the owner's nonce
    instance = session.eth.contract(address=contract_address, abi=abi)

    ### Get and print the initial balance
    initial_balance = session.eth.get_balance(address) / 10**18
    print("Balance before greeting (ETH) \n" + str(initial_balance))

    ### Print the currently stored greeting, should be "Hello" for a freshly deployed Greeter contract.
    print(instance.functions.greet().call())

    ### Get and print the balance after greeting along with the gas, should be the same / 0 respectively
    post_greet_balance = session.eth.get_balance(address) / 10**18
    print("Balance after greeting (ETH) \n" + str(post_greet_balance))

    # Now we'll change the greeting to Ciao, testing out our ability to write to the contract

    ### Build the transaction
    nonce = session.eth.get_transaction_count(address)
    tx = instance.functions.set_greeting('Ciao').build_transaction(
    {'chainId' : CHAIN_ID, 'from' : address, "nonce" : nonce, "gasPrice" : session.eth.gas_price})

    ### Sign it
    signed_tx = session.eth.account.sign_transaction(tx, private_key=key)
    
    ### Send the transaction to the blockchain and store the transaction's hash
    tx_hash = session.eth.send_raw_transaction(signed_tx.rawTransaction)

    ### Wait for the receipt
    tx_receipt = session.eth.wait_for_transaction_receipt(tx_hash)

    ### Print the updated greeting, should be Ciao
    print(instance.functions.greet().call())

    ### Print the balance and gas used after setting the greeting to Ciao
    post_setgreeting_balance = session.eth.get_balance(address) / 10**18
    gas_used_to_change_greeting = (post_greet_balance - post_setgreeting_balance) * 10**18
    print("Balance after changing greeting to Ciao (ETH) \n" + str(post_setgreeting_balance))
    print("Gas used to change greeting to Ciao (WEI/GWEI) \n" + str(gas_used_to_change_greeting) + " / " + 
          str(gas_used_to_change_greeting * 10**(-9)) + "\n")

