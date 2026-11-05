# RaceTrack: Blockchain-Based Carbon Emissions Tracking in Formula 1

RaceTrack is a blockchain-based carbon accounting framework designed to enable transparent, verifiable, and tamper-resistant tracking of carbon emissions across the Formula 1 ecosystem. It integrates blockchain, smart contracts, and machine learning to monitor emissions from logistics, fuel consumption, and manufacturing activities.

The system uses an Ethereum-compatible blockchain to maintain immutable emission records, automated smart contract verification, and token-based sustainability incentives.

## Key Features

- **Emission Analysis:** Machine learning-based emission estimation, data preprocessing, and anomaly detection using Python.
- **Blockchain Integration:** Immutable, timestamped carbon emission records on the Ethereum Sepolia testnet.
- **Smart Contract Verification:** Oracle-authenticated emission submissions and automated on-chain validation.
- **Carbon Rewards:** ERC-20-based RACE tokens minted upon successful emission verification.
- **Python Oracle:** Secure integration between off-chain ML outputs and blockchain smart contracts.
- **Interactive Dashboard:** Real-time visualization of team-wise emissions, transaction metrics, and token rewards.

## Tech Stack

| Component | Technologies |
|---|---|
| Programming Languages | Python, Solidity |
| Blockchain | Ethereum Sepolia Testnet |
| Smart Contracts | Solidity, OpenZeppelin |
| Development Tools | Remix IDE, MetaMask |
| Blockchain Integration | Web3.py |
| Machine Learning | Pandas, Scikit-learn |
| Dashboard | Streamlit, Plotly |
| Token Standard | ERC-20 |

## System Architecture

1. **ML Emission Analysis:** Processes Formula 1 logistics or synthetic datasets to estimate emissions and generate team-wise summaries.
2. **Smart Contracts:** Three Solidity contracts manage verification, emission records, and carbon rewards:
   - `OracleVerifier.sol`: Authenticates authorized oracle submissions.
   - `EmissionRegistry.sol`: Stores verified emission records and manages verification events.
   - `CarbonToken.sol`: Implements the ERC-20 RACE reward token.
3. **Python Oracle:** Hashes and signs emission data, submits transactions through Web3.py, and collects blockchain performance metrics.
4. **Streamlit Dashboard:** Displays emission summaries, transaction performance, and RACE token rewards.

## Workflow

1. Prepare datasets and train the ML emission analysis model.
2. Compile smart contracts using Remix IDE.
3. Deploy contracts to the Ethereum Sepolia testnet using MetaMask.
4. Configure oracle credentials and contract addresses.
5. Submit signed emission records through the Python oracle.
6. Verify submissions using smart contracts.
7. Mint RACE tokens for verified records.
8. Visualize emissions and blockchain metrics through the dashboard.

## Evaluation Metrics

The framework evaluates blockchain performance using:

- Gas consumption per transaction
- Estimated transaction cost in ETH
- Transaction confirmation latency
- Transaction throughput (transactions per minute)
- Total on-chain emission records
- Total RACE tokens minted

## Security Features

- Oracle-signed data authentication
- Immutable blockchain records
- Restricted token minting
- Data provenance through cryptographic hashes
- Ethereum Sepolia testnet deployment

## Future Enhancements

- Real-time IoT-based emission data integration
- Improved ML model calibration using verified sustainability datasets
- Layer-2 integration for reduced transaction costs
- DAO-based governance for multi-stakeholder participation
- Extension to aviation, logistics, and manufacturing industries

## Objective

RaceTrack aims to establish a transparent and auditable digital infrastructure for carbon accountability, supporting Formula 1's Net Zero Carbon 2030 commitment through blockchain technology and intelligent automation.
