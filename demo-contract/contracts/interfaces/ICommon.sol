pragma solidity ^0.8.0;

interface ICommon {

    function changeStakingPool(address new_address) external;

    function getAdmin() external view returns (address);

    function changeRoETH(address new_address)  external;

    function changeOracle(address new_address)  external;

    function getRoETH() external  view returns (address);

    function getStakingPool() external  view returns (address);

    function getOracle() external  view returns (address);


}
