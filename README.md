# Web3 Agent Chatbot 🤖


![AI meets Blockchain](./AI%20meets%20Blockchain.png)
*AI meets Blockchain*

---

# Power of Agentic AI & Blockchain

A powerful AI-powered chatbot designed to interact with Web3 and blockchain technologies. This chatbot provides a conversational interface for users to interact with blockchain networks, manage wallets, and execute smart contracts.

> **Note:** This project uses the **Binance Smart Chain Testnet** for all blockchain operations. Make sure your wallet and provider URLs are configured for BSC Testnet.

## 👨‍💻 Author & Developer

**Muhammad Anas Baig**  
[![GitHub](https://img.shields.io/badge/GitHub-anasbaigmughal-blue)](https://github.com/anasbaigmughal)  
AI & Blockchain Developer


---

![Web3 Agent Chatbot Architecture](./Web3%20Agent%20Chatbot%20Architecture.png)
*Web3 Agent Chatbot - High-Level Architecture*

---

## ✨ Features

### Core Features
- Interactive chat interface for Web3 operations
- Secure wallet management and integration
- Smart contract interaction and deployment
- Multi-chain support (currently configured for BSC Testnet)
- Real-time blockchain data querying
- Transaction execution and monitoring

### Advanced Features
- AI-powered natural language processing
- Context-aware responses
- Chat history management
- Error handling and recovery
- Streamed responses for better UX
- Tool integration for complex operations

---

![Web3 Agent Chatbot Flow](./Web3%20Agent%20Chatbot%20Flow.png)
*Web3 Agent Chatbot - Detailed Flow Diagram*

---

## 🛠️ Technologies Used

- **Python** - Core programming language
- **Chainlit** - UI framework for chat interface
- **Web3.py** - Binance Smart Chain (BSC) Testnet and blockchain interaction
- **LLM Integration** - Flexible LLM support (currently configured for Google Gemini)
- **OpenAI Agents** - Multi-agent workflow framework
- **Logfire** - Logging and monitoring
- **Py-Solc-X** - Smart contract compilation

## 🔄 LLM Integration

The project is designed to work with any Large Language Model (LLM) provider. Currently, it's configured to use Google's Gemini model, but it can be easily adapted to work with other LLMs like:
- OpenAI's GPT models
- Anthropic's Claude
- Meta's Llama
- Other compatible LLM providers

To switch LLM providers, simply update the configuration in the environment variables and adjust the model initialization in the settings.

## 📊 Logging & Monitoring

The project uses Logfire with Pydantic models for comprehensive logging and monitoring:
- Structured logging with Pydantic models
- Real-time monitoring of operations
- Detailed error tracking
- Performance metrics
- Transaction history
- User interaction logs

## 🚀 Available Tasks & Capabilities

### Native Token Operations
- **ETH/BNB Transfers**: Send native tokens between wallets
- **Balance Checks**: Query native token balances for any address
- **Transaction History**: View transaction counts for addresses
- **Gas Price Monitoring**: Check current network gas prices

### ERC20 Token Operations
- **Token Deployment**: Deploy new ERC20 tokens with custom parameters
  - Set token name, symbol, and decimals
  - Configure initial supply
  - Assign initial token holder
- **Token Transfers**: Send ERC20 tokens between wallets
- **Token Approvals**: Approve token spending for DEXs and other contracts
- **Token Balance Checks**: Query token balances for any address
- **Token Information**: Get detailed token information including:
  - Token name and symbol
  - Decimal places
  - Contract address
  - Total supply

### Smart Contract Operations
- **Contract Code Retrieval**: Fetch bytecode of deployed contracts
- **Contract Interaction**: Interact with deployed smart contracts
- **Contract Verification**: Verify deployed contracts on block explorers

### Blockchain Query Operations
- **Address Information**: Get comprehensive information about any blockchain address
- **Transaction Details**: View detailed information about transactions
- **Network Status**: Check current network conditions and parameters

### Security Features
- **Transaction Confirmation**: All write operations require explicit user confirmation
- **Input Validation**: Automatic validation of addresses and parameters
- **Error Handling**: Comprehensive error handling and user feedback
- **Guardrails**: Built-in safety measures to prevent unintended operations

## 💬 Example Prompts

### Native Token (ETH/BNB) Transfer
```
"Send 0.1 ETH from 0x123... to 0x456..."
"Transfer 0.5 BNB to address 0x789..."
"Move 1 ETH from my wallet to 0xabc..."
```

### ERC20 Token Transfer
```
"Send 100 USDT to 0x123..."
"Transfer 50 DAI to address 0x456..."
"Move 1000 BUSD from my wallet to 0x789..."
```

### ERC20 Token Approval
```
"Approve 1000 USDT for PancakeSwap"
"Allow Uniswap to spend 500 DAI"
"Set approval for 2000 BUSD to 0x123..."
```

### ERC20 Token Deployment
```
"Deploy a new token called MyToken with symbol MTK, 18 decimals, and initial supply of 1,000,000"
"Create a new ERC20 token named TestCoin (TST) with 6 decimals and 100,000 initial supply"
"Launch a token called GameToken (GAME) with 18 decimals and 1,000,000,000 initial supply"
```

### Balance and Information Queries
```
"What's the balance of 0x123...?"
"How much USDT does 0x456... have?"
"Show me the details of token at 0x789..."
"What's the current gas price?"
```

### Smart Contract Operations
```
"Show me the code of contract at 0x123..."
"Verify the contract at 0x456... on BscScan"
"Get the transaction count for 0x789..."
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- UV package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/anasbaigmughal/web3-agent-chatbot.git
   cd ai_x_blockchain
   ```

2. **Create and activate virtual environment**
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   uv pip install -e .
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory with the following variables (use BSC Testnet URLs/keys):
   ```env
   OPENAI_API_KEY=your_openai_api_key
   WEB3_PROVIDER_URL=your_web3_provider_url
   WALLET_PRIVATE_KEY=your_wallet_private_key
   ```

5. **Run the application**
   ```bash
   chainlit run main.py
   ```

## 📁 Project Structure

```
web3-agent-chatbot/
├── src/
│   ├── handlers/         # Chatbot interaction handlers
│   ├── models/          # Data models and schemas
│   ├── config/          # Configuration files
│   ├── utils/           # Utility functions
│   ├── components/      # UI components
│   └── __init__.py
├── .chainlit/          # Chainlit configuration
├── .env                # Environment variables
├── chainlit.md         # Welcome screen content
├── main.py            # Application entry point
├── pyproject.toml     # Project dependencies
└── README.md          # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
- PIAIC team members for their assistance
- OpenAI for their powerful language models
- Chainlit team for the amazing UI framework
- Web3.py community for blockchain integration tools
