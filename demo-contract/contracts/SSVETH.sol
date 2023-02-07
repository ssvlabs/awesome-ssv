//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SSVETH is ERC20, Ownable {
    address public minter;

    // ICommon immutable CommonContract;
    constructor() ERC20("decentralize staking with ssv", "ssvETH"){
        minter = msg.sender;
    }


    function mint(address recipient, uint256 amount) external onlyOwner {
        _mint(recipient, amount);
    }

}
