import os
from typing import Any
from eth_typing import HexAddress, HexStr

from ssv.ssv_cli import SSV, OperatorData
from staking_deposit.credentials import CredentialList
from staking_deposit.exceptions import ValidationError
from staking_deposit.settings import get_chain_setting, GOERLI
from staking_deposit.utils.constants import MAX_DEPOSIT_AMOUNT, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME
from staking_deposit.utils.intl import load_text
from staking_deposit.utils.validation import verify_deposit_data_json
from staking_deposit.key_handling.key_derivation.mnemonic import get_mnemonic
from staking_deposit.utils.constants import WORD_LISTS_PATH


def generate_keys(validator_start_index: int,
                  num_validators: int, folder: str, chain: str, keystore_password: str,
                  eth1_withdrawal_address: HexAddress, **kwargs: Any):
    mnemonic = get_mnemonic(language="english", words_path=WORD_LISTS_PATH)
    print(mnemonic)
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
    keystore_filefolders = credentials.export_keystores(password=keystore_password, folder=folder)
    deposits_file = credentials.export_deposit_data_json(folder=folder)
    if not credentials.verify_keystores(keystore_filefolders=keystore_filefolders, password=keystore_password):
        raise ValidationError(load_text(['err_verify_keystores']))
    if not verify_deposit_data_json(deposits_file, credentials.credentials):
        raise ValidationError(load_text(['err_verify_deposit']))
    return credentials, keystore_filefolders, deposits_file


if __name__ == '__main__':
    credentials, keystores, deposit_file = generate_keys(validator_start_index=1, num_validators=2, folder="",
                                                         chain=GOERLI,
                                                         keystore_password="test", eth1_withdrawal_address=HexAddress(
            HexStr("0x70997970C51812dc3A010C7d01b50e0d17dc79C8")))
    for keyfile in keystores:
        ssv = SSV(keyfile,"test")
        op = OperatorData("https://api.ssv.network")
        file = ssv.generate_shares(op.get_operator_data([1, 2, 9, 42]))
        ssv.stake_shares(file)
