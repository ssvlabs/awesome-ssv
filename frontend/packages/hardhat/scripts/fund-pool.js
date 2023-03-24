const { ethers } = require("hardhat");

async function fundStakingPool() {
  // Connect to the deployed StakingPool contract
  const stakingPoolAddress = "0x4e850C82E0512B4Edcd00F8C993f3fb9dEA3e7e3"; // <-- replace this with your staking pool contract address
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
