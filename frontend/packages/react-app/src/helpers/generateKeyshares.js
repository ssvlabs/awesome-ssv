const { SSVKeys } = require('ssv-keys');
const keystore = require('../constants/test.keystore.json');
const operators = require('../constants/operators.json');
const operatorIds = require('../constants/operatorIds.json');
const keystorePassword = 'testtest';

async function generateKeyshares() {
  // Step 1: read keystore file
  const ssvKeys = new SSVKeys(SSVKeys.VERSION.V3);
  const privateKey = await ssvKeys.getPrivateKeyFromKeystoreData(keystore, keystorePassword);

  // Step 2: Build shares from operator IDs and public keys
  const threshold = await ssvKeys.createThreshold(privateKey, operatorIds);
  const encryptedShares = await ssvKeys.encryptShares(operators, threshold.shares);

  // Step 3: Build final web3 transaction payload and update keyshares file with payload data
  const payload = await ssvKeys.buildPayload({
    publicKey: ssvKeys.publicKey,
    operatorIds,
    encryptedShares,
  });

  // Get the amount of 32 ETH from the payload
  const ethAmount = parseInt(payload.value, 16) / 1e18;

  // Get the shares key from the payload
  const sharesKey = payload.key;

  console.debug(`Amount of 32 ETH: ${ethAmount}`);
  console.debug(`Shares key: ${sharesKey}`);
}

module.exports = generateKeyshares;