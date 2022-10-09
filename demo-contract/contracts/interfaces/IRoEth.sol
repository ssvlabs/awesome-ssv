pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IRoEth is IERC20{
    function sharePrice() external view returns (uint256 amount);

    function mint(address user, uint256 amount) external;

//    function burn(address user, uint256 amount) external;

}