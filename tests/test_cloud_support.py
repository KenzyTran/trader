from trader.config import Settings
from trader.database import read_account, write_account


class FakeTable:
    def __init__(self):
        self.items = {}

    def put_item(self, Item):
        self.items[(Item["pk"], Item["sk"])] = Item

    def get_item(self, Key, ConsistentRead=False):
        item = self.items.get((Key["pk"], Key["sk"]))
        return {"Item": item} if item else {}


def test_dynamodb_account_round_trip(monkeypatch):
    table = FakeTable()
    cloud_settings = Settings(storage_backend="dynamodb", dynamodb_table="test-table")
    monkeypatch.setattr("trader.database.settings", cloud_settings)
    monkeypatch.setattr("trader.database.dynamodb_table", lambda: table)

    write_account("Warren", {"balance": 123.0})

    assert read_account("warren") == {"balance": 123.0}


def test_bedrock_model_provider(monkeypatch):
    from strands.models import BedrockModel
    from trader.agents import create_model

    monkeypatch.setattr(
        "trader.agents.settings",
        Settings(model_provider="bedrock", model_id="test-model", aws_region="us-west-2"),
    )

    assert isinstance(create_model(), BedrockModel)
