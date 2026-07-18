from trader.config import Settings
from trader.tools import send_telegram_message


def test_telegram_message_is_skipped_without_configuration(monkeypatch):
    monkeypatch.setattr("trader.tools.settings", Settings())

    result = send_telegram_message("No trades")

    assert "not configured" in result


def test_telegram_message_uses_bot_api(monkeypatch):
    settings = Settings(telegram_bot_token="token", telegram_chat_id="123")
    monkeypatch.setattr("trader.tools.settings", settings)

    class Response:
        def raise_for_status(self):
            return None

    calls = []

    def post(url, data, timeout):
        calls.append((url, data, timeout))
        return Response()

    monkeypatch.setattr("trader.tools.requests.post", post)

    result = send_telegram_message("Bought ABC")

    assert result == "Telegram message sent"
    assert calls == [
        (
            "https://api.telegram.org/bottoken/sendMessage",
            {"chat_id": "123", "text": "Bought ABC"},
            15,
        )
    ]
