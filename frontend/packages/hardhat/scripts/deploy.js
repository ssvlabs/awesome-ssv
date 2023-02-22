// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.
const hre = require("hardhat");
const fs = require("fs");

async function main() {
  const whitelist = "0x123465f75D79AdAEde008E978208cb2Cc28E8B04";
  const withdrawalCreds = "0x123465f75D79AdAEde008E978208cb2Cc28E8B04";
  const operatorIds = [1, 2, 9, 42];

  const depositContract = "0xff50ed3d0ec03ac01d4c79aad74928bff48a7b2b";
  const ssvNetworkContract = "0xb9e155e65B5c4D66df28Da8E9a0957f06F11Bc04";
  const ssvTokenAddress = "0x3a9f01091C446bdE031E39ea8354647AFef091E7";

  const StakingPool = await hre.ethers.getContractFactory("StakingPool");
  const stakingpool = await StakingPool.deploy(
    whitelist,
    depositContract,
    withdrawalCreds,
    ssvNetworkContract,
    ssvTokenAddress,
    operatorIds
  );

  await stakingpool.deployed();

  console.log(`StakingPool deployed to ${stakingpool.address}`);

  const stakingPoolartifact = await hre.artifacts.readArtifact("StakingPool");
  const ssvETHArtifact = await hre.artifacts.readArtifact("SSVETH");

  const stakingPoolAbi = stakingPoolartifact.abi;
  const ssvETHAbi = ssvETHArtifact.abi;

  // Write address and abi to external js file
  fs.writeFileSync(
    "../react-app/src/contracts/goerli/stakingPool.js",
    `module.exports = { address: "${
      stakingpool.address
    }", abi: ${JSON.stringify(stakingPoolAbi)} }`
  );

  const ssvETHAddress = await stakingpool.ssvETH();
  console.log("ssvETHAddress", ssvETHAddress);

  const ssvETHContract = await hre.ethers.getContractAt(
    ssvETHAbi,
    ssvETHAddress
  );

  // Write address and abi to external js file
  fs.writeFileSync(
    "../react-app/src/contracts/goerli/ssvETH.js",
    `module.exports = { address: "${
      ssvETHContract.address
    }", abi: ${JSON.stringify(ssvETHAbi)} }`
  );
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
