# LSD staking pool powered by SSV

This repo showcases minimalistic backend for an LSD staking pool. It is for learning purposes ONLY and should NOT be a base for any solution used in production. It contains backend scripts and smart contracts to manage and stake Ether, minting a LSD token (ssvETH) and leveraging ssv.network to stake in a distributed and decentralized manner.

## Credits

Huge thanks to [@RohitAudit](https://github.com/RohitAudit) on whose [repo](https://github.com/RohitAudit/ssv-service) is this minimalistic staking pool based on!

### Dependencies

- [eth-Brownie](https://eth-brownie.readthedocs.io/en/stable/), you can install it here

### External Libraries used

- [SSV-KEYS](https://github.com/bloxapp/ssv-keys.git) : Used to split ethereum validator keys.

- [Ethereum-staking-cli](https://github.com/ethereum/staking-deposit-cli.git) : Used to generate ethereum validators keys

### Demo Contracts on Goerli

- Staking Pool Contract: [0x0B3382A006DD7F03ED1333c6C7472857fFFB6778](https://goerli.etherscan.io/address/0x0B3382A006DD7F03ED1333c6C7472857fFFB6778#code)

- Keys-manager Contract: [0x2b54244C61346DcD14CB77f8642CeA941Aa82664](https://goerli.etherscan.io/address/0x2b54244C61346DcD14CB77f8642CeA941Aa82664#code)

- RoETH Contract: [0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c](https://goerli.etherscan.io/address/0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c#code)

- Common Contract: [0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c](https://goerli.etherscan.io/address/0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c#code)

## How it works?

### User Actions

- User stakes their eth to a staking contract for which he is minted a liquid staked derivative token, ssvETH.

- That's it!! User can just relax and wait for their ssvETH to autocompound over time and till then use the same tokens in other DeFi protocols

### Protocol

- The backend keeps a close eye on stakingpool contract.

- As soon as the balance reaches 32 eth, it triggers few actions:

- Creates a ethereum validator key and gives it to staking pool for depositing for activation

- Generates keyshares from the validator keystore and stakes them the SSV nodes

- Saves the keystore and keyshares for verification at a later stage

## How to deploy the system?

### deploying smart contracts

- make the script executable

```

chmod +x setup.sh

```

- run the script, it'll install all dependencies.

```

./setup.sh

```

- Go to demo contract folder and make copy of the `env.example` file

```
cd demo-contract/
```

**Brownie Environment setup**

1. You will need to setup your RPC
   you can do so by writing into your console `export WEB3_INFURA_PROJECT_ID=<your id>` if you use infura or `export WEB3_ALCHEMY_PROJECT_ID=<your id>` if you use alchemy. You can obtain one from [infura here](https://app.infura.io/)

2. You need to set up your deployer private key
   you can do so by writing into your console `brownie accounts new <your private key>` more on brownie account management [here](https://eth-brownie.readthedocs.io/en/stable/account-management.html#local-accounts)

### Changes

Now go to demo-contract/scripts/utils/helpers.py and change the following:

line 16: `account_name = "deployer0"` to your account name you have setup in the previous step

Now go to demo-contract/scripts/b_deploy.py and change the following:

- `whitelist` to make tx to staking pool and keysmanager, recomended to use your deployer address for ease of use

- `withdrawal_creds` where you want for your validators (Optional, this is testnet deployment)

- `operator_ids` (Optional, you can keep the default operators)

now run:

```
brownie run ./scripts/b_deploy.py --network goerli
```

The contract addresses will be logged on console. You need them to save them for running the backend

**NOTE:** If you want to deploy your system locally you'll need to deploy Ethereum Deposit Contract for validator activation, SSV token and SSV contract to interact with. You can still deploy and test the contracts locally.

### Staking ETH & funding the pool

Now you can stake your sweet ETH! You will receive your liquid ssvETH representing your stake. If you need help with getting your hands on 32 goerliETH to test validator deployment, we should be able to help you on [our discord](https://discord.com/invite/AbYHBfjkDY).

When you have enough (32) goerliETH for to test depositing a validator change the value in the `b_stake.py` script and run it:

```
brownie run ./scripts/b_stake.py --network goerli
```

Your staking pool needs to be funded with some SSV. Keep at least 50 SSV at your deployer address, or send it directly to the pool.

It will use it to pay operators for running your distributed validator. You can get some from [SSV faucet here](https://faucet.ssv.network/).

---

#### Using the backend scripts

##### Requirements

You need python to run following scripts.

go to the main project folder first

```
cd ..
```

To deploy the backend for your staking pool you need to install requirements:

```

pip install -r requirements.txt

```

Following arguments are needed to run the script

- PRIVATE_KEY(-priv): private key for the whitelisted address in the contracts to do the transaction

- STAKING_POOL(-st): staking pool contract address

- SSV_CONTRACT(-ssv): ssv network contract address

- ETH_RPC(-eth): rpc endpoint for ethereum node

```

python3 main.py stake -eth <ETH_RPC> -priv <PRIVATE_KEY> -st <STAKING_POOL> -ssv <SSV_CONTRACT>

```

- For options use

```

python main.py -h

```

- There are two options

  - stake: use this to start the backend service for the staking pool

  - create-keys: use this to create validator keys and key-shares for operators separately

- To create keys

- OPERATOR_IDS: operator ids for keyshares

- KEY_COUNT: no. of validator keys to create

- WITHDRAWAL_CREDENTIALS: withdrawal credentials for validator keys

- KEYSTORE_PASSWORD: keystore password for validator keys

```

python3 main.py create-keys -id <OPERATOR_IDS> -n <KEY_COUNT> -wc <WITHDRAWAL_CREDENTIALS> -pass <KEYSTORE_PASSWORD>

```

EXAMPLE

```

python3 main.py create-keys -id 1 2 9 42 -n 1 -wc 0xfabb0ac9d68b0b445fb7357272ff202c5651694a -pass ""

### LICENSE

MIT License
```
