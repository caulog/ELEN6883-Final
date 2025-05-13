# NFT Hold Time Analysis & LLM Forecasting — BAYC Subgraph Project

This project analyzes the holding behavior of **Bored Ape Yacht Club (BAYC)** NFTs using on-chain Ethereum data, a custom subgraph built with **The Graph Protocol**, and behavioral insights generated through **LLM (ChatGPT)** integration.

It was developed as a final project for **ELEN6883** at Columbia University.

---

## Project Summary

This repo includes:
- A custom subgraph indexing **Transfer** events from the BAYC ERC-721 smart contract
- Python scripts to extract, structure, and classify NFT transfer data
- Behavior classification logic (Flipper, Collector, Swing Trader)
- Integration of **ChatGPT** prompts to generate trend predictions
- Output files including CSVs, visualizations, and LLM-driven forecasts

---

## Repo Structure

```

ELEN6883-Final/
├── bayc-holdtime/                 # Subgraph code (The Graph Protocol)
│   ├── abis/                      # ABI of the BAYC smart contract
│   ├── src/                       # AssemblyScript handler for Transfer events
│   └── subgraph.yaml              # Subgraph manifest
│
├── fetch\_bayc\_data.py            # GraphQL pagination script (Python)
├── time.py                       # LLM-generated analysis script
├── nft\_holder\_hold\_times.csv     # NFT hold times by wallet
├── holder\_classification.csv     # Wallet classifications
├── holder\_type\_summary.csv       # Aggregated wallet behavior stats
├── hold\_time\_distribution.png    # Histogram of hold durations
└── bayc\_holdtime\_data.csv        # Raw transfer data from subgraph

````

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/caulog/ELEN6883-Final.git
cd ELEN6883-Final
````

### 2. Set Up the Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Data Fetch Script

Pull transfer data from your deployed subgraph:

```bash
python3 fetch_bayc_data.py
```

### 4. Run Behavior Analysis

Calculate hold durations and classify wallet types:

```bash
python3 time.py
```

---

## Key Outputs

* **nft\_holder\_hold\_times.csv** – Every wallet's NFT hold durations
* **holder\_classification.csv** – Labeled behavior types (e.g., Flipper, Collector)
* **holder\_type\_summary.csv** – Summary stats by behavior type
* **hold\_time\_distribution.png** – Visual of transfer timing trends

---

## LLM Integration

This project used **ChatGPT (GPT-4)** to:

* Generate the wallet behavior classification pipeline (`time.py`)
* Forecast BAYC resale trends for the next 30 days
* Interpret market behavior based on structured subgraph data

Prompt used:

> *“Given a CSV of BAYC NFT transfers with timestamps, can you write a Python script that calculates hold times per wallet, classifies wallet behavior (e.g., flipper vs collector), and visualizes the hold time distribution?”*

---

## License & Attribution

Smart contract data sourced from [Etherscan](https://etherscan.io/), indexed with [The Graph](https://thegraph.com/), and analyzed via [ChatGPT](https://chat.openai.com/).

---
