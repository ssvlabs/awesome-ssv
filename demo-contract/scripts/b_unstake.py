#!/usr/bin/python3

from brownie import *
from scripts.utils.helpers import *
import json


def main():

    deployer = get_deployer()

    # TODO change poolAddress, for your pool address which you can find printed on your console
    with open('contrat_addresses.json', "r") as f:
        contract_addresses = json.load(f)

    stakingPoolAddress = contract_addresses["stakingPool_addr"]

    stakingPool = StakingPool.at(stakingPoolAddress)

    print("staking...")
    stakingPool.stake({'value': 32 * 10 ** 18, 'from': deployer})

    # data["stakingPool_addr"] = stakingPool.address
    # data["ssvETH_addr"] = ssvETH.address

    # with open('contrat_addresses.json', 'w') as f:
    #     json.dump(data, f)
