import os
from dotenv import load_dotenv
from web3 import Web3
from openai import AsyncOpenAI
from agents.models.openai_provider import OpenAIProvider
from agents import OpenAIChatCompletionsModel, RunConfig #, enable_verbose_stdout_logging
from ..utils.logging import configure_logging

# enable_verbose_stdout_logging()

PRI_KEY = os.getenv("PRI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
INFURA_URL = os.getenv("INFURA_URL")
BASE_URL = os.getenv("BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.0-flash")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY")

def connect_infura() -> Web3:
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))
    print(f"🟢 Infura Connection Successful!" if w3.is_connected() else f"🔴 Infura Connection Failed!")
    return w3

load_dotenv()
configure_logging()

w3 = connect_infura()

external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model=LLM_MODEL, openai_client=external_client)
config = RunConfig(model=model, model_provider=OpenAIProvider(openai_client=external_client))
