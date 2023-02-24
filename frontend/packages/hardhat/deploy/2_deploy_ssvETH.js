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

  // Create localhost folder if it doesn't exist
  const localhostDir = path.join(
    __dirname,
    "..",
    "..",
    "react-app",
    "src",
    "contracts",
    "localhost"
  );
  fs.mkdirSync(localhostDir, { recursive: true });

  // Export the ssvETH object to a JavaScript file
  const ssvETHObjectPath = path.join(localhostDir, "ssvETH.js");
  const ssvETHObjectContent = `module.exports = {\n  address: "${ssvETHAddress}",\n  abi: ${JSON.stringify(
    ssvETHAbi
  )},\n};`;
  fs.writeFileSync(ssvETHObjectPath, ssvETHObjectContent);

  const ssvETHContract = await hre.ethers.getContractAt(
    ssvETHAbi,
    ssvETHAddress
  );

  return { ssvETH: ssvETHContract };
};
module.exports.tags = ["ssvETH"];
