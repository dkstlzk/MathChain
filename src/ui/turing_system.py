import streamlit as st

def render_turing_system(blockchain):
    st.header("Turing System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        _render_state_evolution(blockchain)
   
def _render_state_evolution(blockchain):
    st.write("**State Evolution (Unique States)**:")
    
    state_counts = {}  
    
    for i in range(len(blockchain.chain)):
        temp_chain = blockchain.chain[:i+1]
        state = _calculate_state(temp_chain)

        state_key = tuple(sorted(state.items())) if state else None

        if state_key in state_counts:
            state_counts[state_key].append(i)
        else:
            state_counts[state_key] = [i]
    
    for state_key, blocks in state_counts.items():
        block_list = ", ".join(map(str, blocks))
        with st.expander(f"State appears in {len(blocks)} block(s): {block_list}",
                         expanded=True):
            if state_key:
                for acc, bal in state_key:
                    st.write(f"**{acc}:** {bal:.2f} coins")
            else:
                st.write("*Genesis State*")


def _calculate_state(chain):
    state = {}
    for block in chain:
        for tx in block.transactions:
            state[tx.sender] = state.get(tx.sender, 1000.0) - tx.amount
            state[tx.receiver] = state.get(tx.receiver, 0.0) + tx.amount
    return state

def render_summary(blockchain):
    st.divider()
    st.write("**Summary:**")
    
    is_valid, _ = blockchain.is_chain_valid()
    total_tx = sum(len(b.transactions) for b in blockchain.chain)
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("Total Blocks", len(blockchain.chain))
    with c2:
        st.metric("Chain Status", "Valid ✅" if is_valid else "Invalid ❌")
    with c3:
        st.metric("Active Accounts", len(blockchain.get_state()))
    with c4:
        st.metric("Total Transactions", total_tx)