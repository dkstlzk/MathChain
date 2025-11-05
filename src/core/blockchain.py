import time
from typing import List, Tuple, Dict
from .block import Block
from .transaction import Transaction


class Blockchain:
    
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis = Block(0, time.time(), [], "0" * 64)
        self.chain.append(genesis)
    
    def add_block(self, transactions: List[Transaction]) -> Block:
        previous_hash = self.chain[-1].compute_hash()
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=transactions,
            previous_hash=previous_hash
        )
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self) -> Tuple[bool, int]:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.previous_hash != previous.compute_hash():
                return False, i
        return True, -1
    
    def get_state(self) -> Dict[str, float]:
        state = {}
        for block in self.chain:
            for tx in block.transactions:
                state[tx.sender] = state.get(tx.sender, 1000.0) - tx.amount
                state[tx.receiver] = state.get(tx.receiver, 0.0) + tx.amount
        return state