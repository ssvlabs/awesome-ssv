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

### 1. Front End plus Smart contracts - Scaffold-eth framework

If you want to deploy smart contract together with frontend using scaffold-eth framework built in `JS`continue to [RUN_SMART_CONTRACTS_AND_FRONTEND.md](/RUN_SMART_CONTRACTS_AND_FRONTEND.md).

It will navigate you through the remaining process.

## OR

### 2. Smart Contracts Only - Brownie framework

If you want to deploy smart contracts only using brownie framework built in `PY` continue to [RUN_SMART_CONTRACTS_ONLY.md](/RUN_SMART_CONTRACTS_ONLY.md).

It will navigate you through the remaining process.
