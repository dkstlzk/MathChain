import streamlit as st
import time
from src.core.transaction import Transaction


def render_block_traversal(blockchain):

    st.header("Block Traversal & Immutability")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        _render_blocks(blockchain)
    
    with col2:
        _render_validation_status(blockchain)
    
    st.write("")
    _render_add_block_section(blockchain)


def _render_blocks(blockchain):
    for i, block in enumerate(blockchain.chain):
        block_hash = block.compute_hash()
        
        with st.expander(f"Block {block.index} | {block_hash[:16]}...", expanded=(i < 2)):
            st.text(f"Previous: {block.previous_hash[:16]}...")
            st.text(f"Current:  {block_hash[:16]}...")
            
            if block.transactions:
                st.write("**Transactions:**")
                for idx, tx in enumerate(block.transactions):
                    _render_transaction(blockchain, i, idx, tx)
            else:
                st.write("Genesis Block")


def _render_transaction(blockchain, block_idx, tx_idx, tx):
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.write(f"• {tx.sender} → {tx.receiver}: {tx.amount}")
    with col_b:
        if st.button(f"✏️", key=f"edit_{block_idx}_{tx_idx}"):
            st.session_state[f'editing_{block_idx}_{tx_idx}'] = True
    
    # Edit mode
    if st.session_state.get(f'editing_{block_idx}_{tx_idx}', False):
        _render_edit_form(blockchain, block_idx, tx_idx, tx)


def _render_edit_form(blockchain, block_idx, tx_idx, tx):
    with st.form(key=f'form_{block_idx}_{tx_idx}'):
        new_sender = st.text_input("Sender", tx.sender)
        new_receiver = st.text_input("Receiver", tx.receiver)
        new_amount = st.number_input("Amount", value=float(tx.amount))
        
        col_x, col_y = st.columns(2)
        with col_x:
            if st.form_submit_button("Save Changes"):
                blockchain.chain[block_idx].transactions[tx_idx].sender = new_sender
                blockchain.chain[block_idx].transactions[tx_idx].receiver = new_receiver
                blockchain.chain[block_idx].transactions[tx_idx].amount = new_amount
                st.session_state[f'editing_{block_idx}_{tx_idx}'] = False
                st.rerun()
        with col_y:
            if st.form_submit_button("Cancel"):
                st.session_state[f'editing_{block_idx}_{tx_idx}'] = False
                st.rerun()


def _render_validation_status(blockchain):
    is_valid, broken = blockchain.is_chain_valid()
    
    if is_valid:
        st.success("✅ Valid Chain")
    else:
        st.error(f"❌ Broken at Block {broken}")
    
    if st.button("🔄 Reset Chain"):
        _reset_blockchain()


def _reset_blockchain():
    from src.core.blockchain import Blockchain
    
    st.session_state.blockchain = Blockchain()
    for i in range(3):
        txs = [
            Transaction(f"Anshika", f"Parneeka", 10.0 + i, time.time()),
            Transaction(f"Parneeka", f"Cherry", 5.0 + i, time.time())
        ]
        st.session_state.blockchain.add_block(txs)
    st.rerun()


def _render_add_block_section(blockchain):
    st.write("**Add New Block:**")
    
    if 'pending_transactions' not in st.session_state:
        st.session_state.pending_transactions = []
    
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
    
    _render_transaction_form(blockchain)


def _render_transaction_form(blockchain):
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