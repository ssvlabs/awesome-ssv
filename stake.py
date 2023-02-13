import json
import sys
import time
import traceback
from collections import namedtuple

from eth_typing import HexAddress, HexStr

from ssv.ssv_cli import SSV, OperatorData, Operator
from staking_deposit.settings import GOERLI
from staking_deposit.utils.constants import WORD_LISTS_PATH

from staking_deposit.key_handling.key_derivation.mnemonic import get_mnemonic
from staking_deposit.validator_key import ValidatorKey
from utils.eth_connector import EthNode
from utils.ssv_network import SSVNetwork, SSVToken
from utils.stakepool import StakingPool


def read_file(file_path):
    """
    This is used to read params from json file and convert them to python Namespaces
    :param file_path: takes the json filepath
    :returns: it returns data in form of python Namespace
    """
    with open(file_path, "r") as file:
        data = json.load(file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    file.close()
    return data


def start_staking(config_file):
    """
    This is an entry function for command line argument stake.
    Following are the actions performed by it:
    [1] It is used to run the backend for stakepool contract.
    [2] It regularly monitors the balances of the stakepool contract and submits keys and keyshares.
    [3] It also monitors the balance of SSV token in the stakepool contract and sends some SSV token from whitelist address
    [4] In the case of script failure it creates a fallabck file which stores the state of the system. Upon resuming the
     service it
    :param config_file: Refer sample_config(stake-config.json) folder for config file params
    :return: Null
    """
    config = read_file(config_file)
    with open("fallback.json", "r") as file:
        fallback = json.load(file)  # used to store the state of the system
    file.close()
    try:
        while True:
            mnemonic = get_mnemonic(language="english", words_path=WORD_LISTS_PATH)  # mnemonic
            web3_eth = EthNode(config.eth.rpc, config.eth.priv_key)
            if web3_eth.get_balance(config.contract_address.stakepool) >= 32 or len(fallback) > 0:
                stake_pool = StakingPool(config.contract_address.stakepool, web3_eth.eth_node)
                print("balance of staking pool:" + str(web3_eth.get_balance(config.contract_address.stakepool)))
                num_validators = int(web3_eth.get_balance(config.contract_address.stakepool) / 32)
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
                for index, cred in enumerate(validators.get_deposit_data(deposit_file)):
                    tx = stake_pool.deposit_validator(cred.pubkey,
                                                      cred.withdrawal_credentials,
                                                      cred.signature,
                                                      cred.deposit_data_root,
                                                      web3_eth.account.address)
                    web3_eth.make_tx(tx)
                    fallback[cred.pubkey] = {"keystore": keystores[index], "ssv_share": ""}
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
                    ssv = SSV(fallback[pubkey]["keystore"], config.keystore_pass)
                    if fallback[pubkey]["ssv_share"] == "":
                        operator_data = [Operator(1,"LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBMVg2MUFXY001QUNLaGN5MTlUaEIKby9HMWlhN1ByOVUralJ5aWY5ZjAyRG9sd091V2ZLLzdSVUlhOEhEbHBvQlVERDkwRTVQUGdJSy9sTXB4RytXbwpwQ2N5bTBpWk9UT0JzNDE5bEh3TzA4bXFja1JsZEg5WExmbmY2UThqWFR5Ym1yYzdWNmwyNVprcTl4U0owbHR1CndmTnVTSzNCZnFtNkQxOUY0aTVCbmVaSWhjRVJTYlFLWDFxbWNqYnZFL2cyQko4TzhaZUgrd0RzTHJiNnZXQVIKY3BYWG1uelE3Vlp6ZklHTGVLVU1CTTh6SW0rcXI4RGZ4SEhSeVU1QTE3cFU4cy9MNUp5RXE1RGJjc2Q2dHlnbQp5UE9BYUNzWldVREI3UGhLOHpUWU9WYi9MM1lnSTU4bjFXek5IM0s5cmFreUppTmUxTE9GVVZzQTFDUnhtQ2YzCmlRSURBUUFCCi0tLS0tRU5EIFJTQSBQVUJMSUMgS0VZLS0tLS0K",0, "Bloxstaking"),
                                         Operator(2,"LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBeUtVWTVEUmZZREljengzcjhVY0UKTlpFMFdIQXFuV2FIRjZYRlUydVdObjVOVE94Zkt4ZmZaLzkyeVE1citQVkJPRmQrcHhILzI2QXJVT3dNL1lBRQpRbDZ0VzBtc1FqdUtIU1Q4aUtvTDRTNUt0aDNoeTBqeFRHR1ZZaWdjWG1vRURjd2YxaG8wdWRxRmlEN3dFWXN1CmZHa2E2U1ZQNnBab1NMaU9HZFRKUWVzVDI5WEVCdDZnblhMaFB1MER2K0xsQUJJQ1pqWEFTZWtpSFVKUHRjYlgKRjZFL0lScGpkWHVNSmUyOXZDcmZudXhWWk93a1ptdzJXdGljYlNDOVJpSFRYWUQ1dnVGakZXRHNZMERHUDhzOAoyc1haVHdsNWl4dEhlUWM2N1lLRFN6YU1MNnY1VUVZblhUTzZzNHFVSWVnTXJwZjd3S0xGVWxqRTMwbnNIaVBUCjBRSURBUUFCCi0tLS0tRU5EIFJTQSBQVUJMSUMgS0VZLS0tLS0K",0, "Bloxstaking2"),
                                         Operator(9,"LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBelc5VGNJMWxXbmUydkNqZzJlb2UKY3o3NnZ4OVU2QWgvTnZRT0dJY1JTbk5mUWc1amxjM0JuTUM4eW1pQTQzVHJDejl6UFVhUVozZG5idW9DZEY3awpoOWZKcVd3SFFrU2pFQ1ZtVytQS2FVWmQ4aW42cGVGbmgrZEowenR1cUx1aUlJMWQvU05xdGJUaFA2VjQ4TGxDCklsVUhXVFRaKzNVY2dBanlwenIxRmxYU2hGV0w0aGcxeXF3K0p1WW1yTnY2cGZaeWdVbTZQaTBVazVXUVZnUk4KR2RrU3BTb2ZYZERGcElWN0xBU3V0a2dGUytqVnpaL3E5bmh1ejVjNlJWaDYvV1hiZVpDbXhnMGU2R2hIVXY0bAp4SGNaSUkraWhzWk5KM3V5b2NiaWlubE5EaTNMK2hySEUxMExNeVRoN2lVSC8yd1k4MjJKMmdDSEZzNWhkVkNrCm53SURBUUFCCi0tLS0tRU5EIFJTQSBQVUJMSUMgS0VZLS0tLS0K",0, "Bloxstaking3"),
                                         Operator(42,"LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBNVV3SFltUnJoL3hwbWovd1RHcWwKLysvZEdNWFFlSkg0VUptSjNNWXhyMUU0aGF4ZkhLK3NzSkhXYzYvbWlpRTdZMTBxcy9sNzRvNHdGNnJ2SXYrVApTYnQ2UjdONXNKYUZsYnZ3M2ZCampiZElQTnBHQ0JTaXl3aTc3M3lQZy8vOG04OHMxNTNwYjZmVnViU2QxMzJWClpEZkhmMEdPdnA4b0hxcHY5ampsQ0NlV2phNXUzVzhqN2RwWDBsQTYvaTJRaW4yN3VESHViMHd1eWFEcGprNDcKWG1tOHV2d1VFTWw1L0trREg3Z2FXUjNzNkluZjR4TVpKbHEvMGplVkdoUll5bHg3RFE1WnVBNDNCSGNGMWtxMAo3ZHU0ejFUQ2tFN0ZIZlZRMTdFUnpwUHlmS2l5YlQ4UXdnb3VVV2hGUjJqK3ExbHZGbHJQR0U2OWpIWE9MVWM0CnV3SURBUUFCCi0tLS0tRU5EIFJTQSBQVUJMSUMgS0VZLS0tLS0K",0, "Bloxstaking4")]
                        file = ssv.generate_shares(operator_data, network_fees)
                        fallback[pubkey]["ssv_share"] = file
                        shares = ssv.get_keyshare(file)
                    else:
                        shares = ssv.get_keyshare(fallback[pubkey]["ssv_share"])
                    if ssv_token.get_balance(web3_eth.eth_node.toChecksumAddress(config.contract_address.stakepool)) < int(
                            shares["ssvAmount"]):
                        print("ssv token balance of stakepool is less than the required amount. Sending some tokens")
                        if ssv_token.get_balance(
                                web3_eth.eth_node.toChecksumAddress(web3_eth.account.address)) > 2 * int(
                            shares["ssvAmount"]):
                            tx = ssv_token.transfer_token(web3_eth.eth_node.toChecksumAddress(config.contract_address.stakepool),
                                                          2 * int(shares["ssvAmount"]), web3_eth.account.address)
                            web3_eth.make_tx(tx)
                            print("Added SSV tokens to stakepool account")
                        elif ssv_token.get_balance(web3_eth.eth_node.toChecksumAddress(web3_eth.account.address)) > int(
                                shares["ssvAmount"]):
                            tx = ssv_token.transfer_token(web3_eth.eth_node.toChecksumAddress(config.contract_address.stakepool),
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
    config_file = sys.argv[1]
    start_staking(config_file)