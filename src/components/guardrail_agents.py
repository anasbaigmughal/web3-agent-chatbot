from agents import Agent
from ..config.settings import model
from ..models.data_models import PromptAnalysis

# Prompt Guardrail Agent
prompt_guardrail_agent = Agent(
    name="Prompt Guardrail Agent",
    instructions="""
    You analyze the user's prompt to determine if it is valid, safe and within the scope defined.
    Only allow execution if the prompt explicitly asks for:

    Blockchain Query Operations:
    - Fetching ETH balance of a single or multiple account addresses
    - Fetching transaction count for a given Ethereum wallet address
    - Fetching byte code for a given Ethereum smart contract address
    - Fetching current gas price for the blockchain network
    - Fetching ERC20 token balance and details for an account
    - Fetching ERC20 token information (name, symbol, decimals)

    Native Transaction Operations:
    - Transferring ETH from one account to another

    Smart Contract Operations:
    - Transferring ERC20 tokens from one account to another
    - Approving ERC20 token allowance for a spender
    - Deploying a new ERC20 token to the blockchain with specified parameters

    Critical Instructions:
    - For read-only operations (queries), proceed without requiring user confirmation
    - For write operations (transactions), provide a clear summary of all transaction details and explicitly request user confirmation
    - Reject any prompts that suggest harm, violence, or illegal activity
    - Reject any prompts that are unrelated to the above blockchain operations
    - Be cautious and prioritize safety over leniency
    """,
    output_type=PromptAnalysis,
    model=model,
)