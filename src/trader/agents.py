import os
import sys
from pathlib import Path

from strands import Agent
from strands.models import BedrockModel
from strands.models.openai import OpenAIModel
from strands.tools.mcp import MCPClient

from .accounts import Account
from .config import settings
from .database import write_log
from .prompts import researcher_prompt, run_prompt, system_prompt
from .tools import account_tools, lookup_share_price, send_telegram_message

PROVIDER_URLS = {
    "deepseek": "https://api.deepseek.com/v1",
    "grok": "https://api.x.ai/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/",
    "openrouter": "https://openrouter.ai/api/v1",
}
PROVIDER_KEYS = {
    "openai": "OPENAI_API_KEY", "deepseek": "DEEPSEEK_API_KEY", "grok": "GROK_API_KEY",
    "gemini": "GOOGLE_API_KEY", "openrouter": "OPENROUTER_API_KEY",
}


def create_model() -> OpenAIModel | BedrockModel:
    provider = settings.model_provider.lower()
    if provider == "bedrock":
        return BedrockModel(model_id=settings.model_id, region_name=settings.aws_region)
    key = os.getenv(PROVIDER_KEYS.get(provider, "OPENAI_API_KEY"))
    client_args = {"api_key": key}
    if provider in PROVIDER_URLS:
        client_args["base_url"] = PROVIDER_URLS[provider]
    return OpenAIModel(client_args=client_args, model_id=settings.model_id)


def create_research_mcp_client() -> MCPClient:
    """Start the local research MCP server used exclusively by Research Agent."""
    project_root = Path(__file__).resolve().parents[2]
    config = {
        "mcpServers": {
            "research": {
                "command": sys.executable,
                "args": ["-m", "trader.research_server"],
                "cwd": str(project_root),
            }
        }
    }
    return MCPClient.load_servers(config)[0]


class TraderAgent:
    def __init__(self, name: str):
        self.name = name
        self.rebalance_next = False

    async def run(self) -> str:
        account = Account.get(self.name)
        with create_research_mcp_client() as research_mcp:
            researcher = Agent(
                name=f"{self.name}-researcher",
                description="Researches financial news and opportunities for the trading agent.",
                model=create_model(),
                system_prompt=researcher_prompt(),
                tools=research_mcp.list_tools_sync(),
                callback_handler=None,
            )
            research_tool = researcher.as_tool(
                name="research_agent",
                description=(
                    "Delegate financial-news and opportunity research to the specialist Research Agent. "
                    "Provide a specific company, topic, or research objective."
                ),
            )
            agent = Agent(
                name=self.name,
                model=create_model(),
                system_prompt=system_prompt(self.name),
                tools=[*account_tools(self.name), lookup_share_price, research_tool, send_telegram_message],
                callback_handler=None,
            )
            write_log(self.name, "agent", "Run started")
            try:
                result = await agent.invoke_async(
                    run_prompt(self.name, account.strategy, account.report(), self.rebalance_next)
                )
                return str(result)
            finally:
                self.rebalance_next = not self.rebalance_next
                Account.get(self.name).report(record=True)
                write_log(self.name, "agent", "Run ended")
