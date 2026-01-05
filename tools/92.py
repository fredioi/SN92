import bittensor as bt
import asyncio

subtensor = bt.Subtensor(network="finney")

# 获取指定子网的metagraph
netuid = 92  # 假设我们要查询netuid为92的子网
metagraph = subtensor.metagraph(netuid)

# 获取当前区块
current_block = subtensor.get_current_block()

# 获取所有验证者UID（在线的）
validator_uids = []
for uid in range(len(metagraph.neurons)):
    # 检查是否为验证者（validator_permit为True）且最近有更新
    if metagraph.validator_permit[uid] and (current_block - metagraph.last_update[uid] < 360):
        validator_uids.append(uid)
print("")
print("="*180)
print(f"在线验证者UID列表 (netuid {netuid}):".center(180))
print("="*180)
print(f"{'UID':<6} {'权限':<8} {'排放':<15} {'质押':<13} {'vtrust':<13} {'更新区块':<10} {'Hotkey':<45} {'Coldkey':<45}")
print("-"*180)
for uid in validator_uids:
    permit_status = "已授权" if metagraph.validator_permit[uid] else "未授权"
    neuron = metagraph.neurons[uid]
    last_update_blocks = current_block - metagraph.last_update[uid]
    emission = metagraph.E[uid]  # E代表emission（排放）
    stake = metagraph.S[uid]  # S代表stake（质押）
    vtrust = metagraph.validator_trust[uid]  # validator_trust代表验证者信任度
    print(f"{uid:<6} {permit_status:<8} {emission:<15.6f} {stake:<15.2f} {vtrust:<15.6f} {last_update_blocks:<10} {neuron.hotkey:<45} {neuron.coldkey:<45}")

print(f"\n总计: {len(validator_uids)} 个在线验证者")
print("="*180)

# 获取所有有有效axon信息的矿工UID
miner_uids = []
for uid in range(len(metagraph.neurons)):
    # 检查是否为矿工（非验证者）且有有效的axon信息
    axon_info = metagraph.axons[uid]
    if not metagraph.validator_permit[uid] and axon_info and axon_info.ip and axon_info.port:
        miner_uids.append(uid)

# 创建一个钱包用于dendrite连接（使用默认的查询钱包）
wallet = bt.Wallet(name="default")
dendrite = bt.Dendrite(wallet=wallet)

# 检查哪些矿工可以连接
online_miner_uids = []
for uid in miner_uids:
    try:
        axon_info = metagraph.axons[uid]
        
        # 发送一个基本的ping请求到矿工的axon
        responses = dendrite.query(
            [axon_info],
            bt.Synapse(),
            timeout=5  # 设置5秒超时
        )
        
        # 检查响应状态
        if responses and len(responses) > 0:
            response = responses[0]
            if response.dendrite.status_code == 200:
                online_miner_uids.append(uid)
    except Exception:
        # 忽略连接异常，继续下一个
        continue

print(f"在线矿工UID列表 (netuid {netuid}):".center(180))
print("="*180)
print(f"{'UID':<6} {'排放':<15} {'质押':<15} {'Hotkey':<60} {'Coldkey':<60}")
print("-"*180)
for uid in online_miner_uids:
    neuron = metagraph.neurons[uid]
    emission = metagraph.E[uid]  # E代表emission（排放）
    stake = metagraph.S[uid]  # S代表stake（质押）
    print(f"{uid:<6} {emission:<15.6f} {stake:<15.2f} {neuron.hotkey:<60} {neuron.coldkey:<60}")

print(f"\n总计: {len(online_miner_uids)} 个在线矿工")
print("="*180)