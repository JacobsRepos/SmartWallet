# Setup 

To set everything up we will first deploy and use the Greeter.sol contract. Once this is done we can move on to more exciting contracts. 

### Setting up the environment 

We will use a virtual environment set up in the project folder for debugging purposes. To set up a local virtual environment one must: 

- Navigate to the project folder in the CLI via 
  - cd PROJECT_PATH 
- Initialise the virtual environment instance via 
  - python3 -m venv VENVNAME 
  - I use .venv as my VENVNAME, the period keeps it hidden. 
- Activate the virtual environment 
  - source VENVNAME/bin/activate

Once the environment is activated, we can begin feeding it packages, I recommend PIP as a package manager. 

### Installing packages

The packages we'll be using are: 

- web3.py, our python interface for interacting with the eth blockchain. Read the docs [here.](https://web3py.readthedocs.io/en/stable/) Install via
  - pip install web3
- dotenv, this is how we'll interact with the .env file to keep keys secure. Read the docs [here.](https://pypi.org/project/python-dotenv/) Install via 
    - pip install python-dotenv
- py-solc-x, our python wrapper for the solidity compiler. Read the docs [here.](https://pypi.org/project/py-solc-x/) Install via 
  - pip install py-solc-x

### Setting up the Ganache command line interface 

We will use the Ganache CLI for our local blockchain instance. You can [read up on Ganache here.](https://trufflesuite.com/docs/ganache/) To set up Ganache we first must have Node.js installed (>=v8).

##### Node.js 
This is the javascript runtime environment we'll be using to host and interact with the Ganache local blockchain. If you're not yet familiar with Node.js it is highly recommended you read up on it [here.](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs) To install on MacOS we can use homebrew. 

- brew install node 

An elementary background in javascript is also highly recommended. Theres a myriad of resources to do so, I leave it to the reader to choose the most appropriate source. 

Node.js comes with the npm javascript package manager, this is what we'll use to install the Ganache CLI. 

##### Installing the Ganache CLI 
Once Node.js is installed we can install the Ganache CLI via 
- npm install -g ganache-cli 

##### Using the Ganache CLI
Now we can set up our local blockchain instance. Ganache has the desirable property of automatic mainnet forking. Namely, when we initialise our blockchain instance it automatically forks the latest ethereum blockchain instance. To initialise simply run 

- ganache-cli
  
In the command line. It will output the addresses of 10 wallets (each with 100 ETH), each wallets respective private key, the gas data at the time of creating our instance and the RPC server we're listening on. Read up on the Ganache CLI [here.](https://github.com/trufflesuite/ganache#readme)

### The .env file

Here is where we'll store our wallet keys, ensuring that they are not accessible by a bad actor with access to our code. While it doesn't matter in the testing environment it is a crucial step in all blockchain development, and we carry out this step for the sake of building good implementation habits. 

When uploading projects to github ensure the .env is in the .gitignore file, otherwise this entire process is redundant!! 

### Writing the Greeter contract

Now we can write our contract, see the Greeter.sol file for a full implementation. I 
commented the code extensively for newer solidity devs to follow along.

### Deploying and testing the greeter contract in python

Now one should be able to run Greeter.py to both deploy and test the contract. This code is also well commented, it is recommended to read through each comment carefully to understand the deployment/testing process. You will be carrying out such a process for each contract you wish to test locally. 

### Uploading your project to github

For the sake of completeness I'll also show how one could upload a local project to github via the commandline. This code is for MacOS, though for other operating systems it'll be largely the same. 

I will assume you already have git and gh installed in the command line. In MacOS this can be done via brew. 

##### Authentication 

To authenticate yourself via logging in the command lineone can 
- gh auth login 
and then just follow the instructions given. For alternative ways of logging in see 
- https://docs.github.com/en/get-started/getting-started-with-git/set-up-git

##### Uploading your local project

- Navigate to the project path
  - cd PROJECT_PATH
- Initialise the git repo 
  - git init
- Create your README markdown file
  - touch README.md 
- Write things to the README.md 
  - echo "Text you want people to read" >> README.md
- Create your .gitignore file 
  - touch .gitignore.txt
- Add files to the .gitignore, for example we want the .env in the gitignore
  - echo ".env" >> .gitignore
- Add folders to the .gitignore, for example we dont want to upload the venv to git
  - echo ".venv/" >> .gitignore
- Get git to track all the remaining files 
  - git add --A
- Commit all the tracked files with a commit message 
  - git commit -m "First commit!"
- Push the commit, default branch name is main but I had issues and made it master
  - git push -u origin BRANCHNAME

Now your project should be up on github :)