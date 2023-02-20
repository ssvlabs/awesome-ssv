# LSD staking pool powered by SSV

This repo showcases minimalistic backend for an LSD staking pool. It is for learning purposes ONLY and should NOT be a

base for any solution used in production. It contains backend scripts and smart contracts to manage and stake Ether,

minting a LSD token (ssvETH) and leveraging ssv.network to stake in a distributed and decentralized manner.

## Credits

Huge thanks to [@RohitAudit](https://github.com/RohitAudit) on whose [repo](https://github.com/RohitAudit/ssv-service)

is this minimalistic staking pool based on!

<!--

### Demo Contracts on Goerli



- Staking Pool

  Contract: [0x0B3382A006DD7F03ED1333c6C7472857fFFB6778](https://goerli.etherscan.io/address/0x0B3382A006DD7F03ED1333c6C7472857fFFB6778#code)



- Keys-manager

  Contract: [0x2b54244C61346DcD14CB77f8642CeA941Aa82664](https://goerli.etherscan.io/address/0x2b54244C61346DcD14CB77f8642CeA941Aa82664#code)



- RoETH

  Contract: [0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c](https://goerli.etherscan.io/address/0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c#code)



- Common

  Contract: [0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c](https://goerli.etherscan.io/address/0xCe24cc06357Ee4960f802D8D44004F2cb84D4d4c#code) -->

## How it works?

### User Actions

- User stakes their eth to a staking contract for which he is minted a liquid staked derivative token, ssvETH.

- Creates a ethereum validator key and gives it to staking pool for depositing for activation

- Generates keyshares from the validator keystore and stakes them the SSV nodes

- Saves the keystore and keyshares for verification at a later stage

## How to deploy?

### External Libraries used

- [SSV-KEYS](https://github.com/bloxapp/ssv-keys.git) : Used to split ethereum validator keys.

- [Ethereum-staking-cli](https://github.com/ethereum/staking-deposit-cli.git) : Used to generate ethereum validators keys

### Install Dependencies

- [python](https://www.python.org/downloads/), you can install it here.

- [eth-Brownie](https://eth-brownie.readthedocs.io/en/stable/), you can install it here.

- [ganache](https://www.npmjs.com/package/ganache) read more here
  - `npm install ganache --global`

### Initial setup

- make the script executable and run it

```

chmod +x setup.sh

./setup.sh


```

## Deploying contracts

```

cd demo-contract/

```

### Brownie Environment setup

1. You will need to setup your RPC

you can do so by writing into your console `export WEB3_INFURA_PROJECT_ID=<your id>` if you use infura

or `export WEB3_ALCHEMY_PROJECT_ID=<your id>` if you use alchemy. You can obtain one

from [infura here](https://app.infura.io/)

2. You need to set up your deployer private key

you can do so by writing into your console `brownie accounts new deployer` more on brownie account

management [here](https://eth-brownie.readthedocs.io/en/stable/account-management.html#local-accounts)

### Contract Changes

Now go to `demo-contract/scripts/deploy.py` and change the following:

- `whitelist, withdrawal_creds` update these values use deployer address, that will you use to run the backend script

Optional

- `operator_ids` (Optional, you can keep the default operators)

### Deployments

#### Goerli-fork

This repo works best with locally forked Goerli network as the network contains both the Beacon Deposit contract and SSV contracts.

Before running the fork, use [SSV faucet](https://faucet.ssv.network/) and send yourself some SSV. You will need it in the next step for your pool manager script to registerValidator.

- Start the goerli fork network:

- `ganache --chain.vmErrorsOnRPCResponse true --wallet.totalAccounts 10 --fork.url https://goerli.infura.io/v3/<ENDPOINT> --wallet.mnemonic brownie --server.port 8545`

ENDPOINT = goerli endpoint from alchemy or infura

- Now you can use this network to deploy your contracts and interact with SSV contracts

- `brownie console`

  - this will open automatically detect local blockchain running and connect to it.

- Make sure you updated `whitelist, withdrawal_creds` addresses in `deploy.py` file.

- In the brownie console run:

- `run('deploy')`

- you will need staking pool address for to run the backend script. you can find it in `contrat_addresses.json`, it is also printed in the console.

- To stake some eth run:
- `StakingPool[0].stake({'value':64*10**18, 'from': accounts[0], 'gas_price': 8750000000})`

- Now you can start the backend scripts

#### Goerli

This repo works well with Goerli network as the network contains both the Beacon Deposit contract and SSV contracts.

- Start the network:

- `brownie console --network goerli`

- Make sure you updated `whitelist, withdrawal_creds` addresses in `deploy.py` file.

- In the brownie console run:

- `run('deploy')`

- you will need staking pool address for to run the backend script. you can find it in `contrat_addresses.json`, it is also printed on the console.

Once you have deployed your contracts you can stake your sweet ETH! You will receive your liquid ssvETH representing your stake. If you need help with getting your hands on 32 goerliETH to test validator deployment, we should be able to help you on [our discord](https://discord.com/invite/AbYHBfjkDY).

When you have enough (32) goerliETH for to test depositing a validator change the value in the `stake.py` script or simply run this in your console:

- `StakingPool[0].stake({'value':64*10**18})`

Now you can start the staking pool manager backend scripts

#### Local deployment

If you want to deploy your system locally additionally you'll need to deploy Ethereum Deposit Contract for validator activation, SSV token and SSV contract to interact with.

## Backend manager
### Running the scripts

Your staking pool needs to be funded with some SSV to pay for running your validator. Keep at least 50 SSV at your deployer address.

It will use it to pay operators for running your distributed validator. You can get some Goerli SSV from [SSV faucet here](https://faucet.ssv.network/). If you are using a local goerli-fork, use the faucet on Goerli, send the SSV to your deployer address and launch it again.

- Open new terminal in the main project folder

To run script you first need to install the requirements :

```
pip install -r requirements.txt
```

To see what all command line option the script supports :
```
python main.py -h/--help
```
Following are the option and their respective config:


- *create-keys* : This option can be used to generate ethereum validator keys and their deposit data
  - Example config file: sample_config/validator-config.json
  - Fill in the params in config file and give it as an argument
```
python main.py create-keys -c <CONFIG_FILE>
```
- *generate-keyshares* : This option can be used to generate SSV keyshares using ssv cli tool
  - Example config file: sample_config/keyshare-config.json
  - Fill in the params in config file and give it as an argument
```
python main.py generate-keyshares -c <CONFIG_FILE>
```
- *deposit-validators* : This option can be used to submit validator to stakepool
  - Example config file: sample_config/deposit-validator.json
  - Fill in the params in config file and give it as an argument
```
python main.py deposit-validators -c <CONFIG_FILE>
```

- *deposit-keyshares* : This option can be used to submit validator keyshares to stakepool
  - Example config file: sample_config/deposit-keyshares.json
  - Fill in the params in config file and give it as an argument
```
python main.py deposit-keyshares -c <CONFIG_FILE>
```

- *stake* : This is the backend script that monitors the stakepool and regularly generates validator pubkeys and SSV keyshares
  - Example config file: sample_config/stake-config.json
  - Fill in the params in config file and give it as an argument
```
python main.py stake -c <CONFIG_FILE>
```


### LICENSE

MIT License
