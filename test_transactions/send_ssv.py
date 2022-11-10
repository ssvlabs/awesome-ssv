import sys

from web3 import Web3

web_th = Web3(Web3.HTTPProvider(sys.argv[1]))


def send_ssv(priv_key, amount, address_ssv, address_stakepool):
    abi_token_ssv = [{
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }]
    account = web_th.eth.account.privateKeyToAccount(priv_key)
    ssv_token = web_th.eth.contract(abi=abi_token_ssv, address=Web3.toChecksumAddress(address_ssv))
    tx = ssv_token.functions.transfer(address_stakepool, amount * 10 ** 18).buildTransaction(
        {'from': account.address, 'gasPrice': web_th.toWei('2', 'gwei'), 'gas': 5000000})
    tx['nonce'] = web_th.eth.get_transaction_count(account.address)
    signed_tx = web_th.eth.account.sign_transaction(tx, account.key)
    tx_hash = web_th.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web_th.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
    if tx_receipt.status == 1:
        print('TX successful')
    else:
        print('TX reverted')


if __name__ == '__main__':
    send_ssv(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
