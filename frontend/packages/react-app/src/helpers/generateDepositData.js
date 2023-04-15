const ethers = require('ethers');

async function generateDepositData() {
  try {
  // Generate a new mnemonic
  const mnemonic = ethers.Wallet.createRandom().mnemonic.phrase;
  const password = ""; // This can be an empty string if your mnemonic doesn't have a password

  

  // Derive the ETH2 deposit keypair from the mnemonic
  const hdNode = ethers.utils.HDNode.fromMnemonic(mnemonic, password);
  const depositKeypair = await hdNode.derivePath("m/12381/3600/0/0").keyPair; // The BIP32 path for ETH2 deposit keys

  // Construct the deposit data object
  const depositData = {
    pubkey: depositKeypair.publicKey.slice(2), // Remove the '0x' prefix
    withdrawalCredentials: '0x0000000000000000000000000000000000000000000000000000000000000000', // This can be set to the same value as the pubkey if you don't plan to withdraw funds
    amount: ethers.utils.parseEther('32').toHexString(), // The deposit amount in ETH (32 ETH is the minimum required to become a validator)
    signature: '0x', // Leave blank for now
  };

  // Calculate the deposit message hash
  const depositMessageHash = ethers.utils.keccak256(
    ethers.utils.defaultAbiCoder.encode(
      ['bytes', 'bytes', 'bytes', 'uint'],
      [
        '0x' + depositData.pubkey,
        '0x' + depositData.withdrawalCredentials,
        depositData.amount,
        0, // This is always 0 for eth2 deposits
      ]
    )
  );

  // Sign the deposit message hash with the deposit keypair
  const depositSignature = depositKeypair.sign(ethers.utils.arrayify(depositMessageHash));
  depositData.signature = depositSignature.slice(2); // Remove the '0x' prefix
  return { mnemonic, depositData };
} catch (error) {
  console.error(error);
}
  
}

module.exports = generateDepositData;
