pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

import "./interfaces/IRoEth.sol";
import "./interfaces/ICommon.sol";

contract RoEth is ERC20, IRoEth {
    address minter;
    uint256 public share_price=1e18;
    ICommon immutable CommonContract;
    constructor(address common) ERC20("staked eth with garuda", "roETH"){
        CommonContract = ICommon(common);
    }

    function setMinter(address minter_address) external {
        require(msg.sender == CommonContract.getAdmin(),"Only admin can set this");
        minter = minter_address;
    }

    function mint(address recipient, uint256 amount) override external {
        require(msg.sender == minter, "only minter can mint");
        _mint(recipient, amount);
    }

    function changeSharePrice(uint256 new_price) external {
        require(msg.sender == CommonContract.getOracle(), "only oracle can change the price");
        share_price = new_price;
    }
    function sharePrice() override external view returns (uint256)
    {
        return share_price;
    }

}
