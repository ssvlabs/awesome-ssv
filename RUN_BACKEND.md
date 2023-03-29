# Backend

This backend allows for easily managing the staking pool.

- Create Validator keys (for Deposit)
- generate-keyshares (for SSV contract)
- deposit-keyshares
- deposit-validators

### External Libraries used

- [SSV-KEYS](https://github.com/bloxapp/ssv-keys.git) : Used to split Ethereum validator keys.

- [Ethereum-staking-cli](https://github.com/ethereum/staking-deposit-cli.git) : Used to generate Ethereum validators keys

### Install Dependencies

- [python](https://www.python.org/downloads/), you can install it here.

## Before Running Backend Manager

### Deploy Contracts

- Smart Contracts only - Brownie framework

  - Follow [RUN_THIS_REPO.md](RUN_THIS_REPO.md)

- Front End & Smart contracts - Scaffold-eth framework
  - Follow [FE_README.md](/frontend/README.md)

## Run Backend Manager

**NOTE:**

- Make sure that for the backend script, you are using a private key corresponding to your `whitelist` address from your `deploy` script.

- Your staking pool needs to be funded with some SSV to pay for running your validator. Keep at least 50 SSV at your deployer address.

It will use it to pay operators for running your distributed validator. You can get some Goerli SSV from [SSV faucet here](https://faucet.ssv.network/). If you are using a local goerli-fork, use the faucet on Goerli, send the SSV to your deployer address and launch it again.

### Outputs

Your created validator keys and deposit data can be found in `"/validator_keys"` folder.

Validator split shares can be found in `"/keyshares"` folder.

```
validator_keys

- Open a new terminal in the main project folder

To run the scripts you first need to install the requirements :

```

pip install -r requirements.txt

```

To see what command line options the script supports :

```

python3 main.py -h/--help

```

Following are the option and their respective config:

- _create-keys_ : This option can be used to generate Ethereum validator keys and their deposit data
  - Example config file: sample_config/validator-config.json
  - Fill in the params in the config file and pass it as an argument

```

python3 main.py create-keys -c <CONFIG_FILE>

e.g.

python3 main.py create-keys -c sample_config/validator-config.json

```

- _generate-keyshares_ : This option can be used to generate SSV keyshares using the SSV CLI tool
  - Example config file: sample_config/keyshare-config.json
  - Fill in the params in the config file and pass it as an argument

```

python3 main.py generate-keyshares -c <CONFIG_FILE>

e.g.

python3 main.py generate-keyshares -c sample_config/keyshare-config.json

```

- _deposit-validators_ : This option can be used to submit validator keys to the staking pool
  - Example config file: sample_config/deposit-validator.json
  - Fill in the params in the config file and pass it as an argument

```

python3 main.py deposit-validators -c <CONFIG_FILE>

e.g.

python3 main.py deposit-validators -c sample_config/deposit-validator.json

```

- _deposit-keyshares_ : This option can be used to submit validator keyshares to the staking pool
  - Example config file: sample_config/deposit-keyshares.json
  - Fill in the params in the config file and pass it as an argument

```

python3 main.py deposit-keyshares -c <CONFIG_FILE>

```

- _stake_ : This is the backend script that monitors the staking pool and regularly generates validator pubkeys and SSV keyshares
  - Example config file: sample_config/stake-config.json
  - Fill in the params in the config file and pass it as an argument

```

python3 main.py stake -c <CONFIG_FILE>

e.g.

python3 main.py stake -c sample_config/stake-config.json

```
**NOTE:** Use `http://localhost:8545` if you are connecting to goerli-fork and `https://goerli.infura.io/v3/<your id>` when connecting to goerli

### LICENSE

MIT License
```
