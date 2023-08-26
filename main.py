from web3 import Web3
from config import *
import json


def abi_read(file: object) -> str:
    abi = json.loads(open(file).read())
    return abi


def usdc_approve(private_key, rpc, spender, amount):
    w3 = Web3(Web3.HTTPProvider(rpc))
    acc = w3.eth.account.from_key(private_key)
    address = acc.address

    decimals = 10**6
    amount = int(float(amount) * decimals)

    contract_instance = w3.eth.contract(address=Web3.to_checksum_address('0x2791bca1f2de4661ed88a30c99a7a9449aa84174'), abi=abi_read('abies/USDC_polygon.json'))
    tx = contract_instance.functions.approve(
        spender,
        amount,
    ).build_transaction({
        'from': address,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(acc.address),
        #'value': w3.to_wei(0.000161938112081064, 'ether') + w3.to_wei(value, 'ether')
    })
    sign = acc.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(sign.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_hash.hex()


if __name__ == '__main__':
    spender = '0xBeb09beB09e95E6FEBf0d6EEb1d0D46d1013CC3C'
    with open('private_keys.txt') as file:
        keys = [key.strip() for key in file]
    amount = input("approve amount (USDC): ")
    tx_count = input("num of tx: ")
    for key in keys:
        for i in range(int(tx_count)):
            tx_hash = usdc_approve(key, RPC['polygon'], spender, amount)
            print(f"tx #{i+1}: {tx_hash}")


