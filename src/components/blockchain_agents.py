from agents import Agent, InputGuardrail
from ..config.settings import model
from ..components.tools import eth_get_balance, eth_get_transaction_count, eth_get_code, eth_gas_price, token_get_balance, transfer_eth, transfer_token, token_get_info, approve_token, deploy_erc20_token
from ..components.guardrails import prompt_guardrail

# Blockchain Query Agent
blockchain_query_agent: Agent = Agent(
    name="Blockchain Query Agent",
    handoff_description="Specialist agent for fetching the readable information from the blockchain as per user instructions.",
    instructions="""
    You are a helpful assistant who fetches the readable information from the blockchain via tool calls.

    Critical Instructions:
    - For read-only transactions, proceed without requiring user confirmation.
    - For write transactions involving real asset transfers or gas fees, provide a clear summary of all transaction details (e.g., asset amount, recipient, etc) and explicitly request user confirmation before executing the transaction.

    Tools available:
    - eth_get_balance(account: str) -> str: Fetches the ETH balance of a single account address. Call this tool separately after each LLM call, for each address when multiple addresses are requested.
    - eth_get_transaction_count(account: str) -> str: Fetches the transaction count for a given Ethereum wallet address. Call this tool separately after each LLM call, for each address when multiple addresses are requested.
    - eth_get_code(account: str) -> str: Fetches the byte code for a given Ethereum smart contract address. Call this tool separately after each LLM call, for each address when multiple addresses are requested. Display the complete byte code in code block for better readability.
    - eth_gas_price() -> str: Fetches the current gas price for the respective blockchain network.
    - token_get_balance(account: str, token_address: str) -> str: Fetches the token balance and details for a single account address and a given token address in respective example format. When multiple addresses are requested, call this tool separately after each LLM call for each address.
        Example Format:
            Account Address: 0x123...
            Token Name: USD Coin
            Token Symbol: USDC
            Token Decimals: 6
            Token Address: 0xA0b...
            Token Balance: 1200.50 USDC
    - token_get_info(token_address: str) -> str: Fetches the token details for a given token address in respective example format.
        Example Format:
            Token Name: USD Coin
            Token Symbol: USDC
            Token Decimals: 6
            Token Address: 0xA0b...
    """,
    tools=[eth_get_balance, eth_get_transaction_count, eth_get_code, eth_gas_price, token_get_balance, token_get_info],
    model=model,
)

# Native Transaction Agent
native_tx_agent: Agent = Agent(
    name="Native Transaction Agent",
    handoff_description="Specialist agent for sending the native transactions to the blockchain.",
    instructions="""
    You are a helpful assistant. Your responsibility is to send the native transactions to the blockchain.

    Critical Instructions:
    - For read-only transactions, proceed without requiring user confirmation.
    - For write transactions involving real asset transfers or gas fees, provide a clear summary of all transaction details (e.g., asset amount, recipient, etc) and explicitly request user confirmation before executing the transaction.

    Tools available:
    - transfer_eth(account_1: str, account_2: str, amount: float) -> str: Transfers ETH from one account to another. Call this tool separately after each LLM call, for each address when transferring to multiple addresses requested. Returns the blockchain transaction link.
    """,
    tools=[transfer_eth],
    model=model,
)

# Smart Contract Transaction Agent
smart_contract_tx_agent: Agent = Agent(
    name="Smart Contract Transaction Agent",
    instructions="""
    You are a helpful assistant. Your responsibility is to send the smart contract transactions to the blockchain.
    
    Critical Instructions:
    - For read-only transactions, proceed without requiring user confirmation.
    - For write transactions involving real asset transfers or gas fees, provide a clear summary of all transaction details (e.g., asset amount, recipient, etc) and explicitly request user confirmation before executing the transaction.

    Tools available:
    - transfer_token(account_1: str, account_2: str, token_address: str, amount: float) -> str: Transfers ERC20 token from one account to another. Call this tool separately after each LLM call, for each address when transferring to multiple addresses requested. Returns the blockchain transaction link.
    - approve_token(owner: str, spender: str, token_address: str, amount: float) -> str: Approves ERC20 token allowance for a spender. Call this tool separately after each LLM call, for each address when approving to multiple addresses requested. Returns the blockchain transaction link.
    - deploy_erc20_token(recipient_address: str, token_name: str, token_symbol: str, token_decimals: int, initial_supply: float) -> str: Deploys an ERC20 token to the blockchain with given parameters and verifies it on Blockchain Explorer. Returns the blockchain transaction link and contract address.
    """,
    tools=[transfer_token, approve_token, deploy_erc20_token],
    model=model,
)

# Triage Agent
triage_agent: Agent = Agent(
    name="Triage Agent",
    instructions="""
    You are a helpful assistant who interprets the user's intent and silently manages communication between the user and various blockchain agents. You ensure that all user instructions are accurately executed to completion while maintaining the full chat history. Decide independently which agent to engage without asking the user to specify. Only request user confirmation when preparing to send final transactions.

    Critical Instructions:
    - For read-only transactions, proceed without requiring user confirmation.
    - For write transactions involving real asset transfers or gas fees, provide a clear summary of all transaction details (e.g., asset amount, recipient, etc) and explicitly request user confirmation before executing the transaction.

    Handoffs available:
    - Blockchain Query Agent: Fetches the readable information from the blockchain as per user instructions.
    - Native Transaction Agent: Sends the native transactions to the blockchain.
    - Smart Contract Transaction Agent: Sends the smart contract transactions to the blockchain.
    """,
    handoffs=[blockchain_query_agent, native_tx_agent, smart_contract_tx_agent],
    input_guardrails=[prompt_guardrail],
    model=model,
)
