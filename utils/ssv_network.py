from web3 import Web3


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
    }]
    contract = None

    def __init__(self, ssv_address, web3: Web3):
        self.contract = web3.eth.contract(abi=self.abi, address=ssv_address)

    def get_network_fee(self):
        return self.contract.functions.getNetworkFee().call()
