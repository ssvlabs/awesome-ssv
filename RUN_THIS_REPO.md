# LSD staking pool powered by SSV

This repo showcases minimalistic backend for an LSD staking pool. It is for learning purposes ONLY and should NOT be a base for any solution used in production. It contains backend scripts and smart contracts to manage and stake Ether, minting a LSD token (ssvETH) and leveraging ssv.network to stake in a distributed and decentralized manner.

## Credits

Huge thanks to [@RohitAudit](https://github.com/RohitAudit) on whose [repo](https://github.com/RohitAudit/ssv-service) is this minimalistic staking pool based on!

### External Libraries used

- [SSV-KEYS](https://github.com/bloxapp/ssv-keys.git) : Used to split ethereum validator keys.

- [Ethereum-staking-cli](https://github.com/ethereum/staking-deposit-cli.git) : Used to generate ethereum validators keys

### Demo Contracts on Goerli

- Staking Pool Contract: [0x0B3382A006DD7F03ED1333c6C7472857fFFB6778](https://goerli.etherscan.io/address/0x0B3382A006DD7F03ED1333c6C7472857fFFB6778#code)

- Keys-manager Contract: [0x2b54244C61346DcD14CB77f8642CeA941Aa82664](https://goerli.etherscan.io/address/0x2b54244C61346DcD14CB77f8642CeA941Aa82664#code)

- RoETH Contract: [0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c](https://goerli.etherscan.io/address/0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c#code)

- Common Contract: [0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c](https://goerli.etherscan.io/address/0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c#code)

### How it works?

#### User Actions

- User stakes their eth to a staking contract for which he is minted a liquid staked derivative token, ssvETH.

- That's it!! User can just relax and wait for their ssvETH to compound over time and till then use the same tokens in other DeFi protocols

#### Protocol

- The backend keeps a close eye on stakingpool contract.

- As soon as the balance reaches 32 eth, it triggers few actions:

- Creates a ethereum validator key and gives it to staking pool for depositing for activation

- Generates keyshares from the validator keystore and stakes them the SSV nodes

- Saves the keystore and keyshares for verification at a later stage

### How to deploy the system?

#### deploying smart contracts

- make the script executable

```

chmod +x setup.sh

```

- run the script, it'll install all dependencies.

```

./setup.sh

```

- In the scripts/deploy.js change the following:

- withdrawal credential you want for your validators

- operator-ids with your operators

- whitelist address to make tx to staking pool and keysmanager

- Go to demo contract folder and run the script for deployment

```

npx hardhat run scripts/deploy.js --network goerli

```

The contract addresses will be logged on console. You can use them while running the backend

```

NOTE: If you are deloying the system on Local you'll need to deploy Deposit Contract for validator activation for Ethereum and SSV contracts to interact

```

#### Using the scripts

- For options use

```

python main.py -h

```

- There are two options

- stake: use this to start the backend service for the staking pool

- create-keys: use this to create validator keys and key-shares for operators separately

- To deploy the backend for staking pool install requirements for python

```

pip install -r requirements.txt

```

- Following arguments are needed to run the script

- PRIVATE_KEY(-priv): private key for the whitelisted address in the contracts to do the transaction

- STAKING_POOL(-st): staking pool contract address

- SSV_CONTRACT(-ssv): ssv network contract address

- ETH_RPC(-eth): rpc endpoint for ethereum node

```

python main.py stake -eth <ETH_RPC> -priv <PRIVATE_KEY> -st <STAKING_POOL> -ssv <SSV_CONTRACT>

```

- To create keys

- OPERATOR_IDS: operator ids for keyshares

- KEY_COUNT: no. of validator keys to create

- WITHDRAWAL_CREDENTIALS: withdrawal credentials for validator keys

- KEYSTORE_PASSWORD: keystore password for validator keys

```

python main.py create-keys -id <OPERATOR_IDS> -n <KEY_COUNT> -wc <WITHDRAWAL_CREDENTIALS> -pass <KEYSTORE_PASSWORD>

```

### LICENSE

MIT License
