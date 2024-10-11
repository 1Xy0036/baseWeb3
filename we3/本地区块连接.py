from web3 import Web3

ganache='HTTP://127.0.0.1:7545'

web3=Web3(Web3.HTTPProvider(ganache))

if web3.is_connected:
    print("本地区块连接成功")
else:
    print("连接失败!!")

account_1='0x134BCA58ad52D4c72c7D898aDD8F32DE315742f2'
account_2='0x3D3c4e0D93C0c6ad463f377FC1A0A1Cfc0225614'
privact_key='0xb39b8b37fdde71bf0b7f68f4bc27d39d58260005377539c9d3742c5da59a9c34'

#get the nonce
nonce=web3.eth.get_transaction_count(account_1)
#build a transaction 
tx={
    'nonce':nonce,
    'to':account_2,
    'value':web3.to_wei(1,'ether'),
    'gas':2000000,
    'gasPrice':web3.to_wei('50','gwei')
}

signed_tx=web3.eth.account.sign_transaction(tx,privact_key)

tx_hash=web3.eth.send_raw_transaction(signed_tx.raw_transaction)
print(web3.to_hex(tx_hash))