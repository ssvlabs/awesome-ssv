const { ethers } = require("hardhat");

async function fundStakingPool() {
  // Connect to the deployed StakingPool contract
  const stakingPoolAddress = "0x00aDF33c3c3D4f9f9f3dB54aA6Ad81FD31bA7f2b"; // <-- replace this with your staking pool contract address
  const stakingPoolContract = await ethers.getContractAt(
    "StakingPool",
    stakingPoolAddress
  );

  const amount = ethers.utils.parseEther("62");
  await stakingPoolContract.stake({ value: amount });

  console.log(
    "Funded Staking Pool with",
    ethers.utils.formatEther(amount),
    "ether."
  );
}

fundStakingPool()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
