const { ethers, upgrades } = require("hardhat");




async function main() {

    // TODO change poolAddress, for your pool address just printed on your console 
    const poolAddress = "0xBBec5E55b31a2e1bAA1f6048cFaDb687CAA0A357";
    const ssvAddress = "0x3a9f01091C446bdE031E39ea8354647AFef091E7";
    let ssv_token = await ethers.getContractAt("IERC20", ssvAddress);

    console.log("transferring...")
    tx = await ssv_token.transfer(poolAddress, ethers.utils.parseEther("50"));
    await tx.wait();
    console.log("tx:", tx.hash);


}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });