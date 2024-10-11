from web3 import Web3
import time

# 通过 Infura 连接到以太坊主网
INFURA_URL = 'https://mainnet.infura.io/v3/0c1276f560db4dd5840c8b787cd443ad'
web3 = Web3(Web3.HTTPProvider(INFURA_URL))  # 使用 HTTPProvider 连接到以太坊

# 检查与以太坊主网的连接状态
if not web3.is_connected():
    print("连接到以太坊失败")
    exit()
else:
    print("成功连接到以太坊主网")

# 需要监控的合约地址
contract_address = '0x8143182a775c54578c8b7b3ef77982498866945d'

# 获取当前区块号
current_block = web3.eth.block_number
print(f"当前区块号: {current_block}")

# 处理每笔交易的函数
def handle_transaction(tx):
    if tx['to']:  # 确保交易有目标地址
        print(f"交易哈希: {tx['hash'].hex()}，发往: {tx['to']}")
        if tx['to'].lower() == contract_address.lower():  # 检查目标地址是否为合约地址
            print(f"发现与目标合约相关的交易: {tx['hash'].hex()}")
            print(f"""
            发起地址: {tx['from']}
            目标地址: {tx['to']}
            交易金额: {web3.from_wei(tx['value'], 'ether')} ETH
            Gas 费用: {tx['gas']}
            Gas 单价: {web3.from_wei(tx['gasPrice'], 'gwei')} Gwei
            """)

# 轮询新区块，监控交易
def monitor_contract():
    global current_block  # 使用全局变量存储当前区块号
    while True:
        try:
            # 获取最新区块号
            latest_block = web3.eth.block_number
            
            # 如果有新块产生（最新区块号比当前区块号大）
            if latest_block > current_block:
                print(f"检查区块 {current_block} 到 {latest_block} 的交易...")
                
                # 遍历每个新块中的交易
                for block_num in range(current_block + 1, latest_block + 1):
                    block = web3.eth.get_block(block_num, full_transactions=True)  # 获取区块中的所有交易
                    print(f"区块 {block_num} 包含 {len(block.transactions)} 个交易")  # 打印当前区块的交易数量
                    
                    # 遍历该区块中的所有交易
                    for tx in block.transactions:
                        handle_transaction(tx)  # 调用处理函数处理每笔交易

                # 更新当前区块号
                current_block = latest_block

            # 设置轮询的时间间隔，避免过度请求
            time.sleep(15)  # 每15秒检查一次

        except Exception as e:
            print(f"发生错误: {e}")
            time.sleep(15)  # 出现错误后等待15秒再重试

# 开始监听合约交易
monitor_contract()
