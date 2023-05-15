// const { ethers } = require("ethers");
// const hre = require("hardhat");
const { keccak256 } = require("ethers");
const { ethers } = require("ethers");

// import { ethers, keccak256 } from "hardhat";

// Generate a random mnemonic phrase
const mnemonic = ethers.Wallet.createRandom().mnemonic;

// Replace with your network provider
const providerUrl =
  "https://goerli.infura.io/v3/02c55d691047439ab33be7c7dd9da4bc";

// Replace with the deposit amount and the withdrawal credentials
const depositAmount = ethers.utils.parseEther("32").toString();
const withdrawalCredentials =
  "0x0000000000000000000000000000000000000000000000000000000000000000";

// Define the deposit contract address and ABI
const depositContractAddress = "0xff50ed3d0ec03ac01d4c79aad74928bff48a7b2b";
const depositContractAbi = [
  "function deposit(address,bytes,bytes) payable",
  "function get_deposit_count() view returns (uint256)",
];

// Create a provider instance and connect to the network
const provider = new ethers.providers.JsonRpcProvider(providerUrl);

// Create a wallet instance from the mnemonic phrase
const wallet = ethers.Wallet.fromMnemonic(mnemonic);

// Set the provider for the wallet instance
wallet.provider = provider;

// Create a contract instance for the deposit contract
const depositContract = new ethers.Contract(
  depositContractAddress,
  depositContractAbi,
  wallet
);

// Generate the deposit data
async function generateDepositData() {
  // Generate a new Ethereum 2.0 key pair
  const eth2KeyPair = ethers.utils.HDNode.fromMnemonic(mnemonic);

  // Derive the deposit key and deposit message root
  const depositKey = eth2KeyPair.derivePath("m/12381/3600/0/0");
  const depositMessageRoot = keccak256(
    ethers.utils.solidityPack(
      ["uint256", "bytes32", "bytes32"],
      [0, depositKey.publicKey.slice(1), withdrawalCredentials]
    )
  );

  // Generate the deposit data
  const depositData = ethers.utils.defaultAbiCoder.encode(
    ["bytes", "bytes", "bytes", "bytes", "uint64"],
    [
      depositKey.publicKey.slice(1),
      withdrawalCredentials,
      keccak256(depositKey.publicKey),
      "0x",
      0,
    ]
  );

  console.log("Deposit data:", depositData);

  // Get the current deposit count
  const depositCount = await depositContract.get_deposit_count();

  // Submit the deposit transaction to the network
  const tx = await depositContract.deposit(
    "0x0000000000000000000000000000000000000000",
    depositData,
    { value: depositAmount }
  );
  console.log("Deposit transaction sent:", tx.hash);
  console.log("Deposit count:", depositCount.toNumber() + 1);
}

generateDepositData();
