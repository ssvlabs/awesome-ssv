#!/usr/bin/python3

from brownie import *
from scripts.utils.helpers import *


def main():

    deployer = get_deployer()

    # TODO change poolAddress, for your pool address just printed on your console
    stakingPoolAddress = "0xa3B53dDCd2E3fC28e8E130288F2aBD8d5EE37472"
    ssvAddress = "0x3a9f01091C446bdE031E39ea8354647AFef091E7"

    ssvToken = load_contract(ssvAddress)

    print("transferring ssv...")
    ssvToken.transfer(stakingPoolAddress, 0.01 * 10**18, {'from': deployer})
