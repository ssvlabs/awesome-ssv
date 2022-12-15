# LSD staking pool powered by SSV

This repo showcases minimalistic backend for an LSD staking pool. It is for learning purposes ONLY and should NOT be a base for any solution used in production. It contains backend scripts and smart contracts to manage and stake Ether, minting a LSD token (ssvETH) and leveraging ssv.network to stake in a distributed and decentralized manner.

## Credits

Huge thanks to [@RohitAudit](https://github.com/RohitAudit) on whose [repo](https://github.com/RohitAudit/ssv-service) is this minimalistic staking pool based on!

### Dependencies

- **eth-Brownie** to install it follow the instructions from [eth-Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/).

### External Libraries used

- [SSV-KEYS](https://github.com/bloxapp/ssv-keys.git) : Used to split ethereum validator keys.

- [Ethereum-staking-cli](https://github.com/ethereum/staking-deposit-cli.git) : Used to generate ethereum validators keys

### Demo Contracts on Goerli

<!--
- Staking Pool Contract: [0x0B3382A006DD7F03ED1333c6C7472857fFFB6778](https://goerli.etherscan.io/address/0x0B3382A006DD7F03ED1333c6C7472857fFFB6778#code)

- Keys-manager Contract: [0x2b54244C61346DcD14CB77f8642CeA941Aa82664](https://goerli.etherscan.io/address/0x2b54244C61346DcD14CB77f8642CeA941Aa82664#code)

- RoETH Contract: [0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c](https://goerli.etherscan.io/address/0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c#code)

- Common Contract: [0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c](https://goerli.etherscan.io/address/0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c#code) -->

## How it works?

### User Actions

- User stakes their eth to a staking contract for which he is minted a liquid staked derivative token, ssvETH.

- That's it!! User can just relax and wait for their ssvETH to autoautocompound over time and till then use the same tokens in other DeFi protocols

### Protocol

### Protocol

- The backend keeps a close eye on stakingpool contract.

- As soon as the balance reaches 32 eth, it triggers few actions:

- Creates a ethereum validator key and gives it to staking pool for depositing for activation

- Generates keyshares from the validator keystore and stakes them the SSV nodes

- Saves the keystore and keyshares for verification at a later stage

## How to deploy the system?

### Install prerequisites

- make the script executable

```

chmod +x setup.sh

```

- run the script, it'll install all dependencies. \
  BE PATIENT, this can take couple of minutes.

```

./setup.sh

```

- Go to demo contract folder

```
cd demo-contract/
```

Install **eth-Brownie** + Ganache local blockchain, follow the instructions from [eth-Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/).

**Brownie Environment setup**

1. You will need to setup your RPC
   you can do so by writing into your console `export WEB3_INFURA_PROJECT_ID=<your id>` if you use infura or `export WEB3_ALCHEMY_PROJECT_ID=<your id>` if you use alchemy. You can obtain one from [infura here](https://app.infura.io/)

2. You need to set up your deployer private key

```
brownie accounts new deployer0

```

Brownie v1.19.0 - Python development framework for Ethereum

```
Enter the private key you wish to add: <your private key>

Enter the password to encrypt this account with:

SUCCESS: A new account '0x0000536dbD99d918092249Ef4eDe4a69A35CccCa' has been generated with the id 'deployer0'

```

more on brownie account management [here](https://eth-brownie.readthedocs.io/en/stable/account-management.html#local-accounts)

---

### Changes

If you created a new deplyer "deployer0" **you can skip the next step**.

#### Updating deployer

Now go to demo-contract/scripts/utils/helpers.py and change the following:

line 16: `account_name = "deployer0"` to your account name you have setup in the previous step

Now go to demo-contract/scripts/b_deploy.py and change the following:

- `whitelist` to make tx to staking pool and keysmanager, recomended to use your deployer address for ease of use

- `withdrawal_creds` where you want for your validators (Optional, this is testnet deployment)

- `operator_ids` (Optional, you can keep the default operators)

---

### Deployment

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

### Running pool manager backend

go to the main project folder first

```
cd ..
```

To deploy the backend for your staking pool you need to install requirements:

```

pip install -r requirements.txt

```

#### Fund deployer

- SSV

Your staking pool needs to be funded with some SSV. Keep **at least 50 SSV** at your deployer address, or send it directly to the pool.

It will use it to pay operators for running your distributed validator. You can get some from [SSV faucet here](https://faucet.ssv.network/).

#### Run pool manager

**NOTE**: you need to stake via stakepool, if you want to test the script creating and distributing validator.

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

```

If your console is showing `trying again` it means there is not enough stake in your staking pool, go to previos step _Staking ETH & funding the pool_ fund the pool and run the script again.

### LICENSE

MIT License
