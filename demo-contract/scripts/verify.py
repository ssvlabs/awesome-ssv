#!/usr/bin/python3

from brownie import *
from scripts.utils.helpers import *
import json


def main():

    deployer = get_deployer()


# TODO export your ETHERSCAN_TOKEN to run this
# export ETHERSCAN_TOKEN=<YOUR TOKEN>

stakingPool = StakingPool.at("<your staking pool contract>")
StakingPool.publish_source(stakingPool)
