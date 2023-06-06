import json
import sys
from web3 import Web3


class SSVNetwork:
    abi = []
    contract = None
    web3: Web3 = None

    def __init__(self, ssv_address, _web3: Web3, abi_path=None):
        self._import_abi(filepath=abi_path)
        self.web3 = _web3
        self.contract = self.web3.eth.contract(
            abi=self.abi, address=ssv_address)

    def _import_abi(self, filepath):
        if filepath is None:
            with open("SSVNetwork.json", "r") as file:
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


if __name__ == '__main__':
    web3 = Web3(Web3.HTTPProvider(sys.argv[1]))
    operator_id = sys.argv[2]
    owner_address = sys.argv[3]
    print(operator_id)
    print(owner_address)
    ssv = SSVNetwork(sys.argv[4], web3)
    print(ssv.get_latest_cluster(owner_address,operator_id))

    # TO run: python get_latest_cluster.py <eth_rpc> <operator_ids_comma_separated> <owner_address> <ssv_address>
