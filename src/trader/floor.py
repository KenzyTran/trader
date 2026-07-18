import asyncio

from .accounts import Account
from .agents import TraderAgent
from .config import settings
from .market import is_market_open
from .prompts import STRATEGIES

TRADER_NAMES = tuple(STRATEGIES)


def reset_accounts() -> None:
    for name, strategy in STRATEGIES.items():
        Account.get(name).reset(strategy)


async def run_once() -> list[str]:
    return await asyncio.gather(*(TraderAgent(name).run() for name in TRADER_NAMES))


async def run_forever() -> None:
    traders = [TraderAgent(name) for name in TRADER_NAMES]
    while True:
        if settings.run_when_closed or is_market_open():
            await asyncio.gather(*(trader.run() for trader in traders), return_exceptions=True)
        else:
            print("Market is closed; skipping this cycle")
        await asyncio.sleep(settings.run_every_minutes * 60)
