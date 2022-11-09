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
import argparse
import time
from utils.eth_connector import EthNode
from utils.stakepool import StakingPool
from utils.ssv_network import SSVNetwork


def generate_keys(mnemonic, validator_start_index: int,
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
    keystore_filefolders = credentials.export_keystores(password=keystore_password, folder=folder)
    deposits_file = credentials.export_deposit_data_json(folder=folder)
    if not credentials.verify_keystores(keystore_filefolders=keystore_filefolders, password=keystore_password):
        raise ValidationError(load_text(['err_verify_keystores']))
    if not verify_deposit_data_json(deposits_file, credentials.credentials):
        raise ValidationError(load_text(['err_verify_deposit']))
    return credentials, keystore_filefolders, deposits_file


def create_keys(config):
    """

    :param config:
    :return:
    """
    mnemonic = get_mnemonic(language="english", words_path=WORD_LISTS_PATH)

    credentials, keystores, deposit_file = generate_keys(mnemonic=mnemonic, validator_start_index=1,
                                                         num_validators=config.number_count, folder="",
                                                         chain=GOERLI,
                                                         keystore_password=config.keystore_password,
                                                         eth1_withdrawal_address=HexAddress(
                                                             HexStr(config.withdrawal_credential)))
    print("Keys and shares creates are present in the following files:")
    for keyfile in keystores:
        ssv = SSV(keyfile, config.keystore_password)
        file = ssv.generate_shares(config.operator_ids, network_fees=0)
        print("Validator private key file:")
        print(keyfile)
        print("SSV key shares file:")
        print(file)
    print("for making deposit to deposit contract via launchpad or yourself you can use the following file:")
    print(deposit_file)


def start_staking(config):
    """

    :return:
    """
    while True:
        mnemonic = get_mnemonic(language="english", words_path=WORD_LISTS_PATH)
        web3_eth = EthNode(config.eth_rpc, config.private_key)
        if web3_eth.get_balance(config.staking_pool) >= 32:
            print("balance of staking pool:" + str(web3_eth.get_balance(config.staking_pool)))
            num_validators = int(web3_eth.get_balance(config.staking_pool) / 32)

            stake_pool = StakingPool(config.staking_pool, web3_eth.eth_node)
            print("creating validators")
            credentials, keystores, deposit_file = generate_keys(mnemonic=mnemonic, validator_start_index=1,
                                                                 num_validators=num_validators, folder="",
                                                                 chain=GOERLI,
                                                                 keystore_password="test1234",
                                                                 eth1_withdrawal_address=HexAddress(
                                                                     HexStr(stake_pool.get_withdrawal_address())))
            print("keys created are:\n")
            print(keystores)
            print("submitting validators")

            for cred in credentials.credentials:
                tx = stake_pool.deposit_validator(cred.deposit_datum_dict["pubkey"],
                                                  cred.deposit_datum_dict["withdrawal_credentials"],
                                                  cred.deposit_datum_dict["signature"],
                                                  cred.deposit_datum_dict["deposit_data_root"],
                                                  web3_eth.account.address)
                web3_eth.make_tx(tx)
                print("deposit the key" + str(cred.deposit_datum_dict["pubkey"]))
            print("submitted validators\n")
            # keystores = ['validator_keys/keystore-m_12381_3600_1_0_0-1665309440.json', 'validator_keys/keystore-m_12381_3600_2_0_0-1665309440.json']
            operator_id = stake_pool.get_operator_ids()
            print("operator ids are:\n")
            print(operator_id)
            ssv_contract = SSVNetwork(config.ssv_contract, web3_eth.eth_node)
            network_fees = 0 if ssv_contract.get_network_fee() is None else ssv_contract.get_network_fee()
            print("network fee is:\n")
            print(network_fees)
            for keyfile in keystores:
                ssv = SSV(keyfile, "test1234")
                op = OperatorData("https://api.ssv.network")
                file = ssv.generate_shares(op.get_operator_data(operator_id), network_fees)
                shares = ssv.stake_shares(file)
                tx = stake_pool.send_key_shares(shares["validatorPublicKey"], operator_id,
                                                shares["sharePublicKeys"], shares["sharePrivateKey"],
                                                int(shares["ssvAmount"]),
                                                web3_eth.account.address)
                web3_eth.make_tx(tx)
            else:
                print("pool balance less than 32")
        time.sleep(10)
        print("trying again")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Command line tool for SSV backend",
                                     usage='''
                                     
                                     '''

                                     )
    subparses = parser.add_subparsers()
    stake = subparses.add_parser("stake",
                                 help="used to start a service that tracks stakinpool contract for keys and key shares")
    keys = subparses.add_parser("create-keys", help="create n keys and their keyshares")

    stake.add_argument("-priv", "--private-key",
                       help="Private key for the account you have whitelisted for staking contacts", required=True)
    stake.add_argument("-st", "--staking-pool",
                       help="staking pool contract address", required=True)
    stake.add_argument("-ssv", "--ssv-contract",
                       help="ssv network contract address", required=True)
    stake.add_argument("-eth", "--eth-rpc",
                       help="rpc url for ethereum node", required=True)
    keys.add_argument("-id", "--operator-ids", type=int, nargs="+", required=True,
                      help="operator ids with space in between for which the key shares are to be created")
    keys.add_argument("-n", "--number-count", type=int, required=True,
                      help="Number of keys and keyshares you want to create")
    keys.add_argument("-wc", "--withdrawal-credential", required=True,
                      help="withdrawal credentials to be used for creating validator keys")
    keys.add_argument("-pass", "--keystore-password", required=True,
                      help="keystore password for validator keys")

    args = parser.parse_args()
    if "keystore_password" in args.__dict__:
        create_keys(args)
    else:
        start_staking(args)
