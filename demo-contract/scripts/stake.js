const {ethers, upgrades} = require("hardhat");


async function main() {

    // TODO change poolAddress, for your pool address just printed on your console 
    const stakingPoolAddress = "0xBBec5E55b31a2e1bAA1f6048cFaDb687CAA0A357";
    let StakingPool = await ethers.getContractAt("StakingPool", stakingPoolAddress);

    console.log("staking...")
    tx = await StakingPool.stake({value: ethers.utils.parseEther("32.01")});
    await tx.wait(); 

    console.log("tx:", tx.hash);

}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });