# web3-construct-stability

A small CLI tool that computes a **stability score** for different Web3 constructs.  
It models three distinct architectural approaches inspired by:

- **Aztec zk circuits** (encrypted state, zero-knowledge execution)
- **Zama FHE compute pipelines** (fully homomorphic encrypted processing)
- **Soundness-first formal labs** (verified semantics and strict correctness discipline)

There are exactly two files in this repository:
- `app.py`
- `README.md`


## Purpose

This tool provides a numerical stability rating between **0.0 and 1.0** using:

- Baseline cryptographic security  
- Privacy strength  
- Scalability characteristics  
- Stability curve (latency, sync time, throughput)  
- Optional advanced features:
  - Commitments  
  - zk-proof verification  
  - FHE layers  

It helps compare architectural design choices across privacy, soundness, and performance axes.


## Installation

Requirements:
- Python 3.8+
- No external dependencies besides the Python standard library.

Put both files (`app.py` and `README.md`) into your GitHub repository.


## Usage

Run with default Aztec-style parameters:

python app.py

Try Zama-style FHE model:

python app.py --construct zama-fhe --fhe --proofs --throughput 5000

Try a soundness-first design with commitments:

python app.py --construct soundness-lab --commitments --sync 650

Output in JSON:

python app.py --construct zama-fhe --fhe --json


## Output Example

Human-readable:

🧩 Web3 Construct Stability Model
Construct     : Aztec-Style zk Circuit
Category      : zk privacy
Description   : Circuit-focused private computation with encrypted state roots.

Parameters:
  Latency (ms)     : 180.0
  Sync time (ms)   : 950.0
  Throughput load  : 3000
  Commitments      : False
  Proofs enabled   : False
  FHE enabled      : False

Stability Multiplier : 0.6121
Final Score          : 0.4678


## Notes

- All numbers are conceptual and not benchmarks.  
- This tool is intended for modeling, research, and architectural comparisons.  
- Extend it freely by adding new constructs or changing weights to reflect real designs.
