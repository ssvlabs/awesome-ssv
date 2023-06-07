#!/usr/bin/python3
import time

from brownie import *
from scripts.utils.helpers import *
import json


def main():

    deployer = get_deployer()

    # TODO OPTIONAL update these values
    whitelist = "0x49c5e038dc918F841589cE517fF975A4429eEb5c"
    withdrawal_creds = "0x44449d7cA8e3724cb9c9E30Ce49B286e275D79bf"
    operator_ids = [4, 9, 17, 76]

    deposit_contract = "0xff50ed3d0ec03ac01d4c79aad74928bff48a7b2b"
    ssv_network_contract = "0xAfdb141Dd99b5a101065f40e3D7636262dce65b3"
    ssv_token_address = "0x3a9f01091C446bdE031E39ea8354647AFef091E7"

    # ssvETH = "0xfcE8F661AbBf1417E6f73593B9cf779aF83501a9"
    # stakingPool = "0xFc6f35B3D7e7d6c5789bC2c3566d8b1E9E11752a"

    print("deploying ssvETH...")
    # ssvETH = SSVETH.deploy({'from': deployer})
    # print('ssvETH deployed to: ', ssvETH.address)

    print("deploying staking Pool...")
    stakingPool = StakingPool.deploy(whitelist, deposit_contract, withdrawal_creds,
                                     ssv_network_contract, ssv_token_address, operator_ids, {'from': deployer, 'gas_price': 875000000000})  # to change nonce  add "'nonce': 142" into the curly brackets
    print("staking pool deployed to:", stakingPool.address)
    time.sleep(3)

    print("trasferring minting ownership...")
    ssvETH = SSVETH.at(stakingPool.ssvETH())
    ssvETH.transferOwnership(stakingPool.address, {
                             'from': deployer, 'gas_price': 875000000000})

    print("testing staking...")
    stakingPool.stake({'value': 65 * 10 ** 18,
                      'from': deployer, 'gas_price': 875000000000})

    print("testing unStaking...")

    ssvETH.approve(stakingPool.address, 0.001 * 10 ** 18,
                   {'from': deployer, 'gas_price': 875000000000})
    stakingPool.unStake(
        0.001 * 10 ** 18, {'from': deployer, 'gas_price': 875000000000})

    with open('contrat_addresses.json', "r") as f:
        data = json.load(f)

    data["stakingPool_addr"] = stakingPool.address
    data["ssvETH_addr"] = ssvETH.address

    print("writing contract addresses into contrat_addresses.json")
    with open('contrat_addresses.json', 'w') as f:
        json.dump(data, f)
