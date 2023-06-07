import json

from web3 import Web3


class StakingPool:
    abi = []

    contract = None

    def __init__(self, stakepool_contract, web3: Web3, abi_path=None):
        """

        :param keysmanager_address:
        """
        self._import_abi(filepath=abi_path)
        self.contract = web3.eth.contract(abi=self.abi, address=stakepool_contract)

    def _import_abi(self, filepath):
        if filepath is None:
            with open("utils/StakingPool.json", "r") as file:
                self.abi = json.load(file)["abi"]
            file.close()
        else:
            with open(filepath, "r") as file:
                self.abi = json.load(file)["abi"]
            file.close()

    def get_withdrawal_address(self):
        return self.contract.functions.WITHDRAWAL_ADDRESS().call()

    def deposit_validator(self, pubkey, withdrawal_creds, signature, deposit_data_root, account_address):
        return self.contract.functions.depositValidator(pubkey, withdrawal_creds, signature,
                                                        deposit_data_root).buildTransaction(
            {"from": account_address})

    def get_operator_ids(self):
        """

        :return:
        """
        return self.contract.functions.getOperators().call()

    def send_key_shares(self, pubkey, operator_ids, shares, amount, cluster, account_address):
        """

        :return:
        """
        return self.contract.functions.depositShares(pubkey, operator_ids, shares,
                                                     amount, cluster).buildTransaction(
            {"from": account_address, 'gas':1500000})
