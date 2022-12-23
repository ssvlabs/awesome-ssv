from brownie import *
from scripts.utils.helpers import *
import json


def main():

    deployer = get_deployer()

    print("deploying ...")
    depositContract = DepositContract.deploy(
        {'from': deployer, 'gas_price': 8750000000})
