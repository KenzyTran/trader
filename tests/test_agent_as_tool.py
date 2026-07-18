from trader.agents import TraderAgent


def test_trader_registers_researcher_as_agent_tool(monkeypatch):
    created = []

    class FakeAgent:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            created.append(self)

        def as_tool(self, **kwargs):
            return {"agent": self, **kwargs}

        async def invoke_async(self, prompt):
            return "done"

    class FakeAccount:
        strategy = "value"

        def report(self, record=False):
            return "account"

    monkeypatch.setattr("trader.agents.Agent", FakeAgent)
    monkeypatch.setattr("trader.agents.create_model", lambda: object())
    monkeypatch.setattr("trader.agents.Account.get", lambda name: FakeAccount())
    monkeypatch.setattr("trader.agents.account_tools", lambda name: ["account_tool"])
    monkeypatch.setattr("trader.agents.write_log", lambda *args: None)

    class FakeMCPClient:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def list_tools_sync(self):
            return ["search_financial_news"]

    monkeypatch.setattr("trader.agents.create_research_mcp_client", FakeMCPClient)

    import asyncio

    asyncio.run(TraderAgent("Warren").run())

    researcher, trader = created
    assert researcher.kwargs["name"] == "Warren-researcher"
    assert researcher.kwargs["tools"] == ["search_financial_news"]
    research_tool = trader.kwargs["tools"][2]
    assert research_tool["name"] == "research_agent"
    assert research_tool["agent"] is researcher
