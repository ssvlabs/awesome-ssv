from web3 import Web3


class StakingPool:
    abi = [{
        "inputs": [],
        "name": "WITHDRAWAL_ADDRESS",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }, {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "pubkey",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "withdrawal_credentials",
                "type": "bytes"
            },
            {
                "internalType": "bytes",
                "name": "signature",
                "type": "bytes"
            },
            {
                "internalType": "bytes32",
                "name": "deposit_data_root",
                "type": "bytes32"
            }
        ],
        "name": "depositValidator",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }]

    contract = None

    def __init__(self, stakepool_contract, web3: Web3):
        """

        :param keysmanager_address:
        """
        self.contract = web3.eth.contract(address=stakepool_contract, abi=self.abi)

    def get_withdrawal_address(self):
        return self.contract.functions.WITHDRAWAL_ADDRESS().call()

    def deposit_validator(self, pubkey, withdrawal_creds, signature, deposit_data_root,account_address):
        return self.contract.functions.depositValidator(pubkey, withdrawal_creds, signature,
                                                        deposit_data_root).buildTransaction({"from":account_address})
