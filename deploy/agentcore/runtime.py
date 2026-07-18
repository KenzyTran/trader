"""Amazon Bedrock AgentCore Runtime entrypoint for the Strands trading floor."""

import asyncio
from typing import Any

from bedrock_agentcore import BedrockAgentCoreApp

from trader.agents import TraderAgent
from trader.floor import TRADER_NAMES

app = BedrockAgentCoreApp()


async def run_traders(trader_name: str | None = None) -> list[dict[str, str]]:
    names = [trader_name] if trader_name else list(TRADER_NAMES)
    unknown = [name for name in names if name not in TRADER_NAMES]
    if unknown:
        raise ValueError(f"Unknown trader: {unknown[0]}")
    results = await asyncio.gather(*(TraderAgent(name).run() for name in names))
    return [{"trader": name, "result": result} for name, result in zip(names, results, strict=True)]


@app.entrypoint
async def invoke(payload: dict[str, Any]) -> dict[str, Any]:
    """Run one trader or a complete scheduled trading cycle."""
    trader_name = payload.get("trader")
    prompt = str(payload.get("prompt", "")).strip()
    if not trader_name and prompt in TRADER_NAMES:
        trader_name = prompt
    return {"status": "completed", "traders": await run_traders(trader_name)}


if __name__ == "__main__":
    app.run()
