# MathChain - Blockchain Visualization Application

A Streamlit-based educational blockchain implementation demonstrating core concepts including block structure, Merkle trees, and state transitions.

## Features

- **Block Traversal**: View and edit blocks to demonstrate immutability
- **Merkle Tree Visualization**: Interactive visualization of transaction verification
- **Turing System**: State-based computation demonstration
- **Transaction Management**: Create and manage transactions and blocks

## File Structure

```
MathChain/
├── src/
│   ├── __init__.py
│   ├── core/                    
│   │   ├── __init__.py
│   │   ├── transaction.py       
│   │   ├── block.py            
│   │   └── blockchain.py        
│   ├── utils/                
│   │   ├── __init__.py
│   │   └── merkle_tree.py       
│   └── ui/                   
│       ├── __init__.py
│       ├── block_traversal.py   
│       ├── merkle_visualization.py
│       └── turing_system.py   
├── app.py                    
├── requirements.txt            
└── README.md                    
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cherry-aggarwal/MathChain.git
cd MathChain
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Architecture

### Core Components

- **Transaction**: Represents a transfer between two parties
- **Block**: Contains multiple transactions and links to previous block
- **Blockchain**: Manages the chain of blocks and validates integrity

### Utilities

- **Merkle Tree**: Computes Merkle roots and generates visualization data

### UI Components

- **Block Traversal**: Allows viewing and editing blocks to demonstrate how changes break the chain
- **Merkle Visualization**: Shows how transactions are verified using Merkle trees
- **Turing System**: Demonstrates state transitions and account balances

## Key Concepts Demonstrated

1. **Immutability**: Editing a transaction breaks the chain by invalidating hashes
2. **Merkle Trees**: Efficient transaction verification
3. **State Transitions**: Deterministic computation of account balances
4. **Hash Linking**: Each block references the previous block's hash

## Development

The codebase follows clean architecture principles:

- **Separation of Concerns**: Core logic separated from UI
- **Modularity**: Each component has a single responsibility
- **Type Hints**: All functions include type annotations
- **Documentation**: Comprehensive docstrings

## License

MIT License