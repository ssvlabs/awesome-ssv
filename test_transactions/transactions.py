from web3 import Web3

web_th = Web3(Web3.HTTPProvider("http://localhost:8545"))
abi = [{
    "inputs": [],
    "name": "stake",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
}]
# print(web_th.eth.get_balance("0x2279B7A0a67DB372996a5FaB50D91eAA73d2eBe6"))
# exit()
account = web_th.eth.account.privateKeyToAccount("0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80")
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
ssv = web_th.eth.contract(abi=abi_token_ssv, address="0x0165878A594ca255338adfa4d48449f69242Eb8F")
tx = ssv.functions.transfer("0xc351628EB244ec633d5f21fBD6621e1a683B1181",100000000000000000000).buildTransaction()
# pool = web_th.eth.contract(abi=abi, address="0x7bc06c482DEAd17c0e297aFbC32f6e63d3846650")
# abi_token = [{
#     "inputs": [
#         {
#             "internalType": "address",
#             "name": "account",
#             "type": "address"
#         }
#     ],
#     "name": "balanceOf",
#     "outputs": [
#         {
#             "internalType": "uint256",
#             "name": "",
#             "type": "uint256"
#         }
#     ],
#     "stateMutability": "view",
#     "type": "function"
# }]
#
# # token = web_th.eth.contract(abi=abi_token, address="0x7a2088a1bFc9d81c55368AE168C2C02570cB814F")
# # print(token.functions.balanceOf(account.address).call())
# tx = pool.functions.stake().buildTransaction({"value": 32 * (10 ** 18)})
tx['nonce'] = web_th.eth.get_transaction_count(account.address)
signed_tx = web_th.eth.account.sign_transaction(tx, account.key)
tx_hash = web_th.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = web_th.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
if tx_receipt.status == 1:
    print('TX successful')
else:
    print('TX reverted')
