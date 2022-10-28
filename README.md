# ssv-service (GARUDA)
You can use this to repo to act as backend of your ssv staking solution

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
- User stakes their eth to a staking contract through which he is given a liquid staked derivative token called roETH.
- That's it!! User can just relax and wait for their roETH to compound over time and till then use the same tokens in other DeFi protocols

#### Protocol
- The backend of garuda keeps a close eye on stakingpool contract. 
- As soon as the balance reaches 32 eth, it triggers few actions:
  - Creates a ethereum validator key and gives it to stakingpool for depositing for activation
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

#### Deploying the backend

To deploy the backend install requirements for python
```
pip install -r requirements.txt
```
Following arguments are needed to run the script
- PRIVATE_KEY(-priv): private key for the whitelisted address in the contracts to do the transaction
- STAKING_POOL(-st): staking pool contract address 
- KEYSMANAGER(-key): keys manager contract address
- SSV_CONTRACT(-ssv): ssv network contract address
- ETH_RPC(-eth): rpc endpoint for ethereum node
```
python main.py -eth <ETH_RPC> -priv <PRIVATE_KEY> -st <STAKING_POOL> -key <KEYSMANAGER> -ssv <SSV_CONTRACT>

```

