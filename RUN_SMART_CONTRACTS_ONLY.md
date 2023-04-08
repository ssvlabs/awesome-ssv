# LSD staking pool powered by SSV

This repo showcases a minimalistic backend for an LSD staking pool. It is for learning purposes ONLY and should NOT be a

base for any solution used in production. It contains backend scripts and smart contracts to manage and stake Ether,

minting an LSD token (ssvETH) and leveraging ssv.network to stake in a distributed and decentralized manner.

## Video walkthrough

[![Repo walkthrough & launchig 🌈LSD pool](http://img.youtube.com/vi/4xgCsi_kSVI/0.jpg)](http://www.youtube.com/watch?v=4xgCsi_kSVI "Repo walkthrough & launchig 🌈LSD pool"){:target="\_blank"}

**NOTE:**

- **Readmes always take precedence** - Some parts of this video may be outdated.
- Video goes into **more detail and gives more background**. If you have some experience with this stuff you can safely skip it and follow READMEs only.

## Credits

Huge thanks to [@RohitAudit](https://github.com/RohitAudit) whose [repo](https://github.com/RohitAudit/ssv-service)

this minimalistic staking pool is based on!

## How it works

- Staking has never been so easy, thanks to SSV, you can stake your ETH and earn ssvETH without running your own validator! 🤑

### User Actions

- Users stake their ETH to a staking contract for which he is minted a liquid staked derivative token, ssvETH.

- Creates an Ethereum validator key and gives it to the staking pool to deposit for activation

- Generates keyshares from the validator keystore and stakes them with the SSV nodes

- Saves the keystore and keyshares for verification at a later stage

## How to deploy?

This readme tutorial is for smart-contract-only deployment using brownie framework. If you want to deploy with frontend as well or prefer using `JS` continue to README in frontend folder [FE_README.md](/frontend/README.md)

If you are happy just with backend, continue.

### Install Dependencies

- [python](https://www.python.org/downloads/), you can install it here.

- [eth-Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), you can install it here.

- [hardhat](https://hardhat.org/hardhat-runner/docs/getting-started#installation) read more here
  - `npm install -g hardhat`

### Brownie Environment setup

1. You will need to set up your RPC

you can do so by writing into your console `export WEB3_INFURA_PROJECT_ID=<your id>` if you use Infura

or `export WEB3_ALCHEMY_PROJECT_ID=<your id>` if you use Alchemy. You can obtain one

from [Infura here](https://app.infura.io/)

2. You need to set up your deployer private key

you can do so by writing into your console `brownie accounts new deployer` more on brownie account

management [here](https://eth-brownie.readthedocs.io/en/stable/account-management.html#local-accounts)

3. Installing packages

you may need to install some packages, this is the one you need, if you need more, just copy the package path from the browser or smart contract directly.

example:

```
brownie pm install OpenZeppelin/openzeppelin-contracts-upgradeable@4.8.0
```

### Contract Changes

Now go to `demo-contract/scripts/deploy.py` and change the following:

- `whitelist, withdrawal_creds` update these values using the deployer address that you will use to run the backend script

Optional

- `operator_ids` (Optional, you can keep the default operators)

### Deployments

#### Goerli-fork

This repo works best with a locally forked Goerli network as the network contains both the Beacon Deposit contract and SSV contracts.

Before running the fork, use the [SSV faucet](https://faucet.ssv.network/) and send yourself some SSV. You will need it in the next step for your pool manager script to registerValidator.

- Start the goerli fork network:

- `npx hardhat node --network hardhat --fork https://goerli.infura.io/v3/<your id>`

ENDPOINT = goerli endpoint from Alchemy or Infura

- Now you can use this network to deploy your contracts and interact with SSV contracts

- `cd demo-contract/`

- `brownie console`

  - this will open automatically, detect the local blockchain running, and connect to it.

- Make sure you updated `whitelist, withdrawal_creds` addresses in `deploy.py` file.

- In the brownie console run:

- `run('deploy')`

- you will need a staking pool address to run the backend script. You can find it in `contrat_addresses.json`, it is also printed in the console.

- To stake some eth run:
- `StakingPool[0].stake({'value':64*10**18, 'from': accounts[0], 'gas_price': 8750000000})`

- Now you can start the backend scripts here [RUN_BACKEND.md](RUN_BACKEND.md)

#### Goerli

This repo works well with Goerli network as the network contains both the Beacon Deposit contract and SSV contracts.

- Start the network:

- `cd demo-contract/`

- `brownie console --network goerli`

- Make sure you updated `whitelist, withdrawal_creds` addresses in `deploy.py` file.

- In the brownie console run:

- `run('deploy')`

- you will need a staking pool address to run the backend script. You can find it in `contrat_addresses.json`, it is also printed on the console.

Once you have deployed your contracts you can stake your sweet ETH! You will receive your liquid ssvETH representing your stake. If you need help getting your hands on 32 goerliETH to test validator deployment, we should be able to help you on [our discord](https://discord.com/invite/AbYHBfjkDY).

When you have enough (32) goerliETH to test depositing a validator change the value in the `stake.py` script or simply run this in your console:

- `StakingPool[0].stake({'value':64*10**18})`

Now you can start the staking pool manager backend scripts

#### Local deployment

If you want to deploy your system locally additionally you'll need to deploy the Ethereum Deposit Contract for validator activation, SSV token, and SSV contract to interact with.

## Backend manager

Once your smart contracts are deployed you are ready to [RUN_BACKEND.md](RUN_BACKEND.md)
