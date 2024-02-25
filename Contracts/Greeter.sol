// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0; // Version >= 0.8.0 in line with our compiler version

contract Greeter {

    string public greeting; // Initialise the greeting, variable is stored on the contract.

    // constructor() functions are ran upon deployment, our constructor initalises the greeting as "Hello"
    // They work like main() functions in c++ if you're familiar with these. 
    constructor() public {
        greeting = 'Hello';
    }

    // This will update the greeting, and thus as we're writing to the blockchain it will require gas to run. 
    // The memory keyword indicates _greeting, our new greeting isn't to be stored in the contract, only in the method, 
    // and we instead overwrite the already stored greeting string. 
    function set_greeting(string memory _greeting) public {
        greeting = _greeting;
    }

    // This function will access and return the greeting, we don't do any writing (hence the view keyword) 
    // so this won't require gas to run. 
    function greet() view public returns (string memory) {
        return greeting;
    }

}