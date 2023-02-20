import json
import os
from collections import namedtuple
from typing import Any
from eth_typing import HexAddress
from staking_deposit.credentials import CredentialList
from staking_deposit.exceptions import ValidationError
from staking_deposit.settings import get_chain_setting, GOERLI
from staking_deposit.utils.constants import MAX_DEPOSIT_AMOUNT, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME
from staking_deposit.utils.intl import load_text
from staking_deposit.utils.validation import verify_deposit_data_json
from typing import List

DepositData = namedtuple("DepositData", "pubkey withdrawal_credentials signature deposit_data_root")


class ValidatorKey:
    priv_key_files = []
    deposit_data = []

    def generate_keys(self, mnemonic, validator_start_index: int,
                      num_validators: int, folder: str, chain: str, keystore_password: str,
                      eth1_withdrawal_address: HexAddress, **kwargs: Any):
        mnemonic_password = ""
        amounts = [MAX_DEPOSIT_AMOUNT] * num_validators
        folder = os.path.join(folder, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
        chain_setting = get_chain_setting(chain)
        if not os.path.exists(folder):
            os.mkdir(folder)
        credentials = CredentialList.from_mnemonic(
            mnemonic=mnemonic,
            mnemonic_password=mnemonic_password,
            num_keys=num_validators,
            amounts=amounts,
            chain_setting=chain_setting,
            start_index=validator_start_index,
            hex_eth1_withdrawal_address=eth1_withdrawal_address,
        )
        self.priv_key_files = credentials.export_keystores(password=keystore_password, folder=folder)
        self.deposit_data = credentials.export_deposit_data_json(folder=folder)
        if not credentials.verify_keystores(keystore_filefolders=self.priv_key_files, password=keystore_password):
            raise ValidationError(load_text(['err_verify_keystores']))
        if not verify_deposit_data_json(self.deposit_data, credentials.credentials):
            raise ValidationError(load_text(['err_verify_deposit']))
        return self.priv_key_files, self.deposit_data

    def get_deposit_data(self, deposit_data_file) -> List[DepositData]:
        with open(deposit_data_file, "r") as file:
            deposit = json.load(file)
        file.close()
        data = []
        for key in deposit:
            data.append(
                DepositData(key["pubkey"], key["withdrawal_credentials"], key["signature"], key["deposit_data_root"]))
        return data
