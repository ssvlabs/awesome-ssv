const {ethers, upgrades} = require("hardhat");


async function main() {
    const SSVETH = await ethers.getContractFactory("SSVETH");
    // const Common = await ethers.getContractFactory("Common");
    // const KeysManager = await ethers.getContractFactory("KeysManager");
    const StakingPoolABI = await ethers.getContractFactory("StakingPool");
    // OPTIONAL you can change your SSV operators here
    const operator_ids = [1, 2, 9, 42]
    // TODO change whitelist to address you will making tx to staking pool and keysmanager, probably your current depolyer
    const whitelist = "0x0000536dbD99d918092249Ef4eDe4a69A35CccCa"
    // OPTIONAL change to receive eth rewards
    const withdrawal_creds = "0x0000536dbD99d918092249Ef4eDe4a69A35CccCa"
    const deposit_contract = "0xff50ed3d0ec03ac01d4c79aad74928bff48a7b2b"
    const ssv_network_contract = "0xb9e155e65B5c4D66df28Da8E9a0957f06F11Bc04"
    const ssv_token_address = "0x3a9f01091C446bdE031E39ea8354647AFef091E7";
    // const oracle_address = "0xfabb0ac9d68b0b445fb7357272ff202c5651694a"

    console.log("deploying ssvETH...");
    const ssvETH = await SSVETH.deploy();
    await ssvETH.deployed();
    // const ssvETH = await ssvETH.attach("0x7a2088a1bFc9d81c55368AE168C2C02570cB814F");
    console.log("ssvETH deployed to:", ssvETH.address)

    // const common = await Common.deploy();
    // console.log("Common contract deployed to:", common.address)

    console.log("deploying staking Pool...");
    const stakingPool = await StakingPoolABI.deploy(whitelist, deposit_contract, withdrawal_creds, ssv_network_contract, ssv_token_address, ssvETH.address, operator_ids);
    await stakingPool.deployed();
    console.log("staking pool deployed to:", stakingPool.address)
    // tx = await ssvETH.setMinter(stakingpool.address);
    // await tx.wait()



    // console.log("adding values in common contract")
    // tx = await common.changeStakingPool(stakingpool.address);
    // await tx.wait();
    // tx = await common.changeRoETH(roETH.address);
    // await tx.wait();

    // tx = await common.changeOracle(oracle_address);
    // await tx.wait();


    // console.log("added values in common contract");
    // console.log(await common.getAdmin());


}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });