const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

module.exports = async ({ deployments }) => {
  const stakingPoolDep = await deployments.get("StakingPool");
  const stakingPoolAbi = stakingPoolDep.abi;
  const stakingPoolAddress = stakingPoolDep.address;

  const stakingPoolContract = await hre.ethers.getContractAt(
    stakingPoolAbi,
    stakingPoolAddress
  );

  const ssvETHAddress = await stakingPoolContract.ssvETH();
  console.log("ssvETHAddress", ssvETHAddress);

  const ssvETHAbi = (await deployments.getArtifact("SSVETH")).abi;

  // Export the ssvETH object to a JavaScript file
  const ssvETHObjectPath = path.join("../react-app/src/contracts/localhost/", "ssvETH.js");
  const ssvETHObjectContent = `module.exports = {\n  address: "${ssvETHAddress}",\n  abi: ${JSON.stringify(ssvETHAbi)},\n};`;
  fs.writeFileSync(ssvETHObjectPath, ssvETHObjectContent);

  const ssvETHContract = await hre.ethers.getContractAt(
    ssvETHAbi,
    ssvETHAddress
  );

  return { ssvETH: ssvETHContract };
};
module.exports.tags = ["ssvETH"];
