#!/usr/bin/python3

from brownie import *
from scripts.utils.helpers import *
import json


def main():

    deployer = get_deployer()

    print("deploying ...")
    depositContract = DepositContract.deploy(
        {'from': deployer, 'gas_price': 8750000000})

    print("deploying ...")
    ssvNetwork = SSVNetwork.deploy(
        {'from': deployer, 'gas_price': 8750000000})

    print("deploying ...")
    ssvToken = SSVTokenMock.deploy(
        {'from': deployer, 'gas_price': 8750000000})

 # TODO OPTIONAL update these values
    whitelist = "0x0000536dbD99d918092249Ef4eDe4a69A35CccCa"
    withdrawal_creds = "0x0000536dbD99d918092249Ef4eDe4a69A35CccCa"
    operator_ids = [1, 2, 9, 42]

    deposit_contract = depositContract.address
    ssv_network_contract = ssvNetwork.address
    ssv_token_address = ssvToken.address

    print("deploying ssvETH...")
    ssvETH = SSVETH.deploy({'from': deployer, 'gas_price': 8750000000})
    # print('ssvETH deployed to: ', ssvETH.address)

    print("deploying staking Pool...")
    stakingPool = StakingPool.deploy(whitelist, deposit_contract, withdrawal_creds,
                                     ssv_network_contract, ssv_token_address, ssvETH.address, operator_ids, {'from': deployer, 'gas_price': 8750000000})
    # print("staking pool deployed to:", stakingPool.address)

    print("trasferring minting ownership...")
    ssvETH.transferOwnership(stakingPool.address, {
                             'from': deployer, 'gas_price': 8750000000})

    print("staking...")
    stakingPool.stake({'value': 0.001 * 10 ** 18,
                      'from': deployer, 'gas_price': 8750000000})

    print("unStaking...")
    ssvETH.approve(stakingPool.address, 0.001 * 10 ** 18,
                   {'from': deployer, 'gas_price': 8750000000})
    stakingPool.unStake(
        0.001 * 10 ** 18, {'from': deployer, 'gas_price': 8750000000})

    with open('contrat_addresses.json', "r") as f:
        data = json.load(f)

    data["stakingPool_addr"] = stakingPool.address
    data["ssvETH_addr"] = ssvETH.address
    data["deposit_contract_addr"] = deposit_contract
    data["ssv_network_contract_addr"] = ssv_network_contract
    data["ssv_token_address_addr"] = ssv_token_address

    with open('contrat_addresses.json', 'w') as f:
        json.dump(data, f)

    print("addresses written")

    print(".")
    print(".")
    print(".")
    print("all deployed")
