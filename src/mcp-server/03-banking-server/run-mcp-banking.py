import os

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv
from openai import AsyncOpenAI

from data_functions import submit_payment, get_account_balance

load_dotenv()


def _build_chat_client() -> OpenAIChatClient:
    token = None
    endpoint = None
    model_name = None

    if os.environ.get("GITHUB_TOKEN") is not None:
        token = os.environ["GITHUB_TOKEN"]
        endpoint = "https://models.github.ai/inference"
        model_name = "openai/gpt-5-nano"
        print("Using GitHub Token for authentication")
    elif os.environ.get("AZURE_OPENAI_API_KEY") is not None:
        token = os.environ["AZURE_OPENAI_API_KEY"]
        endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        model_name = os.environ["COMPLETION_DEPLOYMENT_NAME"]
        print("Using Azure OpenAI Token for authentication")
    else:
        raise RuntimeError("No GitHub or Azure OpenAI credentials found in environment.")

    async_client = AsyncOpenAI(base_url=endpoint, api_key=token)

    return OpenAIChatClient(
        model_id=model_name,
        api_key=token,
        async_client=async_client,
    )


def build_banking_agent() -> ChatAgent:
    chat_client = _build_chat_client()

    agent = ChatAgent(
        chat_client=chat_client,
        name="FinanceAgent",
        instructions=(
            "You are an agent from Contoso Bank. You assist users with "
            "financial operations and provide clear explanations. For transfers "
            "only amount, recipient name, and reference are needed."
        ),
        tools=[submit_payment, get_account_balance],
    )

    return agent


if __name__ == "__main__":
    # Simple smoke-test run creating the agent; actual serving is via the MCP server.
    agent = build_banking_agent()
    print("Banking agent initialized with tools:", [t.__name__ for t in agent.tools])
