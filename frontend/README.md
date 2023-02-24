# 🥩 Awesome SSV Staking Frontend 🥩

🚀 By staking their ETH to a staking contract, users receive a liquid staked derivative token called ssvETH. This allows them to earn compound interest on their staked ETH, while also being able to use the ssvETH tokens in other DeFi protocols without having to unstake their original ETH.

🙏 For aditional functionality and documentation check the amazing [scaffold-eth](https://github.com/scaffold-eth/scaffold-eth) repo this frontend is based on!

# Live Deployment

You can find our live demo deployment [Here](https://awesome-ssv-staking.surge.sh)

# Frontend

## Prerequisites

[Node (v18 LTS)](https://nodejs.org/en/download/)
[Yarn (v1.x)](https://classic.yarnpkg.com/en/docs/install/)
[Git](https://git-scm.com/downloads)

## Installation

> 1️⃣ clone/fork awesome SSV Staking repo:

```bash
git clone https://github.com/bloxapp/awesome-ssv
```
> 2️⃣ make sure you have the right network set

> 3️⃣ install and start the frontend:

```bash
cd frontend
yarn install
yarn react-app:start
```

📱 Open http://localhost:3000 to see the app

In `frontend/packages/react-app/src/App.jsx` change to `NETWORKS.localhost` if running with `yarn fork` or `NETWORKS.goerli` if live Goerli network.

```js
const initialNetwork = NETWORKS.localhost;

```

🎉 If you already have the contracts deployed from the [backend](https://github.com/bloxapp/awesome-ssv), you just need to update the default network in `packages/react-app/src/App.jsx` and your new contract addresses and ABIs in `packages/react-app/src/contracts/external_contracts`.

=======
# Editing

📝 Edit your frontend `App.jsx` in `packages/react-app/src`

✏ Edit the home view and the manager view in  `packages/react-app/src/views/Home.jsx` and `packages/react-app/src/views/Manager.jsx`respectively.  

❗❗ Important : Make sure that your front end is connected to the correct chain, either:

1. `const initialNetwork = NETWORKS.goerli;`

or

2. `const initialNetwork = NETWORKS.localhost;`

# Deploy Contracts

🔏 Edit the smart contracts in `packages/hardhat/contracts`

💼 Add/Edit your deployment scripts in `packages/hardhat/deploy`

## 🚨 Local deployment (Goerli fork):

If you want to deploy the contracts locally using the Goerli fork you can do so with hardhat.

You will need to setup your RPC endpoint.

Update `frontend/packages/hardhat/package.json` file and edit this line `"fork": "hardhat node --network hardhat --fork https://goerli.infura.io/v3/<YOUR_KEY>"` and input `<YOUR_KEY>`

You can obtain one from [infura here](https://app.infura.io/).

Now run:

```bash
yarn fork
```

After setting up your `defaultNetwork` to `"localhost"` in `hardhat-config.js` you can run

```bash
yarn deploy
```
🎇 after this your new staking pool and ssvETH contracts should reflect on automatically in `packages/react-app/src/contracts/localhost/`

# 🚨 Goerli live deployment:

If you want to deploy on the live Goerli testnet, you'll only need to run this :

```bash
yarn deploy-goerli
```
🎇 after this your new staking pool and ssvETH contracts should reflect on automatically in `packages/react-app/src/contracts/goerli/`


✅ you can verify your staking pool contract on Goerli by using this :


```bash
yarn verify --constructor-args arguments.js --network goerli <NEW_DEPLOYED_CONTRACT_ADDRESS>
```


✅ you can verify your ssvETH contract on Goerli by using this :


```bash
yarn verify --network goerli NEW_DEPLOYED_CONTRACT_ADDRESS
```

❗❗ Important :
💥 Once you have your contracts deployed you will need to update the default network in `App.jsx` to match your default network in `hardhat-config.js`. And your new contracts addresses and ABIs in `packages/react-app/src/contracts/external_contracts`.

# Show off to the world

🚨📡 To deploy to a public domain, use `yarn surge`. You will need to have a surge account and have the surge CLI installed. There is also the option to deploy to IPFS using `yarn ipfs` and `yarn s3` to deploy to an AWS bucket 🪣 There are scripts in the `packages/react-app/src/scripts` folder to help with this.`

---



# Backend

Now it's time to activate some validators beacon chain and use ssv network to run it! 

All the backend functionality for this, namely 

1. validator creation
2. validator activation with beacon chain
3. splitting your validator (DVT!) into multiple shares
4. registering validator share with ssv.network 

are done for you out of the box!!!


🚀 Just follow the readme and run scripts [here](https://github.com/bloxapp/awesome-ssv/blob/main/RUN_BACKEND.md)


💼 Add/Edit your deployment scripts in `packages/hardhat/scripts/deploy` for Goerli and in `packages/hardhat/deploy` for localhost (Goerli fork)



# Interested? Get involved 

- build sth interesting on top, transferable NFT validators, Restaking app, or whatever else and **open PR**.

## Connect

Best way is via discord channel [#devs-support](https://discord.com/channels/723834989506068561/766640777815523330), ask there, tag the team directly and also @MarkoInEther and @Matty. They will help you to get to the right person.




