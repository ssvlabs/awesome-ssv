#!/usr/bin/python3

from brownie import *
from scripts.utils.helpers import *
import json


def main():

    deployer = get_deployer()

    # TODO OPTIONAL update these values
    whitelist = "0x123465f75D79AdAEde008E978208cb2Cc28E8B04"
    withdrawal_creds = "0x123465f75D79AdAEde008E978208cb2Cc28E8B04"
    operator_ids = [1, 2, 9, 42]

    deposit_contract = "0xff50ed3d0ec03ac01d4c79aad74928bff48a7b2b"
    ssv_network_contract = "0xb9e155e65B5c4D66df28Da8E9a0957f06F11Bc04"
    ssv_token_address = "0x3a9f01091C446bdE031E39ea8354647AFef091E7"

    # ssvETH = "0xfcE8F661AbBf1417E6f73593B9cf779aF83501a9"
    # stakingPool = "0xFc6f35B3D7e7d6c5789bC2c3566d8b1E9E11752a"

    print("deploying ssvETH...")
    # ssvETH = SSVETH.deploy({'from': deployer, 'gas_price': 8750000000})
    # print('ssvETH deployed to: ', ssvETH.address)

    print("deploying staking Pool...")
    stakingPool = StakingPool.deploy(whitelist, deposit_contract, withdrawal_creds,
                                     ssv_network_contract, ssv_token_address, operator_ids, {'from': deployer, 'gas_price': 8750000000})
    # print("staking pool deployed to:", stakingPool.address)

    # print("trasferring minting ownership...")
    # ssvETH.transferOwnership(stakingPool.address, {
    #                          'from': deployer, 'gas_price': 8750000000})

    print("testing staking...")
    stakingPool.stake({'value': 0.001 * 10 ** 18,
                      'from': deployer, 'gas_price': 8750000000})

    print("testing unStaking...")
    ssvETH = SSVETH.at(stakingPool.ssvETH())
    ssvETH.approve(stakingPool.address, 0.001 * 10 ** 18,
                   {'from': deployer, 'gas_price': 8750000000})
    stakingPool.unStake(
        0.001 * 10 ** 18, {'from': deployer, 'gas_price': 8750000000})

    with open('contrat_addresses.json', "r") as f:
        data = json.load(f)

    data["stakingPool_addr"] = stakingPool.address
    data["ssvETH_addr"] = ssvETH.address

    print("writing contract addresses into contrat_addresses.json")
    with open('contrat_addresses.json', 'w') as f:
        json.dump(data, f)
