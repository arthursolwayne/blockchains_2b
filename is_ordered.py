from web3 import Web3
import random
import json


alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/SFvU9KC-VwMQ2O84dcM-RmeQQ4hPIXj_"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

if w3.is_connected():
    print("Connected to Ethereum node!")
else:
    print("Failed to connect to Ethereum node.")



"""
	Takes a block number
	Returns a boolean that tells whether all the transactions in the block are ordered by priority fee

	Before EIP-1559, a block is ordered if and only if all transactions are sorted in decreasing order of the gasPrice field

	After EIP-1559, there are two types of transactions
		*Type 0* The priority fee is tx.gasPrice - block.baseFeePerGas
		*Type 2* The priority fee is min( tx.maxPriorityFeePerGas, tx.maxFeePerGas - block.baseFeePerGas )

	Conveniently, most type 2 transactions set the gasPrice field to be min( tx.maxPriorityFeePerGas + block.baseFeePerGas, tx.maxFeePerGas )
"""
def is_ordered_block(block_num):
    block = w3.eth.get_block(block_num, full_transactions=True)
    previous_priority_fee = float('inf')
    is_post_eip_1559 = block.get('baseFeePerGas') is not None
    for tx in block.transactions:
        if not is_post_eip_1559 or tx['type'] == 0:
            priority_fee = tx['gasPrice']
        elif tx['type'] == 2:  # For post-EIP-1559 Type 2 transactions
            priority_fee = min(tx['maxPriorityFeePerGas'], tx['maxFeePerGas'] - block['baseFeePerGas'])
        else:
            # If transaction type is not recognized, skip this transaction
            continue
        if priority_fee > previous_priority_fee:
            return False
        previous_priority_fee = priority_fee
    return True


"""
	This might be useful for testing
"""
if __name__ == "__main__":
	latest_block = w3.eth.get_block_number()

	london_hard_fork_block_num = 12965000
	assert latest_block > london_hard_fork_block_num, f"Error: the chain never got past the London Hard Fork"

	n = 5

	for _ in range(n):
        #Pre-London
		block_num = random.randint(1,london_hard_fork_block_num-1)
		ordered = is_ordered_block(block_num)
		if ordered:
			print( f"Block {block_num} is ordered" )
		else:
			print( f"Block {block_num} is ordered" )

        #Post-London
		block_num = random.randint(london_hard_fork_block_num,latest_block)
		ordered = is_ordered_block(block_num)
		if ordered:
			print( f"Block {block_num} is ordered" )
		else:
			print( f"Block {block_num} is ordered" )

