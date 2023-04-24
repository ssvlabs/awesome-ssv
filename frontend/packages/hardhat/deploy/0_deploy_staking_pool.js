const hre = require("hardhat");

const localChainId = "31337";

module.exports = async ({ getNamedAccounts, deployments, getChainId }) => {
  const { deploy } = deployments;
  const { deployer } = await getNamedAccounts();
  const keyGenerator = "0x123465f75D79AdAEde008E978208cb2Cc28E8B04";
  const withdrawal = "0x123465f75D79AdAEde008E978208cb2Cc28E8B04";
  const operatorIds = [1, 2, 9, 42];

  const depositAddress = "0xff50ed3d0ec03ac01d4c79aad74928bff48a7b2b";
  const ssvNetworkContract = "0xAfdb141Dd99b5a101065f40e3D7636262dce65b3";
  const ssvTokenAddress = "0x3a9f01091C446bdE031E39ea8354647AFef091E7";

  const stakingpool = await deploy("StakingPool", {
    from: deployer,
    args: [
      keyGenerator,
      depositAddress,
      withdrawal,
      ssvNetworkContract,
      ssvTokenAddress,
      operatorIds,
    ],
    log: true,
  });

  console.log(`StakingPool deployed to ${stakingpool.address}`);
  
};
module.exports.tags = ["StakingPool"];
