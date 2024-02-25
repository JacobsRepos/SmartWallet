### Code to test the SmartWallet contract ###

### Imports 
from web3 import Web3
import json
from dotenv import load_dotenv

### Load in the .env file 
load_dotenv()

### Get our blockchain instance variables
RPC_SERVER = 'HTTP://127.0.0.1:8545'
CHAIN_ID = 1337 # The ganache chain id, always 1337!

### Interacts with the already deployed SmartWallet contract. In particular it:
# Deposits the deposit amount from the sender's wallet to the contract via the deposit function
# Withdraws the withdraw amount from the contract to the owner's wallet
def test_SmartWallet(sender_address, sender_key, owner_address, owner_key, contract_address, contract_abi, deposit_amount, withdraw_amount):

    ### Connect to local blockchain instance 
    session = Web3(Web3.HTTPProvider(RPC_SERVER))

    ### Create contract instance 
    instance = session.eth.contract(address=contract_address, abi=contract_abi)

    ### Get and print the initial balances
    initial_contract_balance = instance.functions.get_contract_balance().call() / 10**18
    initial_owner_balance = session.eth.get_balance(owner_address) / 10**18
    initial_sender_balance = session.eth.get_balance(sender_address) / 10**18
    print("Initial contract balance (ETH) \n" + str(initial_contract_balance) + "\n") 
    print("Initial owner balance (ETH) \n" + str(initial_owner_balance) + "\n")
    print("Initial sender balance (ETH) \n" + str(initial_sender_balance) + "\n")
    
    ### Build, sign and deploy the deposit transaction 
    nonce = session.eth.get_transaction_count(sender_address)
    tx = instance.functions.deposit().build_transaction(
        {'chainId' : CHAIN_ID, 'from' : sender_address, "nonce" : nonce, "gasPrice" : session.eth.gas_price, "value" : deposit_amount})
    signed_tx = session.eth.account.sign_transaction(tx, private_key = sender_key)
    tx_hash = session.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = session.eth.wait_for_transaction_receipt(tx_hash) 

    ### Get and print the resulting balances
    post_deposit_contract_balance = instance.functions.get_contract_balance().call() / 10**18
    post_deposit_owner_balance = session.eth.get_balance(owner_address) / 10**18
    post_deposit_sender_balance = session.eth.get_balance(sender_address) / 10**18
    gas_used_for_deposit = (initial_sender_balance - post_deposit_sender_balance - (deposit_amount/10**18))
    print("Contract balance after deposit (ETH) \n" + str(post_deposit_contract_balance) + "\n")
    print("Owner balance after deposit (ETH) \n" + str(post_deposit_owner_balance) + "\n")
    print("Sender balance after deposit (ETH) \n" + str(post_deposit_sender_balance) + "\n")
    print("Gas used to deposit " + str(deposit_amount / 10**18) + " (ETH) from contract (WEI/GWEI) \n" + str(gas_used_for_deposit*10**18) + 
          " / " + str(gas_used_for_deposit * 10**9) + "\n")
    
    # Contract balance should increase by the amount sent, sender address should decrease by the amount sent + gas 
    # and the owner balance should remain unchanged.

    ### Now lets withdraw the 1 ETH from the contract to the owner's address

    ### Create new contract instance 
    instance2 = session.eth.contract(address=contract_address, abi=contract_abi)
    
    ### Build, sign and deploy the withdraw transaction
    nonce2 = session.eth.get_transaction_count(owner_address)
    tx2 = instance2.functions.withdraw(withdraw_amount).build_transaction(
        {'chainId' : CHAIN_ID, 'from' : owner_address, "nonce" : nonce2, "gasPrice" : session.eth.gas_price})
    signed_tx2 = session.eth.account.sign_transaction(tx2, private_key = owner_key)
    tx_hash2 = session.eth.send_raw_transaction(signed_tx2.rawTransaction)
    tx_receipt2 = session.eth.wait_for_transaction_receipt(tx_hash2) 
    
    ### Get and print the resulting balances
    post_withdrawal_contract_balance = instance2.functions.get_contract_balance().call() / 10**18
    post_withdrawal_owner_balance = session.eth.get_balance(owner_address) / 10**18
    post_withdrawal_sender_balance = session.eth.get_balance(sender_address) / 10**18
    gas_used_for_withdrawal = (post_deposit_owner_balance - post_withdrawal_owner_balance + (withdraw_amount/10**18))
    print("Contract balance after withdrawal (ETH) \n" + str(post_withdrawal_contract_balance) + "\n")
    print("Owner balance after withdrawal (ETH) \n" + str(post_withdrawal_owner_balance) + "\n")
    print("Sender balance after withdrawal (ETH) \n" + str(post_withdrawal_sender_balance) + "\n")
    print("Gas used to withdraw " + str(withdraw_amount / 10**18) + " (ETH) from contract (WEI/GWEI) \n" + str(gas_used_for_withdrawal * 10**18) +
          " / " + str(gas_used_for_withdrawal * 10**9) + "\n")

    # Sender balance should be unchanged, owner balance should be increased by the withdrawn amount - gas 
    # and contract balance should decrease by the amount withdrawn. 