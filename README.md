# Table of contents 
- [Table of contents](#table-of-contents)
- [Project\_Description](#project_description)
- [Setup](#setup)
    - [Environment\_Setup](#environment_setup)
    - [Installing\_Packages](#installing_packages)
    - [Ganache\_CLI](#ganache_cli)
        - [Node.js](#nodejs)
        - [Installing the Ganache CLI](#installing-the-ganache-cli)
        - [Using the Ganache CLI](#using-the-ganache-cli)
    - [.env\_files](#env_files)
- [Greeter](#greeter)
    - [Writing\_Greeter](#writing_greeter)
    - [Deploying\_Greeter](#deploying_greeter)
    - [Testing\_Greeter](#testing_greeter)
- [SmartWallet](#smartwallet)
    - [Writing\_SmartWallet](#writing_smartwallet)
    - [Deploying\_SmartWallet](#deploying_smartwallet)
    - [Testing\_SmartWallet](#testing_smartwallet)

# Project_Description

The aim of this project is to provide beginner smart contract developers the tools required to develop and test their contracts on a local blockchain instance, using python to interact with said blockchain and to compile the contracts. We will begin by setting up our workspace, which will include setting up Ganache as our local blockchain instance. Then we will deploy and test out the Greeter contract seen throughout the web3.py docs. This step acts as a test to check our working environment is set up correctly. Then we will move on to the juicier SmartWallet contract, which will allow us to send ETH to a smart contract stored on the blockchain, and further to withdraw it to the contract owner's wallet.

# Setup 

Here I outline the working environment I elect to use for local smart contract testing. Follow these steps and you (should) be able to use the Greeter and SmartWallet contracts freely. I only added the Greeter contract for ease of testing, the contract is used frequently in the Web3.py notes for documentation examples and thus should be the easiest contract to use for debugging. 

### Environment_Setup 

I use a virtual environment set up in the project folder for debugging purposes. To set up a local virtual environment one can: 

- Navigate to the project folder in the CLI via 
  - cd PROJECT_PATH 
- Initialise the virtual environment instance via 
  - python3 -m venv VENVNAME 
  - I use .venv as my VENVNAME, the period keeps it hidden in the file explorer. 
- Activate the virtual environment 
  - source VENVNAME/bin/activate

Once the environment is activated, we can begin feeding it packages, I recommend PIP as a package manager. I put mine in the gitignore, do it yourself you lazy... 

### Installing_Packages

The packages we'll be using are: 

- web3.py, our python interface for interacting with the eth blockchain. Read the docs [here.](https://web3py.readthedocs.io/en/stable/) Install via
  - pip install web3
- dotenv, this is how we'll interact with the .env file. Read the docs [here.](https://pypi.org/project/python-dotenv/) Install via 
    - pip install python-dotenv
- py-solc-x, a python wrapper for the solidity compiler. Read the docs [here.](https://pypi.org/project/py-solc-x/) Install via 
  - pip install py-solc-x
  - You'll need solidity installed to actually use this wrapper, on MacOS one can just "brew install solidity"

Use PIP as your package manager, its by far the best python package manager. 

### Ganache_CLI

We will use the Ganache CLI for our local blockchain instance. You can [read up on Ganache here.](https://trufflesuite.com/docs/ganache/) To set up Ganache we first must have Node.js installed (>=v8).

##### Node.js 

This is the javascript runtime environment used to host and interact with the Ganache local blockchain. If you're not yet familiar with Node.js it is recommended you read up on it [here.](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs) To install on MacOS we can use homebrew. 

- brew install node 

Node.js comes with the npm javascript package manager, this is what we'll use to install the Ganache CLI. If you know nothing of Node.js this is all you really need to know about to proceed. 

##### Installing the Ganache CLI 

Once Node.js is installed we can install the Ganache CLI via 
- npm install -g ganache-cli 

##### Using the Ganache CLI

Once installed we can set up our local blockchain instance. Ganache has the desirable property of automatic mainnet forking. Namely, when we initialise our blockchain instance it automatically forks the latest ethereum blockchain instance. To initialise simply run 
- ganache-cli
In the command line. It will output the addresses of 10 wallets (each with 100 ETH), each wallets respective private key, the gas data at the time of creating our instance and the RPC server we're listening on. Read up on the Ganache CLI [here.](https://github.com/trufflesuite/ganache#readme)

### .env_files

Here is where we'll store our wallet keys, ensuring that they are not accessible by a bad actor with access to our code. Simply create a
file called ".env" and add your private variables as: 
- VARIABLE_NAME=VARIABLE
Capitalised variable names are a convention, note everything is automatically a string so just paste in the wallet key directly. No spaces!

When uploading projects to github ensure the .env is in the .gitignore file, otherwise this entire process is redundant!! 

# Greeter

### Writing_Greeter

See greeter.sol for an implementation with detailed comments. This contract: 
- Stores a string called greeting.
- Has a function called set_greeting which takes in a new string to write to the greeting variable.
- Has a function called greet which returns the currently stored greeting.
  
This minimalist contract allows us to test pretty much everything we need to see if our working environment is working ok as we test:

- Variable storage (on the chain and inside methods).
- Read only functions.
- Write functions.

### Deploying_Greeter

To deploy this contract we follow the following process, again an implementation with detailed comments is found in Greeter.py 
- Load in our working variables. These are 
  - The RPC server we're listening on.
  - The Chain ID (always 1337 for Ganache environments).
  - The address, key pair of the wallet we wish to deploy the contract with (fed to the deploy function)
- Write a deployment function to upload this contract to the blockchain. The steps carried out in this function are: 
  - Read in the Greeter.sol file (returning a string containing the contract code).
  - Feed this string to the solidity compiler using compile source, returning the abi and bytecode.
    - For reusability we can store the compiled solidity file to a JSON. 
  - Connect to the blockchain using the web3 python wrapper.
  - Build the transaction which will deploy this contract.
  - Sign this transaction.
  - Send this transaction to the blockchain.
  - Wait for the transaction receipt.
  - Fetch the ABI and contract address from the receipt.
    - This will allow us to create instances of this already deployed contract down the road.

### Testing_Greeter

Once the Greeter contract is deployed to the blockchain we can test out the functionality of it by: 
- Load in our working variables, these are the same variables we needed to deploy with the addition of the: 
  - Contract's address.
  - Contract's ABI.
- Connect to the blockchain as we did before when deploying.
- Create an instance of the contract using the contract's address and ABI.
- Test out the read only function immediately by calling it and printing the result.
  - Note we don't have to go through the building, signing and sending process here as we aren't altering the blockchain.
- Build, sign and send a transaction for the set_greeting function, make sure to feed set_greeting a greeting!
  - This time we have to go through the build, sign and send process as we are altering the contract and hence the blockchain.
  - Theoretically we could also store this as a json for easy reuse, however it'll only be useful if we want to revert the greeting back to the greeting we just chose. Hence I don't bother here, worth experimenting with though! (not sure this is true, need to check)
- Recall the greet function to check our greeting did in fact change. 

# SmartWallet

Did the tests for the greeter contract run ok? If so we can now use the SmartWallet contract to set up an Ethereum wallet stored as a contract on the blockchain. As before we will write, deploy and then test this contract, with each step again well described. 

### Writing_SmartWallet

See SmartWallet.sol for an implementation with detailed commenting. This contract: 
- Stores the wallet owner's address, which will be set as the address which the contract was deployed from upon construction.
- Has a deposit function which can be called by any user, which will deposit the amount fed into the transaction minus gas. 
- Has a withdraw function which can only be called by the owner, this will withdraw the amount chosen from the contract to the owner's wallet. 
- Has a get_contract_balance function which returns the amount of ETH (stored as WEI) in the wallet. 

### Deploying_SmartWallet

We follow an identical deployment process as before, you'll want to commit this process to memory (the memory in your brain that is) in order to be an efficient smart contract developer.  

### Testing_SmartWallet

This way we interact will follow a near identical procedure as with the Greeter, we just have more functionality to test this time. The steps are: 
- Get in the contract information from the DeploySmartWallet.json file.
- Connect to the local blockchain instance and create an instance of the contract.
  - Before proceeding we'll print all the initial wallet balances (owner, sender, contract). 
  - Note we can print the contract address before sending any transactions as this is a view only function.
- Build, sign and send the transaction for deposit, feeding it the extra "value" parameter containing the amount to be deposited. 
- Print the updated balances (for the same 3 as before) and the gas used to make sure this is all working as expected. 
- Build, sign and send the transaction for withdraw, feeding it the _amount parameter containing the amount to be withdrawn. 
- Print the updated balances (you guessed it, same 3) and the gas used. Pray it works correctly, if not start crying. 