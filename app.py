import streamlit as st
import time

from src.core.blockchain import Blockchain
from src.core.transaction import Transaction
from src.ui.block_traversal import render_block_traversal
from src.ui.merkle_visualization import render_merkle_tree
from src.ui.turing_system import render_turing_system, render_summary


def initialize_blockchain():
    if 'blockchain' not in st.session_state:
        st.session_state.blockchain = Blockchain()
        
        # Add sample blocks
        for i in range(3):
            txs = [
                Transaction(f"Anshika", f"Parneeka", 10.0 + i, time.time()),
                Transaction(f"Parneeka", f"Cherry", 5.0 + i, time.time())
            ]
            st.session_state.blockchain.add_block(txs)


def main():
    # Page configuration
    st.set_page_config(page_title="MathChain", layout="wide")
    st.title("🔗 MathChain")
    
    # Initialize blockchain
    initialize_blockchain()
    blockchain = st.session_state.blockchain
    
    # Render UI sections
    render_block_traversal(blockchain)
    st.divider()
    
    render_merkle_tree(blockchain)
    st.divider()
    
    render_turing_system(blockchain)
    render_summary(blockchain)


if __name__ == "__main__":
    main()