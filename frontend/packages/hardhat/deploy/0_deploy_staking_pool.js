const hre = require("hardhat");

const localChainId = "31337";

module.exports = async ({ getNamedAccounts, deployments, getChainId }) => {
  const { deploy } = deployments;
  const { deployer } = await getNamedAccounts();
  const chainId = await getChainId();
  const whitelist = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266";
  const withdrawalCreds = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266";
  const operatorIds = [1, 2, 9, 42];

  const depositContract = "0xff50ed3d0ec03ac01d4c79aad74928bff48a7b2b";
  const ssvNetworkContract = "0xb9e155e65B5c4D66df28Da8E9a0957f06F11Bc04";
  const ssvTokenAddress = "0x3a9f01091C446bdE031E39ea8354647AFef091E7";

  const stakingpool = await deploy("StakingPool", {
    from: deployer,
    args: [
      whitelist,
      depositContract,
      withdrawalCreds,
      ssvNetworkContract,
      ssvTokenAddress,
      operatorIds,
    ],
    log: true,
  });

  console.log(`StakingPool deployed to ${stakingpool.address}`);
  
};
module.exports.tags = ["StakingPool"];
