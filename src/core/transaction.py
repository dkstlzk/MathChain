import hashlib
import json
from dataclasses import dataclass, asdict


@dataclass
class Transaction:    
    sender: str
    receiver: str
    amount: float
    timestamp: float
    
    def to_dict(self):
        return asdict(self)
    
    def compute_hash(self):
        tx_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()