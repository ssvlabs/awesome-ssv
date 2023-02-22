const fs = require("fs");

module.exports = async ({ getNamedAccounts, deployments }) => {
  const { deploy } = deployments;
  const { deployer } = await getNamedAccounts();

  const whitelist = "0x123465f75D79AdAEde008E978208cb2Cc28E8B04";
  const withdrawalCreds = "0x123465f75D79AdAEde008E978208cb2Cc28E8B04";
  const operatorIds = [1, 2, 9, 42];

  const depositContract = "0xff50ed3d0ec03ac01d4c79aad74928bff48a7b2b";
  const ssvNetworkContract = "0xb9e155e65B5c4D66df28Da8E9a0957f06F11Bc04";
  const ssvTokenAddress = "0x3a9f01091C446bdE031E39ea8354647AFef091E7";

  const stakingPool = await deploy("StakingPool", {
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

  // Write address and abi to external js file
  fs.writeFileSync(
    "../react-app/src/contracts/localhost/stakingPool.js",
    `module.exports = { address: "${
      stakingPool.address
    }", abi: ${JSON.stringify(stakingPool.abi)} }`
  );
};

module.exports.tags = ["StakingPool"];
