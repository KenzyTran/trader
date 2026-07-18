from trader.accounts import Account, INITIAL_BALANCE
from trader.config import Settings


def test_buy_and_sell(monkeypatch, tmp_path):
    test_settings = Settings(data_dir=tmp_path)
    monkeypatch.setattr("trader.config.settings", test_settings)
    monkeypatch.setattr("trader.database.settings", test_settings)
    monkeypatch.setattr("trader.accounts.get_share_price", lambda _: 100.0)
    account = Account.get("test")
    account.buy("ABC", 2, "test")
    assert account.holdings == {"ABC": 2}
    account.sell("ABC", 1, "test")
    assert account.holdings == {"ABC": 1}
    assert account.balance < INITIAL_BALANCE
