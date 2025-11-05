import hashlib
import json
from dataclasses import dataclass
from typing import List
from .transaction import Transaction
from ..utils.merkle_tree import compute_merkle_root


@dataclass
class Block:    
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    nonce: int = 0
    
    def compute_hash(self):
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def get_merkle_root(self):
        if not self.transactions:
            return hashlib.sha256(b'').hexdigest()
        return compute_merkle_root([tx.compute_hash() for tx in self.transactions])