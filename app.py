#!/usr/bin/env python3
import argparse
import json
import math
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Web3Construct:
    key: str
    name: str
    category: str
    baseline_security: float     # 0–1
    privacy_factor: float        # 0–1
    scalability_factor: float    # 0–1
    description: str


CONSTRUCTS: Dict[str, Web3Construct] = {
    "aztec-zk": Web3Construct(
        key="aztec-zk",
        name="Aztec-Style zk Circuit",
        category="zk privacy",
        baseline_security=0.81,
        privacy_factor=0.94,
        scalability_factor=0.58,
        description="Circuit-focused private computation with encrypted state roots.",
    ),
    "zama-fhe": Web3Construct(
        key="zama-fhe",
        name="Zama FHE Compute Layer",
        category="fhe compute",
        baseline_security=0.89,
        privacy_factor=0.87,
        scalability_factor=0.42,
        description="Fully homomorphic encrypted computation woven into Web3 data models.",
    ),
    "soundness-lab": Web3Construct(
        key="soundness-lab",
        name="Soundness-Driven Formal Model",
        category="formal verification",
        baseline_security=0.97,
        privacy_factor=0.51,
        scalability_factor=0.72,
        description="Extremely rigorous models built from formal proofs and verified semantics.",
    ),
}


def stability_curve(latency_ms: float, sync_ms: float, throughput: int) -> float:
    """
    Returns a stability multiplier based on:
    - RPC latency
    - sync cycle time
    - throughput load
    """
    latency_term = math.exp(-latency_ms / 1500)
    sync_term = math.exp(-sync_ms / 800)
    throughput_term = 1 / (1 + throughput / 10000)

    return max(0.0, min(1.0, (latency_term + sync_term + throughput_term) / 3))


def compute_score(
    construct: Web3Construct,
    latency_ms: float,
    sync_ms: float,
    throughput: int,
    enable_commitments: bool,
    enable_proofs: bool,
    enable_fhe: bool,
) -> Dict[str, Any]:

    base = (
        construct.baseline_security * 0.40
        + construct.privacy_factor * 0.30
        + construct.scalability_factor * 0.30
    )

    if enable_commitments:
        base += 0.04
    if enable_proofs:
        base += 0.07
    if enable_fhe:
        base += 0.05

    stability = stability_curve(latency_ms, sync_ms, throughput)
    final = max(0.0, min(1.0, base * stability))

    return {
        "construct": construct.key,
        "name": construct.name,
        "category": construct.category,
        "description": construct.description,
        "latencyMs": latency_ms,
        "syncMs": sync_ms,
        "throughput": throughput,
        "enableCommitments": enable_commitments,
        "enableProofs": enable_proofs,
        "enableFhe": enable_fhe,
        "stabilityMultiplier": round(stability, 4),
        "finalScore": round(final, 4),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute Web3 construct stability score based on privacy/soundness models."
    )
    parser.add_argument("--construct", choices=list(CONSTRUCTS.keys()), default="aztec-zk")
    parser.add_argument("--latency", type=float, default=180.0, help="RPC latency in ms.")
    parser.add_argument("--sync", type=float, default=950.0, help="State sync time in ms.")
    parser.add_argument("--throughput", type=int, default=3000, help="System throughput load.")
    parser.add_argument("--commitments", action="store_true", help="Enable commitment schemes.")
    parser.add_argument("--proofs", action="store_true", help="Enable zk-proof verification.")
    parser.add_argument("--fhe", action="store_true", help="Enable FHE layers.")
    parser.add_argument("--json", action="store_true", help="Output as JSON.")
    return parser.parse_args()


def print_human(d: Dict[str, Any]):
    print("🧩 Web3 Construct Stability Model")
    print(f"Construct     : {d['name']} ({d['construct']})")
    print(f"Category      : {d['category']}")
    print(f"Description   : {d['description']}")
    print("")
    print("Parameters:")
    print(f"  Latency (ms)     : {d['latencyMs']}")
    print(f"  Sync time (ms)   : {d['syncMs']}")
    print(f"  Throughput load  : {d['throughput']}")
    print(f"  Commitments      : {d['enableCommitments']}")
    print(f"  Proofs enabled   : {d['enableProofs']}")
    print(f"  FHE enabled      : {d['enableFhe']}")
    print("")
    print(f"Stability Multiplier : {d['stabilityMultiplier']:.4f}")
    print(f"Final Score          : {d['finalScore']:.4f}")


def main():
    args = parse_args()
    construct = CONSTRUCTS[args.construct]

    result = compute_score(
        construct,
        latency_ms=args.latency,
        sync_ms=args.sync,
        throughput=args.throughput,
        enable_commitments=args.commitments,
        enable_proofs=args.proofs,
        enable_fhe=args.fhe,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_human(result)


if __name__ == "__main__":
    main()
