// SPDX-License-Identifier: GPL-3.0
pragma solidity >= 0.8.0;

contract Greeter {
    string greeting;

    constructor() {
        greeting = 'Hello';
    }

    function setGreeting(string memory new_greet) public {
        greeting = new_greet;
    }

    function greet() view public returns (string memory) {
        return greeting;
    }
}