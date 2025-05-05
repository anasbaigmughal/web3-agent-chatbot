import requests
import time
import chainlit as cl
from agents.tool import function_tool
from web3.types import TxParams
from solcx import compile_source, install_solc
from ..config.settings import w3, ETHERSCAN_API_KEY, BSCSCAN_API_KEY, PRI_KEY

# <-------- NATIVE TRANSACTION AGENT TOOLS -------->

@function_tool
@cl.step(type="tool")
def transfer_eth(account_1: str, account_2: str, amount: float) -> str:
    """
    Transfers ETH from one account to another.
    For transfer to multiple accounts, invoke this tool separately after each LLM call, for each address when transferring to multiple addresses requested.

    Critical Instructions:
    - For write transactions involving real asset transfers or gas fees, provide a clear summary of all transaction details (e.g., asset amount, recipient, etc) and explicitly request user confirmation before executing the transaction.

    Args:
        account_1 (str): The 'from' Ethereum account wallet address.
        account_2 (str): The 'to' Ethereum account wallet address.
        amount (float): The amount of ETH to transfer.

    Returns:
        str: A formatted string containing the blockchain transaction link.

    Exception:
        If the address is invalid or error during transaction, it raises an exception and brief about the error to user.
    """
    print(f"🟢 Tool Call: transfer_eth({account_1}, {account_2}, {amount})")
    try:
        checksummed_account_1 = w3.to_checksum_address(account_1)
        checksummed_account_2 = w3.to_checksum_address(account_2)

        print(f"🟢 Gas Price: {w3.eth.gas_price}")

        # Build a transaction
        tx:TxParams = {
            "nonce": w3.eth.get_transaction_count(checksummed_account_1),
            "to": checksummed_account_2,
            "value": w3.to_wei(amount, "ether"),
            "gas": 2000000,
            "gasPrice": w3.to_wei(3, "gwei"),
            "chainId": 97
        }
        print(f"🟢 Transaction Object Built: {tx}") 

        # Sign a transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRI_KEY)
        print(f"🟢 Signed Transaction: {signed_tx}")
        
        # Send a transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"🟢 Transaction Hash: {w3.to_hex(tx_hash)}")

        return f"Blockchain Transaction Link: https://testnet.bscscan.com/tx/{w3.to_hex(tx_hash)}"
    except Exception as e:
        print(f"🔴 Error in transfer_eth: {str(e)}")
        return f"Error: {str(e)}"

# <-------- BLOCKCHAIN QUERY AGENT TOOLS -------->

@function_tool
@cl.step(type="tool")
def eth_get_balance(account: str) -> str:
    """
    Fetches the ETH balance for a given Ethereum wallet address.
    For multiple accounts, invoke this tool separately after each LLM call, for each address when multiple addresses are requested.

    Critical Instructions:
    - For read-only transactions, proceed without requiring user confirmation.

    Args:
        account (str): The Ethereum account wallet address.

    Returns:
        str: A formatted string containing the provided account address and its ETH balance.

    Exception:
        If the address is invalid or error during balance fetching, it raises an exception and brief about the error to user.
    """
    print(f"🟢 Tool Call: eth_get_balance({account})")
    try:
        checksummed_account = w3.to_checksum_address(account)
        balance = w3.eth.get_balance(checksummed_account)
        return f"Account {checksummed_account} has {w3.from_wei(balance, 'ether'):.5f} ETH."
    except Exception as e:
        print(f"🔴 Error in eth_get_balance: {str(e)}")
        return f"Error: {str(e)}"

@function_tool
@cl.step(type="tool")
def eth_get_transaction_count(account: str) -> str:
    """
    Fetches the transaction count for a given Ethereum wallet address.
    For multiple accounts, invoke this tool separately after each LLM call, for each address when multiple addresses are requested.

    Critical Instructions:
    - For read-only transactions, proceed without requiring user confirmation.

    Args:
        account (str): The Ethereum account wallet address.

    Returns:
        str: A formatted string containing the provided account address and its transaction count.

    Exception:
        If the address is invalid or error during transaction count fetching, it raises an exception and brief about the error to user.
    """
    print(f"🟢 Tool Call: eth_get_transaction_count({account})")
    try:
        checksummed_account = w3.to_checksum_address(account)
        transaction_count = w3.eth.get_transaction_count(checksummed_account)
        return f"Account {checksummed_account} has {transaction_count} transactions."
    except Exception as e:
        print(f"🔴 Error in eth_get_transaction_count: {str(e)}")
        return f"Error: {str(e)}"
    
@function_tool
@cl.step(type="tool")
def eth_get_code(account: str) -> str:
    """
    Fetches the byte code for a given Ethereum smart contract address.
    For multiple accounts, invoke this tool separately after each LLM call, for each address when multiple addresses are requested.

    Critical Instructions:
    - For read-only transactions, proceed without requiring user confirmation.

    Args:
        account (str): The Ethereum smart contract address.

    Returns:
        str: A formatted string containing the provided account address and its byte code.

    Exception:
        If the address is invalid or error during bytecode fetching, it raises an exception and brief about the error to user.
    """
    print(f"🟢 Tool Call: eth_get_code({account})")
    try:
        checksummed_account = w3.to_checksum_address(account)
        code = w3.eth.get_code(checksummed_account).hex()
        return f"Account {checksummed_account} has bytecode: {code}"
    except Exception as e:
        print(f"🔴 Error in eth_get_code: {str(e)}")
        return f"Error: {str(e)}"

@function_tool
@cl.step(type="tool")
def eth_gas_price() -> str:
    """
    Fetches the current gas price for the respective blockchain network.

    Critical Instructions:
    - For read-only transactions, proceed without requiring user confirmation.

    Returns:
        str: A formatted string containing the current gas price.

    Exception:
        If error during gas price fetching, it raises an exception and brief about the error to user.
    """
    print(f"🟢 Tool Call: eth_gas_price()")
    try:
        gas_price = w3.from_wei(w3.eth.gas_price, 'gwei')
        return f"Current gas price: {gas_price} gwei"
    except Exception as e:
        print(f"🔴 Error in eth_gas_price: {str(e)}")
        return f"Error: {str(e)}"

@function_tool
@cl.step(type="tool")
def token_get_balance(account: str, token_address: str) -> str:
    """
    Fetches the ERC20 token balance for a given account address and returns result in respective example format.
    For multiple accounts, invoke this tool separately after each LLM call, for each address when multiple addresses are requested.

    Example Format:
        Account Address: 0x123...
        Token Name: USD Coin
        Token Symbol: USDC
        Token Decimals: 6
        Token Address: 0xA0b...
        Token Balance: 1200.50 USDC

    Critical Instructions:
    - For read-only transactions, proceed without requiring user confirmation.

    Args:
        account (str): The Ethereum account wallet address.
        token_address (str): The Ethereum token address.

    Returns:
        str: A formatted string containing the provided account address, token name, token symbol, token decimals, token address, and its token balance.

    Exception:
        If the address is invalid or error during balance fetching, it raises an exception and brief about the error to user.
    """
    print(f"🟢 Tool Call: token_get_balance({account}, {token_address})")
    try:
        checksummed_account = w3.to_checksum_address(account)
        checksummed_token_address = w3.to_checksum_address(token_address)
        token_abi = get_contract_abi(checksummed_token_address)
        contract = w3.eth.contract(address=checksummed_token_address, abi=token_abi)
        balance = contract.functions.balanceOf(checksummed_account).call()
        decimals = contract.functions.decimals().call()
        token_name = contract.functions.name().call()
        token_symbol = contract.functions.symbol().call()
        return f"""
        Account Address: {checksummed_account}
        Token Name: {token_name}
        Token Symbol: {token_symbol}
        Token Decimals: {decimals}
        Token Address: {checksummed_token_address}
        Token Balance: {balance / 10**decimals}
        """
    except Exception as e:
        print(f"🔴 Error in token_get_balance: {str(e)}")
        return f"Error: {str(e)}"

@function_tool
@cl.step(type="tool")
def token_get_info(token_address: str) -> str:
    """
    Fetches the ERC20 token information (name, symbol, decimals) and returns it in the respective example format.

    Example Format:
        Token Name: USD Coin
        Token Symbol: USDC
        Token Decimals: 6
        Token Address: 0xA0b...

    Critical Instructions:
    - For read-only transactions, proceed without requiring user confirmation.

    Args:
        token_address (str): The Ethereum token contract address.

    Returns:
        str: A formatted string containing the token name, symbol, decimals, and token address.

    Exception:
        If the address is invalid or error during info fetching, it raises an exception and brief about the error to user.
    """
    print(f"🟢 Tool Call: token_get_info({token_address})")
    try:
        checksummed_token_address = w3.to_checksum_address(token_address)
        token_abi = get_contract_abi(checksummed_token_address)
        contract = w3.eth.contract(address=checksummed_token_address, abi=token_abi)
        token_name = contract.functions.name().call()
        token_symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        return f"""
        Token Name: {token_name}
        Token Symbol: {token_symbol}
        Token Decimals: {decimals}
        Token Address: {checksummed_token_address}
        """
    except Exception as e:
        print(f"🔴 Error in token_get_info: {str(e)}")
        return f"Error: {str(e)}"

# <-------- HELPER FUNCTIONS -------->

def get_contract_abi(contract_address):
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": 97,
        "module": "contract",
        "action": "getabi",
        "address": contract_address,
        "apikey": ETHERSCAN_API_KEY
    }
    print(f"🟢 Function Call: get_contract_abi({contract_address})")
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data["result"]
    except Exception as e:
        print(f"🔴 Error in get_contract_abi: {str(e)}")
        return f"Error: {str(e)}"

# <-------- SMART CONTRACT TRANSACTION AGENT TOOLS -------->

@function_tool
@cl.step(type="tool")
def transfer_token(account_1: str, account_2: str, token_address: str, amount: float) -> str:
    """
    Transfers ERC20 token from one account to another.
    For transfer to multiple accounts, invoke this tool separately after each LLM call, for each address when transferring to multiple addresses requested.

    Critical Instructions:
    - For write transactions involving real asset transfers or gas fees, provide a clear summary of all transaction details (e.g., asset amount, recipient, etc) and explicitly request user confirmation before executing the transaction.

    Args:
        account_1 (str): The 'from' Ethereum account wallet address.
        account_2 (str): The 'to' Ethereum account wallet address.
        token_address (str): The Ethereum token address.
        amount (float): The amount of token to transfer.

    Returns:
        str: A formatted string containing the blockchain transaction link.

    Exception:
        If the address is invalid or error during transaction, it raises an exception and brief about the error to user.
    """
    print(f"🟢 Tool Call: transfer_token({account_1}, {account_2}, {token_address}, {amount})")
    try:
        checksummed_account_1 = w3.to_checksum_address(account_1)
        checksummed_account_2 = w3.to_checksum_address(account_2)
        checksummed_contract_address = w3.to_checksum_address(token_address)
        contract_abi = get_contract_abi(checksummed_contract_address)
        contract = w3.eth.contract(address=checksummed_contract_address, abi=contract_abi)

        print(f"🟢 Gas Price: {w3.eth.gas_price}")

        # Step 1: Build a transaction
        tx = contract.functions.transfer(to=checksummed_account_2, value=w3.to_wei(amount, "ether")).build_transaction(
            {
                "nonce": w3.eth.get_transaction_count(checksummed_account_1),
                "gas": 2000000,
                "gasPrice": w3.to_wei(3, "gwei"),
            }
        )

        # Step 2: Sign a transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRI_KEY)

        # Step 3: Send a transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        return f"Blockchain Transaction Link: https://testnet.bscscan.com/tx/{w3.to_hex(tx_hash)}"
    except Exception as e:
        print(f"🔴 Error in transfer_token: {str(e)}")
        return f"Error: {str(e)}"

@function_tool
@cl.step(type="tool")
def approve_token(owner: str, spender: str, token_address: str, amount: float) -> str:
    """
    Approves ERC20 token allowance for a spender.
    This allows the spender to spend the specified amount of tokens on behalf of the owner.

    Critical Instructions:
    - For write transactions involving real asset transfers or gas fees, provide a clear summary of all transaction details (e.g., token, spender, allowance) and explicitly request user confirmation before executing the transaction.

    Args:
        owner (str): The Ethereum account that is granting the allowance.
        spender (str): The Ethereum account that is being approved to spend tokens.
        token_address (str): The Ethereum token address.
        amount (float): The amount of token to approve.

    Returns:
        str: A formatted string containing the blockchain transaction link.

    Exception:
        If the address is invalid or an error occurs during the transaction, it raises an exception and explains the error to the user.
    """
    print(f"🟢 Tool Call: approve_token({owner}, {spender}, {token_address}, {amount})")
    try:
        checksummed_owner = w3.to_checksum_address(owner)
        checksummed_spender = w3.to_checksum_address(spender)
        checksummed_contract_address = w3.to_checksum_address(token_address)
        contract_abi = get_contract_abi(checksummed_contract_address)
        contract = w3.eth.contract(address=checksummed_contract_address, abi=contract_abi)

        print(f"🟢 Gas Price: {w3.eth.gas_price}")

        # Step 1: Build a transaction
        tx = contract.functions.approve(checksummed_spender, w3.to_wei(amount, "ether")).build_transaction(
            {
                "nonce": w3.eth.get_transaction_count(checksummed_owner),
                "gas": 200000,
                "gasPrice": w3.to_wei(3, "gwei"),
            }
        )

        # Step 2: Sign the transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRI_KEY)

        # Step 3: Send the transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        return f"Blockchain Transaction Link: https://testnet.bscscan.com/tx/{w3.to_hex(tx_hash)}"
    except Exception as e:
        print(f"🔴 Error in approve_token: {str(e)}")
        return f"Error: {str(e)}"

@function_tool
@cl.step(type="tool")
def deploy_erc20_token(
    recipient_address: str,
    token_name: str,
    token_symbol: str,
    token_decimals: int,
    initial_supply: int
) -> str:
    """
    Deploys an ERC20 token contract on the BSC testnet with specified parameters.
    The function handles contract compilation, deployment, and verification on BscScan.

    Args:
        recipient_address (str): The address that will receive the initial token supply.
        token_name (str): The name of the token (e.g., "My Token").
        token_symbol (str): The symbol of the token (e.g., "MTK").
        token_decimals (int): Number of decimal places for token amounts (typically 18).
        initial_supply (int): Initial token supply in base units (will be multiplied by 10^decimals).

    Returns:
        str: A formatted string containing:
            - Contract deployment status
            - Contract address
            - Transaction link
            - Verification status

    Raises:
        Exception: If any step in the deployment process fails, with detailed error message.
    """
    print(f"🟢 Tool Call: deploy_erc20_token({recipient_address}, {token_name}, {token_symbol}, {token_decimals}, {initial_supply})")
    
    try:
        # Install and verify Solidity compiler
        install_solc("0.8.29")
        
        # Convert and validate addresses
        checksummed_recipient_address = w3.to_checksum_address(recipient_address)
        initial_supply = int(initial_supply * 10 ** token_decimals)

        # Generate ERC20 contract source code with optimized gas usage
        erc20_source = f"""
        // SPDX-License-Identifier: MIT
        pragma solidity 0.8.29;

        contract {token_name.replace(" ", "")}Token {{
            string public constant name = "{token_name}";
            string public constant symbol = "{token_symbol}";
            uint8 public constant decimals = {token_decimals};
            uint256 public constant totalSupply = {initial_supply};
            
            mapping(address => uint256) private _balances;
            mapping(address => mapping(address => uint256)) private _allowances;

            event Transfer(address indexed from, address indexed to, uint256 value);
            event Approval(address indexed owner, address indexed spender, uint256 value);

            constructor() {{
                _balances[msg.sender] = totalSupply;
                emit Transfer(address(0), msg.sender, totalSupply);
            }}

            function balanceOf(address account) public view returns (uint256) {{
                return _balances[account];
            }}

            function allowance(address owner, address spender) public view returns (uint256) {{
                return _allowances[owner][spender];
            }}

            function transfer(address to, uint256 amount) public returns (bool) {{
                require(to != address(0), "ERC20: transfer to zero address");
                require(_balances[msg.sender] >= amount, "ERC20: insufficient balance");
                
                _balances[msg.sender] -= amount;
                _balances[to] += amount;
                emit Transfer(msg.sender, to, amount);
                return true;
            }}

            function approve(address spender, uint256 amount) public returns (bool) {{
                require(spender != address(0), "ERC20: approve to zero address");
                
                _allowances[msg.sender][spender] = amount;
                emit Approval(msg.sender, spender, amount);
                return true;
            }}

            function transferFrom(address from, address to, uint256 amount) public returns (bool) {{
                require(to != address(0), "ERC20: transfer to zero address");
                require(_balances[from] >= amount, "ERC20: insufficient balance");
                require(_allowances[from][msg.sender] >= amount, "ERC20: insufficient allowance");
                
                _balances[from] -= amount;
                _balances[to] += amount;
                _allowances[from][msg.sender] -= amount;
                emit Transfer(from, to, amount);
                return true;
            }}
        }}
        """

        # Compile contract with optimization
        compiled = compile_source(
            erc20_source,
            output_values=["abi", "bin", "metadata"],
            solc_version="0.8.29",
            optimize=True,
            optimize_runs=200
        )
        contract_id, contract_interface = compiled.popitem()
        abi = contract_interface["abi"]
        bytecode = contract_interface["bin"]

        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx = contract.constructor().build_transaction({
            "from": checksummed_recipient_address,
            "nonce": w3.eth.get_transaction_count(checksummed_recipient_address),
            "gasPrice": w3.to_wei(3, "gwei"),
            "gas": 3000000,
            "chainId": 97
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRI_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print(f"🟢 Contract deployment tx hash: {w3.to_hex(tx_hash)}")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt["contractAddress"]

        print("🟢🔴🟢🔴🟢🔴🟢🔴🟢🔴 Waiting for 10 seconds before verification...")
        time.sleep(10) # wait before verification

        # Verify contract on BscScan
        verification_url = "https://api-testnet.bscscan.com/api"
        params = {
            "module": "contract",
            "action": "verifysourcecode",
            "apikey": BSCSCAN_API_KEY,
            "contractaddress": contract_address,
            "sourceCode": erc20_source,
            "codeformat": "solidity-single-file",
            "contractname": f"{token_name.replace(' ', '')}Token",
            "compilerversion": "v0.8.29+commit.ab55807c",
            "optimizationUsed": 1,
            "runs": 200,
            "constructorArguements": ""
        }
        verification_response = requests.post(verification_url, data=params)

        print("🟢 Verification API response:", verification_response.json())
        result_json = verification_response.json()
        if result_json.get("status") == "1":
            verification_status = f"✅ Verification Submitted. GUID: {result_json['result']}"
        else:
            verification_status = f"🔴 Verification Failed: {result_json.get('result')}"

        return f"""
        ✅ Token Deployed Successfully!
        🔗 Contract Address: {contract_address}
        🔗 Explorer Tx: https://testnet.bscscan.com/tx/{w3.to_hex(tx_hash)}
        {verification_status}
        """

    except Exception as e:
        print(f"🔴 Error in deploy_erc20_token: {e}")
        return f"Error: {e}"


# <-------- EXAMPLE PROMPTS -------->
# yra ikk kum kr tu transfer kr dy 1.5  token of token address 0xEce5E455A8191E42a2b8162124248cb20Ceea76f mery apny account 0xC9654530E08907D0Ea73E17fa8EF8964129A3dB7 se meri sangi k account m 0xDA616Cf8f1114dcC4acfb76Efc9b23DCF2DeB54a
