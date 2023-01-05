#!/usr/bin/python3

from brownie import *
from scripts.utils.helpers import *


def main():

    deployer = get_deployer()

    # TODO change poolAddress, for your pool address which you can find printed on your console
    stakingPoolAddress = "0x5c69Aeb46150c6944819e190Bfb7075b4C09024d"

    stakingPool = StakingPool.at(stakingPoolAddress)

    print("staking...")
    stakingPool.stake({'value': 32 * 10 ** 18, 'from': deployer})
