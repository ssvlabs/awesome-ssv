from web3 import Web3
from utils.eth_connector import EthNode


class SSVNetwork:
    abi = [{
        "inputs": [],
        "name": "getNetworkFee",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }, {
        "inputs": [
            {
                "internalType": "uint32",
                "name": "operatorId",
                "type": "uint32"
            }
        ],
        "name": "getOperatorById",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            },
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }]
    contract = None

    def __init__(self, ssv_address, web3: Web3):
        self.contract = web3.eth.contract(abi=self.abi, address=ssv_address)

    def get_network_fee(self):
        return self.contract.functions.getNetworkFee().call()

    def get_operator(self, id):
        operator = self.contract.functions.getOperatorById(id).call()
        operator_pubkey = str(operator[2]).split("x02d")[1].split("\\x00\\x00")[0]
        operator_name = str(operator[0])
        operator_fee = str(operator[4])

        return operator_pubkey, operator_fee, operator_name, id


class SSVToken:
    abi = [{
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }, {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
    ]

    def __init__(self, ssv_address, web3: Web3):
        self.contract = web3.eth.contract(abi=self.abi, address=ssv_address)

    def get_balance(self, account_address):
        return self.contract.functions.balanceOf(account_address).call()

    def transfer_token(self, address, amount, account_address):
        return self.contract.functions.transfer(address, amount).buildTransaction(
            {"from": account_address, "maxFeePerGas": 10 ** 12})


if __name__ == '__main__':
    web3 = EthNode("https://eth-goerli.g.alchemy.com/v2/9y1ltLyP99wkj4RY0Nsp67Eat3WAlDoz","0d19dfbb7dd09b8f19d76d9e57036cd109b55cf12c97080918c533b7bb6b12a7")
    ssv = SSVNetwork("0xb9e155e65B5c4D66df28Da8E9a0957f06F11Bc04",web3.eth_node)
    print(ssv.get_operator(1))
