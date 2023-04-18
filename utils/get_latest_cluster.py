import json
from collections import namedtuple

from web3 import Web3
from utils.eth_connector import EthNode


class SSVNetwork:
    abi = []
    contract = None
    web3: Web3 = None
    goerli: Web3 = None

    def __init__(self, ssv_address, _web3: Web3, _goerli: Web3, abi_path=None):
        self._import_abi(filepath=abi_path)
        self.web3 = _web3
        self.goerli = _goerli
        self.contract = self.web3.eth.contract(
            abi=self.abi, address=ssv_address)

    def _import_abi(self, filepath):
        if filepath is None:
            with open("utils/SSVNetwork.json", "r") as file:
                self.abi = json.load(file)["abi"]
            file.close()
        else:
            with open(filepath, "r") as file:
                self.abi = json.load(file)["abi"]
            file.close()

    def get_latest_cluster(self, owner_address, operator_ids):
        step = 50000
        from_block = self.web3.eth.get_block_number() - step
        to_block = self.web3.eth.get_block_number()
        while to_block > 8661727:
            filter = self.contract.events.ValidatorAdded.build_filter()
            filter.fromBlock = from_block
            filter.toBlock = to_block
            filter.args.owner.match_single(owner_address)
            filter.args.operatorIds.match_single(operator_ids)
            filter_deploy = filter.deploy(self.web3)
            result = filter_deploy.get_all_entries()
            if len(result) > 0:
                return [i for i in dict(result[len(result) - 1].args.cluster).values()]
            to_block = from_block
            from_block -= step
        return [0, 0, 0, 0, True]


# class SSVNetworkview:
#     abi = []
#     web3: Web3 = None

#     def __init__(self, ssv_address, web3: Web3, abi_path=None):

#         self._import_abi(filepath=abi_path)
#         self.contract = web3.eth.contract(abi=self.abi, address=ssv_address)

#     def _import_abi(self, filepath):
#         if filepath is None:
#             with open("utils/SSVNetworkViews.json", "r") as file:
#                 self.abi = json.load(file)["abi"]
#             file.close()
#         else:
#             with open(filepath, "r") as file:
#                 self.abi = json.load(file)["abi"]
#             file.close()

#     def get_operator_fee(self, id):
#         return self.contract.functions.getOperatorFee(id).call()

#     def get_network_fee(self):
#         return self.contract.functions.getNetworkFee().call()


# class SSVToken:
#     abi = [{
#         "inputs": [
#             {
#                 "internalType": "address",
#                 "name": "account",
#                 "type": "address"
#             }
#         ],
#         "name": "balanceOf",
#         "outputs": [
#             {
#                 "internalType": "uint256",
#                 "name": "",
#                 "type": "uint256"
#             }
#         ],
#         "stateMutability": "view",
#         "type": "function"
#     }, {
#         "inputs": [
#             {
#                 "internalType": "address",
#                 "name": "to",
#                 "type": "address"
#             },
#             {
#                 "internalType": "uint256",
#                 "name": "amount",
#                 "type": "uint256"
#             }
#         ],
#         "name": "transfer",
#         "outputs": [
#             {
#                 "internalType": "bool",
#                 "name": "",
#                 "type": "bool"
#             }
#         ],
#         "stateMutability": "nonpayable",
#         "type": "function"
#     }
#     ]

#     def __init__(self, ssv_address, web3: Web3):
#         self.contract = web3.eth.contract(abi=self.abi, address=ssv_address)

#     def get_balance(self, account_address):
#         return self.contract.functions.balanceOf(account_address).call()

#     def transfer_token(self, address, amount, account_address):
#         return self.contract.functions.transfer(address, amount).build_transaction(
#             {"from": account_address})


# if __name__ == '__main__':
#     web3 = EthNode("https://eth-goerli.g.alchemy.com/v2/9y1ltLyP99wkj4RY0Nsp67Eat3WAlDoz",
#                    "0d19dfbb7dd09b8f19d76d9e57036cd109b55cf12c97080918c533b7bb6b12a7")
#     ssv = SSVNetwork("0xb9e155e65B5c4D66df28Da8E9a0957f06F11Bc04", web3.eth_node)
#     print(ssv.get_operator(1))
