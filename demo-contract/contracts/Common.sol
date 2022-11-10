pragma solidity ^0.8.0;

import "./interfaces/ICommon.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract Common is ICommon, Ownable {
    address public RoETH;
    address public StakingPool;
    address public Oracle;

    event RoETHAddressChanges(address new_address);
    event StakingPoolAddressChanges(address new_address);
    event OracleAddressChanges(address new_address);


    function changeStakingPool(address new_address) override onlyOwner external {
        StakingPool = new_address;
        emit StakingPoolAddressChanges(new_address);
    }

    function getAdmin() override external view returns(address){
        return owner();
    }
    function changeRoETH(address new_address) override onlyOwner external {
        RoETH = new_address;
        emit RoETHAddressChanges(new_address);
    }
    function changeOracle(address new_address) override onlyOwner external {
        Oracle = new_address;
        emit OracleAddressChanges(new_address);
    }

    function getRoETH() override external view returns (address){
        return RoETH;
    }

    function getStakingPool() override external view returns (address){
        return StakingPool;
    }

    function getOracle() override external view returns (address){
        return Oracle;
    }
}
