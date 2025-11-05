import hashlib
import math
from typing import List, Tuple, Optional


def compute_merkle_root(hashes: List[str]) -> str:

    if len(hashes) == 0:
        return hashlib.sha256(b'').hexdigest()
    if len(hashes) == 1:
        return hashes[0]
    
    # Duplicate last hash if odd number of hashes
    if len(hashes) % 2 != 0:
        hashes.append(hashes[-1])
    
    parent_hashes = []
    for i in range(0, len(hashes), 2):
        combined = hashes[i] + hashes[i+1]
        parent_hash = hashlib.sha256(combined.encode()).hexdigest()
        parent_hashes.append(parent_hash)
    
    return compute_merkle_root(parent_hashes)


def build_merkle_tree_visual(hashes: List[str]) -> Optional[Tuple]:

    if not hashes:
        return None
    
    # Pad to power of 2
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