# 导入 Web3 库
from web3 import Web3
import requests
from decimal import Decimal

# 通过 HTTP 连接到新的以太坊节点
web3 = Web3(Web3.HTTPProvider('https://rpc.payload.de'))

# 检查是否连接成功
if web3.is_connected:
    print("Connected to Ethereum network")
else:
    print("Failed to connect")

# 获取当前 gas 价格
gas_price = web3.eth.gas_price
gas_price_gwei = web3.from_wei(gas_price, 'gwei')
print('Current Gas Price:', gas_price_gwei, 'Gwei')

# 获取当前 ETH 价格（使用 CoinGecko API）
response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=cny')
eth_price = Decimal(response.json()['ethereum']['cny'])  # 转换为 Decimal

# 将 gas 价格转换为以太坊并计算人民币
gas_price_eth = Decimal(web3.from_wei(gas_price, 'ether'))  # 转换为 Decimal
gas_price_rmb = gas_price_eth * eth_price

print('Current Gas Price in RMB:', gas_price_rmb)
