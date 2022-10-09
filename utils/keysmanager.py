from web3 import Web3


class KeysManager:
    abi = [{
        "inputs": [],
        "name": "getOperators",
        "outputs": [
            {
                "internalType": "uint32[4]",
                "name": "",
                "type": "uint32[4]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }, {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "publicKey",
                "type": "bytes"
            },
            {
                "internalType": "uint32[]",
                "name": "operatorIds",
                "type": "uint32[]"
            },
            {
                "internalType": "bytes[]",
                "name": "sharesPublicKeys",
                "type": "bytes[]"
            },
            {
                "internalType": "bytes[]",
                "name": "sharesEncrypted",
                "type": "bytes[]"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "submitValidatorShares",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }]
    contract = None

    def __init__(self, keysmanager_address, web3: Web3):
        """

        :param keysmanager_address:
        """
        self.contract = web3.eth.contract(address=keysmanager_address, abi=self.abi)

    def get_operator_ids(self):
        """

        :return:
        """
        return self.contract.functions.getOperators().call()

    def send_key_shares(self, pubkey, operator_ids, sharesPublicKeys, sharesEncrypted, amount, account_address):
        """

        :return:
        """
        return self.contract.functions.submitValidatorShares(pubkey, operator_ids, sharesPublicKeys, sharesEncrypted,
                                                             amount).buildTransaction({"from": account_address})
