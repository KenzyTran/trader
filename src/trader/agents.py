import os

from strands import Agent
from strands.models import BedrockModel
from strands.models.openai import OpenAIModel

from .accounts import Account
from .config import settings
from .database import write_log
from .prompts import run_prompt, system_prompt
from .tools import account_tools, lookup_share_price, search_financial_news, send_telegram_message

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


class TraderAgent:
    def __init__(self, name: str):
        self.name = name
        self.rebalance_next = False

    async def run(self) -> str:
        account = Account.get(self.name)
        agent = Agent(
            name=self.name,
            model=create_model(),
            system_prompt=system_prompt(self.name),
            tools=[*account_tools(self.name), lookup_share_price, search_financial_news, send_telegram_message],
            callback_handler=None,
        )
        write_log(self.name, "agent", "Run started")
        try:
            result = await agent.invoke_async(run_prompt(self.name, account.strategy, account.report(), self.rebalance_next))
            return str(result)
        finally:
            self.rebalance_next = not self.rebalance_next
            Account.get(self.name).report(record=True)
            write_log(self.name, "agent", "Run ended")
