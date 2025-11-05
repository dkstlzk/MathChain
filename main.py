import streamlit as st
import hashlib
import json
import time
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import plotly.graph_objects as go

# ============================================================================
# BLOCKCHAIN STRUCTURE
# ============================================================================

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


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis = Block(0, time.time(), [], "0" * 64)
        self.chain.append(genesis)
    
    def add_block(self, transactions: List[Transaction]):
        previous_hash = self.chain[-1].compute_hash()
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=transactions,
            previous_hash=previous_hash
        )
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.previous_hash != previous.compute_hash():
                return False, i
        return True, -1
    
    def get_state(self):
        state = {}
        for block in self.chain:
            for tx in block.transactions:
                state[tx.sender] = state.get(tx.sender, 1000.0) - tx.amount
                state[tx.receiver] = state.get(tx.receiver, 0.0) + tx.amount
        return state


# ============================================================================
# MERKLE TREE
# ============================================================================

def compute_merkle_root(hashes: List[str]) -> str:
    if len(hashes) == 0:
        return hashlib.sha256(b'').hexdigest()
    if len(hashes) == 1:
        return hashes[0]
    
    if len(hashes) % 2 != 0:
        hashes.append(hashes[-1])
    
    parent_hashes = []
    for i in range(0, len(hashes), 2):
        combined = hashes[i] + hashes[i+1]
        parent_hash = hashlib.sha256(combined.encode()).hexdigest()
        parent_hashes.append(parent_hash)
    
    return compute_merkle_root(parent_hashes)


def build_merkle_tree_visual(hashes: List[str]):
    """Build merkle tree and return coordinates for visualization"""
    if not hashes:
        return None, None, None
    
    # Pad to power of 2
    import math
    depth = math.ceil(math.log2(len(hashes))) if len(hashes) > 1 else 1
    padded_size = 2 ** depth
    while len(hashes) < padded_size:
        hashes.append(hashes[-1])
    
    levels = [hashes]  # Start with leaf level
    
    # Build tree bottom-up
    current_level = hashes
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            combined = current_level[i] + current_level[i+1]
            parent_hash = hashlib.sha256(combined.encode()).hexdigest()
            next_level.append(parent_hash)
        levels.append(next_level)
        current_level = next_level
    
    # Create coordinates for plotting
    x_coords = []
    y_coords = []
    labels = []
    edge_x = []
    edge_y = []
    
    total_levels = len(levels)
    
    for level_idx, level in enumerate(levels):
        y = total_levels - level_idx - 1  # Top to bottom
        num_nodes = len(level)
        spacing = 10.0 / (num_nodes + 1)
        
        for node_idx, hash_val in enumerate(level):
            x = (node_idx + 1) * spacing
            x_coords.append(x)
            y_coords.append(y)
            
            # Shorter labels
            if level_idx == 0:  # Leaf nodes
                labels.append(f"TX{node_idx}<br>{hash_val[:8]}")
            else:
                labels.append(f"{hash_val[:8]}")
            
            # Draw edges to children
            if level_idx > 0:
                parent_spacing = 10.0 / (len(levels[level_idx-1]) + 1)
                child_left_x = (node_idx * 2 + 1) * parent_spacing
                child_right_x = (node_idx * 2 + 2) * parent_spacing
                child_y = y + 1
                
                # Left edge
                edge_x.extend([x, child_left_x, None])
                edge_y.extend([y, child_y, None])
                
                # Right edge
                edge_x.extend([x, child_right_x, None])
                edge_y.extend([y, child_y, None])
    
    return (x_coords, y_coords, labels, edge_x, edge_y)


# ============================================================================
# STREAMLIT UI
# ============================================================================

st.set_page_config(page_title="MathChain", layout="wide")
st.title("🔗 MathChain")

# Initialize
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()
    for i in range(3):
        txs = [
            Transaction(f"Anshika", f"Parneeka", 10.0 + i, time.time()),
            Transaction(f"Parneeka", f"Cherry", 5.0 + i, time.time())
        ]
        st.session_state.blockchain.add_block(txs)

blockchain = st.session_state.blockchain

# ============================================================================
# PART 1: BLOCK TRAVERSAL
# ============================================================================

st.header("Block Traversal & Immutability")

col1, col2 = st.columns([3, 1])

with col1:
    for i, block in enumerate(blockchain.chain):
        block_hash = block.compute_hash()
        
        with st.expander(f"Block {block.index} | {block_hash[:16]}...", expanded=(i < 2)):
            st.text(f"Previous: {block.previous_hash[:16]}...")
            st.text(f"Current:  {block_hash[:16]}...")
            
            if block.transactions:
                st.write("**Transactions:**")
                for idx, tx in enumerate(block.transactions):
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.write(f"• {tx.sender} → {tx.receiver}: {tx.amount}")
                    with col_b:
                        if st.button(f"✏️", key=f"edit_{i}_{idx}"):
                            st.session_state[f'editing_{i}_{idx}'] = True
                    
                    # Edit mode
                    if st.session_state.get(f'editing_{i}_{idx}', False):
                        with st.form(key=f'form_{i}_{idx}'):
                            new_sender = st.text_input("Sender", tx.sender)
                            new_receiver = st.text_input("Receiver", tx.receiver)
                            new_amount = st.number_input("Amount", value=float(tx.amount))
                            
                            col_x, col_y = st.columns(2)
                            with col_x:
                                if st.form_submit_button("Save Changes"):
                                    blockchain.chain[i].transactions[idx].sender = new_sender
                                    blockchain.chain[i].transactions[idx].receiver = new_receiver
                                    blockchain.chain[i].transactions[idx].amount = new_amount
                                    st.session_state[f'editing_{i}_{idx}'] = False
                                    st.rerun()
                            with col_y:
                                if st.form_submit_button("Cancel"):
                                    st.session_state[f'editing_{i}_{idx}'] = False
                                    st.rerun()
            else:
                st.write("Genesis Block")

with col2:
    is_valid, broken = blockchain.is_chain_valid()
    
    if is_valid:
        st.success("✅ Valid Chain")
    else:
        st.error(f"❌ Broken at Block {broken}")
    
    if st.button("🔄 Reset Chain"):
        st.session_state.blockchain = Blockchain()
        for i in range(3):
            txs = [
                Transaction(f"Anshika", f"Parneeka", 10.0 + i, time.time()),
                Transaction(f"Parneeka", f"Cherry", 5.0 + i, time.time())
            ]
            st.session_state.blockchain.add_block(txs)
        st.rerun()

st.write("")
st.write("**Add New Block:**")

# Initialize pending transactions in session state
if 'pending_transactions' not in st.session_state:
    st.session_state.pending_transactions = []

# Display pending transactions
if st.session_state.pending_transactions:
    st.write("**Pending Transactions:**")
    for idx, tx in enumerate(st.session_state.pending_transactions):
        col_a, col_b = st.columns([5, 1])
        with col_a:
            st.write(f"{idx+1}. {tx['sender']} → {tx['receiver']}: {tx['amount']}")
        with col_b:
            if st.button("❌", key=f"remove_{idx}"):
                st.session_state.pending_transactions.pop(idx)
                st.rerun()
    st.write("")

# Add transaction form
c1, c2, c3, c4, c5 = st.columns([2, 2, 1, 1, 1])
with c1:
    sender = st.text_input("From", "Anshika")
with c2:
    receiver = st.text_input("To", "Parneeka")
with c3:
    amount = st.number_input("Amount", value=10.0, min_value=0.1)
with c4:
    st.write("")
    if st.button("➕ Add TX"):
        st.session_state.pending_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        st.rerun()
with c5:
    st.write("")
    if st.button("📦 Create Block", disabled=len(st.session_state.pending_transactions) == 0):
        transactions = [
            Transaction(tx['sender'], tx['receiver'], tx['amount'], time.time())
            for tx in st.session_state.pending_transactions
        ]
        blockchain.add_block(transactions)
        st.session_state.pending_transactions = []
        st.rerun()

st.divider()

# ============================================================================
# PART 2: MERKLE TREE
# ============================================================================

st.header("Merkle Tree Verification")

block_idx = st.selectbox("Select Block", range(len(blockchain.chain)), format_func=lambda x: f"Block {x}")
block = blockchain.chain[block_idx]

if not block.transactions:
    st.info("No transactions in genesis block")
else:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**Transactions:**")
        for idx, tx in enumerate(block.transactions):
            tx_hash = tx.compute_hash()
            st.write(f"**TX{idx}:** {tx.sender}→{tx.receiver}")
            st.write(f"Amount: {tx.amount}")
            st.code(tx_hash[:16]+"...", language="text")
            st.write("")
        
        merkle_root = block.get_merkle_root()
        st.success(f"**Merkle Root:**")
        st.code(merkle_root[:24]+"...", language="text")
    
    with col2:
        st.write("**Merkle Tree Structure:**")
        
        # Build tree visualization
        tx_hashes = [tx.compute_hash() for tx in block.transactions]
        result = build_merkle_tree_visual(tx_hashes)
        
        if result:
            x_coords, y_coords, labels, edge_x, edge_y = result
            
            # Create plotly figure
            fig = go.Figure()
            
            # Add edges
            fig.add_trace(go.Scatter(
                x=edge_x, y=edge_y,
                mode='lines',
                line=dict(color='#666', width=2),
                hoverinfo='none',
                showlegend=False
            ))
            
            # Add nodes
            fig.add_trace(go.Scatter(
                x=x_coords, y=y_coords,
                mode='markers+text',
                marker=dict(
                    size=40,
                    color=['#90EE90' if y == 0 else '#87CEEB' if y == max(y_coords) else '#FFD700' 
                           for y in y_coords],
                    line=dict(color='#333', width=2)
                ),
                text=labels,
                textposition="middle center",
                textfont=dict(size=8, color='#000'),
                hoverinfo='text',
                showlegend=False
            ))
            
            fig.update_layout(
                showlegend=False,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)

st.divider()

# ============================================================================
# PART 3: TURING SYSTEM
# ============================================================================

st.header("Turing System")

col1, col2 = st.columns(2)

with col1:
    st.write("**State Evolution:**")
    
    for i in range(len(blockchain.chain)):
        temp_chain = blockchain.chain[:i+1]
        state = {}
        for b in temp_chain:
            for tx in b.transactions:
                state[tx.sender] = state.get(tx.sender, 1000.0) - tx.amount
                state[tx.receiver] = state.get(tx.receiver, 0.0) + tx.amount
        
        with st.expander(f"State at Block {i}", expanded=(i == len(blockchain.chain)-1)):
            if state:
                for acc, bal in sorted(state.items()):
                    st.write(f"**{acc}:** {bal:.2f} coins")
            else:
                st.write("*Genesis State*")

with col2:
    st.write("**State Transition Function:**")
    st.code("""State[n+1] = f(State[n], Input[n])

# def state_transition(state, tx):
#     new_state = state.copy()
#     new_state[tx.sender] -= tx.amount
#     new_state[tx.receiver] += tx.amount
#     return new_state

# Properties:
# • Deterministic
# • State-based computation
# • Turing-complete
""", language="python")

st.divider()

# Summary
st.write("**Summary:**")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Blocks", len(blockchain.chain))
with c2:
    st.metric("Chain Status", "Valid ✅" if is_valid else "Invalid ❌")
with c3:
    st.metric("Active Accounts", len(blockchain.get_state()))
with c4:
    total_tx = sum(len(b.transactions) for b in blockchain.chain)
    st.metric("Total Transactions", total_tx)