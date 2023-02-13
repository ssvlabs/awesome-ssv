import json
from collections import namedtuple
from eth_typing import HexAddress, HexStr
from ssv.ssv_cli import SSV, OperatorData
from staking_deposit.settings import  GOERLI
from staking_deposit.key_handling.key_derivation.mnemonic import get_mnemonic
from staking_deposit.utils.constants import WORD_LISTS_PATH
import argparse
import time
from utils.eth_connector import EthNode
from utils.stakepool import StakingPool
from utils.ssv_network import SSVNetwork, SSVToken
import traceback
from staking_deposit.validator_key import ValidatorKey
from ssv.ssv_cli import Operator


def read_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    file.close()
    return data


def create_keys(config_file):
    """
    :param config:
    :return:
    """
    config = read_file(config_file)
    validators = ValidatorKey()
    mnemonic = get_mnemonic(language="english", words_path=WORD_LISTS_PATH)
    keystores, deposit_data = validators.generate_keys(mnemonic, 0, config.validator_count, "", GOERLI,
                                                       config.keystore_password, config.withdrawal_creds)
    print("mnemonic used to generate validator keys:")
    print(mnemonic)
    print("Keystore files generated for your validators are:")
    print(keystores)
    print("deposit data for your validator keys are:")
    print(deposit_data)


def create_keyshares(config_file):
    """

    """
    config = read_file(config_file)
    operators = [Operator(operator_data.id, operator_data.pubkey, operator_data.fee, operator_data.name) for
                 operator_data in config.operators]
    for keystore in config.keystore_files:
        ssv = SSV(keystore, config.keystore_password)
        keyshare_file = ssv.generate_shares(operators, config.ssv_fee)
        print("for following keystore file: {} keyshare generated is:{}".format(keystore, keyshare_file))


def start_staking(config_file):
    """

    :return:
    """
    config = read_file(config_file)
    with open("fallback.json", "r") as file:
        fallback = json.load(file)
    file.close()
    try:
        while True:
            mnemonic = get_mnemonic(language="english", words_path=WORD_LISTS_PATH)  # mnemonic
            web3_eth = EthNode(config.eth.rpc, config.eth.priv_key)
            if web3_eth.get_balance(config.staking_pool) >= 32 or len(fallback) > 0:
                stake_pool = StakingPool(config.contract_address.stakepool, web3_eth.eth_node)
                print("balance of staking pool:" + str(web3_eth.get_balance(config.staking_pool)))
                num_validators = int(web3_eth.get_balance(config.staking_pool) / 32)
                print("creating validators")
                validators = ValidatorKey()
                keystores, deposit_file = validators.generate_keys(mnemonic=mnemonic, validator_start_index=1,
                                                                     num_validators=num_validators, folder="",
                                                                     chain=GOERLI,
                                                                     keystore_password=config.keystore_pass,
                                                                     eth1_withdrawal_address=HexAddress(
                                                                         HexStr(stake_pool.get_withdrawal_address())))
                print("keys created are:\n")
                print(keystores)
                print("submitting validators")
                for index, cred in enumerate(validators.get_deposit_data(file)):
                    tx = stake_pool.deposit_validator(cred.pubkey,
                                                      cred.withdrawal_credentials,
                                                      cred.signature,
                                                      cred.deposit_data_root,
                                                      web3_eth.account.address)
                    web3_eth.make_tx(tx)
                    fallback[cred.pubkey.hex()] = {"keystore": keystores[index], "ssv_share": ""}
                    print("deposit the key" + str(cred.pubkey))
                print("submitted validators\n")
                operator_id = stake_pool.get_operator_ids()
                print("operator ids are:\n")
                print(operator_id)
                ssv_contract = SSVNetwork(config.contract_address.ssv_network, web3_eth.eth_node)
                ssv_token = SSVToken(config.contract_address.ssv_token, web3_eth.eth_node)
                network_fees = 0 if ssv_contract.get_network_fee() is None else ssv_contract.get_network_fee()
                print("network fee is:\n")
                print(network_fees)
                pubkeys = list(fallback.keys())
                for pubkey in pubkeys:
                    ssv = SSV(fallback[pubkey]["keystore"], "test1234")
                    if fallback[pubkey]["ssv_share"] == "":
                        op = OperatorData("https://api.ssv.network")
                        file = ssv.generate_shares(op.get_operator_data(operator_id), network_fees)
                        fallback[pubkey]["ssv_share"] = file
                        shares = ssv.get_keyshare(file)
                    else:
                        shares = ssv.get_keyshare(fallback[pubkey]["ssv_share"])
                    if ssv_token.get_balance(web3_eth.eth_node.toChecksumAddress(config.staking_pool)) < int(
                            shares["ssvAmount"]):
                        print("ssv token balance of stakepool is less than the required amount. Sending some tokens")
                        if ssv_token.get_balance(
                                web3_eth.eth_node.toChecksumAddress(web3_eth.account.address)) > 2 * int(
                            shares["ssvAmount"]):
                            tx = ssv_token.transfer_token(web3_eth.eth_node.toChecksumAddress(config.staking_pool),
                                                          2 * int(shares["ssvAmount"]), web3_eth.account.address)
                            web3_eth.make_tx(tx)
                            print("Added SSV tokens to stakepool account")
                        elif ssv_token.get_balance(web3_eth.eth_node.toChecksumAddress(web3_eth.account.address)) > int(
                                shares["ssvAmount"]):
                            tx = ssv_token.transfer_token(web3_eth.eth_node.toChecksumAddress(config.staking_pool),
                                                          int(shares["ssvAmount"]), web3_eth.account.address)
                            web3_eth.make_tx(tx)
                            print(
                                "WARNING!!!! Balance too low for account and stakepool for SSV tokens. Please add some")
                        else:
                            raise Exception(
                                "ERROR!!!! keys shares not added as your account doesn't have enough SSV tokens")
                    tx = stake_pool.send_key_shares(shares["validatorPublicKey"], operator_id,
                                                    shares["sharePublicKeys"], shares["sharePrivateKey"],
                                                    int(shares["ssvAmount"]),
                                                    web3_eth.account.address)
                    web3_eth.make_tx(tx)
                    print("ssv shares submitted to the contract")
                    fallback.pop(pubkey)
                fallback = {}
            else:
                print("pool balance less than 32")
                time.sleep(10)
                print("trying again")
    except Exception as err:
        print(traceback.format_exc())
        print(fallback)
        with open("fallback.json", "w") as file:
            json.dump(fallback, file)
        file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Command line tool for SSV backend")
    subparses = parser.add_subparsers()
    stake = subparses.add_parser("stake",
                                 help="used to start a service that tracks stakinpool contract for keys and key shares")
    stake.set_defaults(which="stake")

    keys = subparses.add_parser("create-keys", help="create n keys and their keyshares")
    keys.set_defaults(which="keys")

    keyshares = subparses.add_parser("generate-keyshares", help="generate ssv keyshares from validator keystore files")
    keyshares.set_defaults(which="keyshares")

    stake.add_argument("-c", "--config", help="pass a config file with required params. Refer README", required=True)
    keys.add_argument("-c", "--config", help="pass a config file with required params. Refer README", required=True)
    keyshares.add_argument("-c", "--config", help="pass a config file with required params. Refer README",
                           required=True)

    args = parser.parse_args()
    if args.which == "keys":
        create_keys(args.config)
    elif args.which == "stake":
        start_staking(args.config)
    elif args.which == "keyshares":
        create_keyshares(args.config)