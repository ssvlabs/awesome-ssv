// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.

// import { ethers } from "hardhat";
// const ethers = require("hardhat");

const hre = require("hardhat");



async function main() {
  const whitelist = "0x00704A2E3EAf3992c7C9802DF0088F8BA9e4426d";
  const withdrawalCreds = "0x00704A2E3EAf3992c7C9802DF0088F8BA9e4426d";
  const operatorIds = [1, 2, 9, 42];

  const depositContract = "0xff50ed3d0ec03ac01d4c79aad74928bff48a7b2b";
  const ssvNetworkContract = "0xb9e155e65B5c4D66df28Da8E9a0957f06F11Bc04";
  const ssvTokenAddress = "0x3a9f01091C446bdE031E39ea8354647AFef091E7";
  const amount = hre.ethers.utils.parseEther("62");

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

  await stakingpool.stake({value: amount});
  console.log(`StakingPool funded`);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
