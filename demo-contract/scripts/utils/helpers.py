#!/usr/bin/python3

from brownie import *
import brownie.network as network
from brownie.network import max_fee, priority_fee


def get_deployer():
    if network.show_active() in ["goerli", "mainnet"]:
        if network.show_active() == "mainnet":
            priority_fee("2 gwei")
            max_fee("25 gwei")
            account_name = "live_deployer"
        else:
            # TODO change to your wallet name
            account_name = "deployer"

        if network.show_active() == "mainnet-fork":
            publish = False
        else:
            publish = False
        deployer = accounts.load(account_name)

    else:
        deployer = accounts[0]
        publish = False
    return(deployer)


def load_contract(addr):
    if addr == ZERO_ADDRESS:
        return None
    try:
        cont = Contract(addr)
    except ValueError:
        cont = Contract.from_explorer(addr)
    return cont
