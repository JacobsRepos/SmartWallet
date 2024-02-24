// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0; // Version >= 0.8.0 in line with our compiler version

contract Greeter {

    string public greeting; // Initialise the greeting

    // constructor() functions are ran upon deployment, our constructor initalises the 
    // greeting as "Hello"

    constructor() public {
        greeting = 'Hello';
    }

    // A write function to update the greeting, should be pretty self explanatory. 
    // This will require gas to run as we're writing to the blockchain. 

    function setGreeting(string memory _greeting) public {
        greeting = _greeting;
    }

    // A read function to fetch the greeting, won't require gas to run as we are not 
    // writing anything new to the blockchain, keyword view indicates this. 

    function greet() view public returns (string memory) {
        return greeting;
    }

}