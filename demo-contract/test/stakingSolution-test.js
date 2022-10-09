const {ethers, network, upgrades} = require("hardhat");
const {expect} = require("chai");
const {utils} = require("ethers");
const hre = require("hardhat");
const {defaultAccounts} = require("ethereum-waffle");
const {BigNumber, constants} = ethers;
const {AddressZero, MaxUint256, MaxInt256} = constants;

const approveMAX = async (erc20, signer, to, amount) => {
    if ((await erc20.allowance(signer.address, to)).lt(amount)) {
        let tx = await erc20.connect(signer).approve(to, MaxUint256);
        await tx.wait();
    }
};

const balanceOf = async (erc20, userAddress) => {
    return await erc20.balanceOf(userAddress);
};

const rpcCall = async (callType, params) => {
    return await network.provider.request({
        method: callType,
        params: params,
    });
};

const snapshot = async () => {
    return await rpcCall("evm_snapshot", []);
};

const revertToSnapshot = async (snapId) => {
    return await rpcCall("evm_revert", [snapId]);
};

const increaseTime = async (seconds) => {
    await network.provider.send("evm_increaseTime", [seconds]);
    await network.provider.send("evm_mine");
};

describe("contracts", function (){
    let defaultSigner, user1, user2, oracle, whitelistt;
    let stakingpool,keysmanager,roeth,common
    before(async function (){
        [
            defaultSigner,
            user1,
            user2,
            oracle,
            whitelistt,
        ] = await ethers.getSigners();

        const RoEth = await ethers.getContractFactory("RoEth");
        const Common = await ethers.getContractFactory("Common");
        const KeysManager = await ethers.getContractFactory("KeysManager");
        const StakingPool = await ethers.getContractFactory("StakingPool");

        const common = await Common.deploy();
        console.log("Common contract deployed to:", common.address)
        const roETH = await RoEth.deploy(common.address);
        // const roETH = await RoEth.attach("0x7a2088a1bFc9d81c55368AE168C2C02570cB814F");

        console.log("roETH deployed to:", roETH.address)
        const stakingpool = await StakingPool.deploy(whitelistt.address, "0x2279B7A0a67DB372996a5FaB50D91eAA73d2eBe6", common.address, "0xfabb0ac9d68b0b445fb7357272ff202c5651694a");
        console.log("staking pool deployed to:", stakingpool.address)
        const keymanager = await KeysManager.deploy("0xa513E6E4b8f2a923D98304ec87F64353C4D5C853", "0x0165878A594ca255338adfa4d48449f69242Eb8F", whitelistt.address, [1, 2, 9, 191])
        // const keymanager = await KeysManager.attach("0xc5a5C42992dECbae36851359345FE25997F5C42d")
        console.log("keysmanager deployed to:", keymanager.address)
        // console.log(await keymanager.getOperators())

        tx = await roETH.setMinter(stakingpool.address);
        await tx.wait()
        console.log("adding values in common contract")
        tx = await common.changeStakingPool(stakingpool.address);
        await tx.wait();
        tx = await common.changeRoETH(roETH.address);
        await tx.wait();

        tx = await common.changeOracle("0xfabb0ac9d68b0b445fb7357272ff202c5651694a");
        await tx.wait();

        tx = await common.changeKeysManager(keymanager.address);
        await tx.wait();

        console.log("added values in common contract");
        console.log(await common.getAdmin());
    })
    beforeEach(async function () {
        snapshotId = await snapshot();
    });

    afterEach(async function () {
        await revertToSnapshot(snapshotId);
    });
    describe("keysmanager",function (){
        it("should add keys to ")
    })
})



