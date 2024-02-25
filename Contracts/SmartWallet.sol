// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0; 

contract SmartWallet {
    address payable public owner;

    constructor() payable {
        owner = payable(msg.sender);
    }
    
    function deposit() external payable {}
    
    function withdraw(uint256 _amount) public {
       // require(msg.sender == owner)
        require(_amount <= address(this).balance, "Can't withdraw more ETH than is in the contract");
        address payable to = payable(msg.sender);
        to.transfer(_amount);
    }

    function get_contract_balance() external view returns (uint256){
        return address(this).balance;
    }
}   

