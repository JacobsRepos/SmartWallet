import os
import json
from Interactions.deploy_Greeter import deploy_Greeter
from Interactions.test_Greeter import test_Greeter
from Interactions.deploy_SmartWallet import deploy_SmartWallet
from Interactions.test_SmartWallet import test_SmartWallet

### Get in the address/key pair we wish to deploy the Greeter contract to, I use Wallet 0 from my Ganache instance.
address = "0xd7D0de6B55f056dB3c44A44fa6a925FaA2851186"
key = os.getenv("WALLET0_KEY")

### Get in our owner and sender address/key pairs, I use Wallet 1 and 2 from my Ganache instance.
owner_address = "0x4FA38505Ed103cDef973d37F6B8ddB72eaCD1146"
sender_address = "0x3647b739d2adD66934cE3290603522B0AF6E1933"
owner_key = os.getenv('WALLET1_KEY')
sender_key = os.getenv('WALLET2_KEY')

### Deploy the greeter contract to the blockchain
deploy_Greeter(address=address, key=key)
    
### Read in the Greeter contract address & ABI from the DeployedGreeter json file
with open("./Contracts/DeployedGreeter.json", "r") as file: 
    DeployedGreeter_dict = json.loads(file.read())
    DeployedGreeter_abi = DeployedGreeter_dict["abi"]
    DeployedGreeter_address = DeployedGreeter_dict["address"]
    file.close() # Remember to always close your files when you're done with them :) 

### Test the Greeter contract, should print "Hello" followed by "Ciao" if all is working well. 
test_Greeter(address=address, key=key, contract_address=DeployedGreeter_address, abi=DeployedGreeter_abi)

### Deploy the SmartWallet contract to the blockchain
deploy_SmartWallet(owner_address=owner_address, owner_key=owner_key)

### Read in the SmartWallet contract address & ABI from the DeployedSmartWallet
with open("./Contracts/DeployedSmartWallet.json", "r") as file: 
    SmartWallet_dict = json.loads(file.read())
    SmartWallet_abi = SmartWallet_dict['abi']
    SmartWallet_address = SmartWallet_dict['address']
    file.close()

### Test the SmartWallet contract, the correct outputs should be clear according to your input params
# Note we deposit / withdraw WEI not ETH, one ETH is 10^18 WEI
deposit_amount = 10**18 
withdrawn_amount = 10**18
test_SmartWallet(sender_address=sender_address, sender_key=sender_key, owner_address=owner_address, owner_key=owner_key, 
                 contract_address=SmartWallet_address, contract_abi=SmartWallet_abi, deposit_amount=deposit_amount, withdraw_amount=withdrawn_amount) 

