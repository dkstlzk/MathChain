import streamlit as st
import plotly.graph_objects as go
from src.utils.merkle_tree import build_merkle_tree_visual


def render_merkle_tree(blockchain):

    st.header("Merkle Tree Verification")
    
    block_idx = st.selectbox(
        "Select Block", 
        range(len(blockchain.chain)), 
        format_func=lambda x: f"Block {x}"
    )
    block = blockchain.chain[block_idx]
    
    if not block.transactions:
        st.info("No transactions in genesis block")
    else:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            _render_transaction_list(block)
        
        with col2:
            _render_tree_visualization(block)


def _render_transaction_list(block):
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


def _render_tree_visualization(block):
    st.write("**Merkle Tree Structure:**")
    
    # Build tree visualization
    tx_hashes = [tx.compute_hash() for tx in block.transactions]
    result = build_merkle_tree_visual(tx_hashes)
    
    if result:
        x_coords, y_coords, labels, edge_x, edge_y = result
        fig = _create_tree_figure(x_coords, y_coords, labels, edge_x, edge_y)
        st.plotly_chart(fig, use_container_width=True)


def _create_tree_figure(x_coords, y_coords, labels, edge_x, edge_y):
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(color='#666', width=2),
        hoverinfo='none',
        showlegend=False
    ))
    
    # Add nodes with color coding
    node_colors = [
        '#90EE90' if y == 0 else '#87CEEB' if y == max(y_coords) else '#FFD700' 
        for y in y_coords
    ]
    
    fig.add_trace(go.Scatter(
        x=x_coords, y=y_coords,
        mode='markers+text',
        marker=dict(
            size=40,
            color=node_colors,
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
    
    return fig