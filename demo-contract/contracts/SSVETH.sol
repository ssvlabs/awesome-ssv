pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

// import "./interfaces/IRoEth.sol";
// import "./interfaces/ICommon.sol";

contract SSVETH is ERC20, Ownable {
    address public minter;
    uint256 public sharePrice = 1e18;


    // ICommon immutable CommonContract;
    constructor() ERC20("decentralize staking with ssv", "ssvETH"){
        minter = msg.sender;
    }

    // function setMinter(address minter_address) external {
    //     require(msg.sender == CommonContract.getAdmin(),"Only admin can set this");
    //     minter = minter_address;
    // }

    function mint(address recipient, uint256 amount) external onlyOwner {
        _mint(recipient, amount);
    }


    function changeSharePrice(uint256 new_price) external onlyOwner {
        sharePrice = new_price;
    }

    // TODO //
    // ?? add events? 

    // function sharePrice() override external view returns (uint256)
    // {
    //     return share_price;
    // }

}
