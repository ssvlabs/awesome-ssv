#!/usr/bin/python3

from brownie import *
from scripts.utils.helpers import *


def main():

    deployer = get_deployer()

    # TODO change poolAddress, for your pool address which you can find printed on your console
    stakingPoolAddress = "0xe7440EE513760E2b431E07AF300060c3501a2A01"

    stakingPool = StakingPool.at(stakingPoolAddress)

    print("staking...")
    stakingPool.stake({'value': 0.1 * 10 ** 18, 'from': deployer})
