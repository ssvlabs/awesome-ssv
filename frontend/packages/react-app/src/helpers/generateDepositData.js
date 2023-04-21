const ethers = require('ethers');

async function generateDepositData() {
  try {
    // Generate a new mnemonic
    const mnemonic = ethers.Wallet.createRandom().mnemonic.phrase;
    const password = ""; // This can be an empty string if your mnemonic doesn't have a password

    // Derive the ETH2 deposit keypair from the mnemonic
    const hdNode = ethers.utils.HDNode.fromMnemonic(mnemonic, password);
    const depositDerivationPath = "m/12381/3600/0/0"; // This is the ETH2 deposit derivation path
    const depositKeypair = hdNode.derivePath(depositDerivationPath);
    console.log("depositKeypair : ", depositKeypair);
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
          depositData.withdrawalCredentials,
          depositData.amount,
          0, // This is always 0 for eth2 deposits
        ]
      )
    );
    const depositPrivateKey = hdNode.derivePath(depositDerivationPath).privateKey;
    const signingKey = new ethers.utils.SigningKey(depositPrivateKey);
    const depositSignature = signingKey.signDigest(ethers.utils.arrayify(depositMessageHash));
    const rsv = ethers.utils.splitSignature(depositSignature);
    const signature = ethers.utils.hexlify(ethers.utils.concat([rsv.r, rsv.s, rsv.v]));
    depositData.signature = signature.slice(2);

    // Calculate the deposit data root
    const depositDataRoot = ethers.utils.sha256(
      ethers.utils.solidityPack(
        ['bytes', 'bytes', 'bytes', 'uint'],
        [
          '0x' + depositData.pubkey,
          depositData.withdrawalCredentials,
          '0x' + depositData.signature,
          depositData.amount,
        ]
      )
    );

    return { depositData, depositDataRoot };
  } catch (error) {
    console.error(error);
  }
}

module.exports = generateDepositData;