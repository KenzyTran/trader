import requests
from strands import tool

from .accounts import Account
from .config import settings
from .database import write_log
from .market import get_share_price


def account_tools(name: str):
    @tool
    def account_report() -> str:
        """Return cash, holdings, transactions, portfolio value and profit/loss."""
        return Account.get(name).report()

    @tool
    def buy_shares(symbol: str, quantity: int, rationale: str) -> str:
        """Buy a positive number of shares when sufficient cash is available."""
        return Account.get(name).buy(symbol, quantity, rationale)

    @tool
    def sell_shares(symbol: str, quantity: int, rationale: str) -> str:
        """Sell a positive number of shares already held by this account."""
        return Account.get(name).sell(symbol, quantity, rationale)

    @tool
    def change_strategy(strategy: str) -> str:
        """Replace the account's investment strategy after learning from results."""
        account = Account.get(name)
        account.strategy = strategy
        account.save()
        write_log(name, "tool", "Strategy updated")
        return "Strategy updated"

    return [account_report, buy_shares, sell_shares, change_strategy]


@tool
def lookup_share_price(symbol: str) -> float:
    """Get the latest available or simulated USD share price for a ticker."""
    return get_share_price(symbol)


@tool
def search_financial_news(query: str) -> str:
    """Search current financial news and return concise source snippets."""
    if not settings.tavily_api_key:
        return "TAVILY_API_KEY is not configured; use market data and existing knowledge."
    response = requests.post("https://api.tavily.com/search", json={"api_key": settings.tavily_api_key, "query": query, "topic": "news", "max_results": 5}, timeout=30)
    response.raise_for_status()
    return "\n".join(f"{item['title']}: {item['content']} ({item['url']})" for item in response.json().get("results", []))


@tool
def send_telegram_message(message: str) -> str:
    """Send a brief trading summary to the configured Telegram chat."""
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return f"Telegram message skipped (not configured): {message}"

    response = requests.post(
        f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage",
        data={"chat_id": settings.telegram_chat_id, "text": message},
        timeout=15,
    )
    response.raise_for_status()
    return "Telegram message sent"
