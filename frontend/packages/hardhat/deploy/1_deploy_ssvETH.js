const hre = require("hardhat");

const fs = require("fs");

const path = require("path");

const localChainId = "31337";

module.exports = async ({ deployments, getChainId }) => {
  const chainId = await getChainId();
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

  const ssvETHContract = await hre.ethers.getContractAt(
    ssvETHAbi,
    ssvETHAddress
  );
  // Create folder if it doesn't exist
  const dir =
    chainId === localChainId
      ? path.join(
          __dirname,
          "..",
          "..",
          "react-app",
          "src",
          "contracts",
          "localhost"
        )
      : path.join(
          __dirname,
          "..",
          "..",
          "react-app",
          "src",
          "contracts",
          "goerli"
        );
  fs.mkdirSync(dir, { recursive: true });
  // Export the ssvETH object to a JavaScript file
  const ssvETHObjectPath = path.join(dir, "ssvETH.js");
  const ssvETHObjectContent = `module.exports = {\n  address: "${ssvETHAddress}",\n  abi: ${JSON.stringify(
    ssvETHAbi
  )},\n};`;
  fs.writeFileSync(ssvETHObjectPath, ssvETHObjectContent);

  return { ssvETH: ssvETHContract };
};
module.exports.tags = ["ssvETH"];
