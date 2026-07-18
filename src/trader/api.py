"""Read-only HTTP API consumed by the React dashboard."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .accounts import Account
from .config import settings
from .database import read_logs
from .floor import TRADER_NAMES
from .market import get_share_price, is_market_open

LAST_NAMES = dict(zip(TRADER_NAMES, ("Patience", "Bold", "Systematic", "Crypto"), strict=True))
MODEL_LABELS = {name: settings.model_id for name in TRADER_NAMES}
LOG_COLORS = {"agent": "#38bdf8", "tool": "#34d399", "error": "#fb7185"}

app = FastAPI(title="Strands Trading Floor API", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def require_trader(name: str) -> str:
    canonical = next((item for item in TRADER_NAMES if item.lower() == name.lower()), None)
    if canonical is None:
        raise HTTPException(status_code=404, detail=f"Unknown trader: {name}")
    return canonical


def average_cost(account: Account, symbol: str) -> float:
    buys = [tx for tx in account.transactions if tx.symbol == symbol and tx.quantity > 0]
    quantity = sum(tx.quantity for tx in buys)
    return sum(tx.quantity * tx.price for tx in buys) / quantity if quantity else 0.0


def trader_snapshot(name: str) -> dict:
    account = Account.get(name)
    holdings = []
    for symbol, quantity in account.holdings.items():
        price = get_share_price(symbol)
        cost = average_cost(account, symbol)
        holdings.append(
            {
                "symbol": symbol,
                "quantity": quantity,
                "price": price,
                "avg_cost": cost,
                "market_value": price * quantity,
                "unrealized_pnl": (price - cost) * quantity,
            }
        )
    portfolio_value = account.balance + sum(item["market_value"] for item in holdings)
    return {
        "name": name,
        "lastname": LAST_NAMES[name],
        "model_name": MODEL_LABELS[name],
        "strategy": account.strategy,
        "balance": account.balance,
        "portfolio_value": portfolio_value,
        "pnl": account.profit_loss(),
        "holdings": holdings,
        "transactions": [tx.model_dump() for tx in reversed(account.transactions[-30:])],
        "time_series": [
            {"datetime": timestamp, "value": value}
            for timestamp, value in account.portfolio_value_time_series
        ],
    }


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/market")
def market_status() -> dict:
    return {
        "source": "massive" if settings.massive_api_key else "simulator",
        "is_market_open": is_market_open(),
    }


@app.get("/api/traders")
def traders() -> list[dict]:
    return [
        {"name": name, "lastname": LAST_NAMES[name], "model_name": MODEL_LABELS[name]}
        for name in TRADER_NAMES
    ]


@app.get("/api/traders/{name}")
def trader(name: str) -> dict:
    return trader_snapshot(require_trader(name))


@app.get("/api/traders/{name}/logs")
def trader_logs(name: str, last_n: int = Query(default=13, ge=1, le=200)) -> list[dict]:
    canonical = require_trader(name)
    return [
        {
            "datetime": timestamp,
            "type": kind,
            "message": message,
            "color": LOG_COLORS.get(kind, "#94a3b8"),
        }
        for timestamp, kind, message in read_logs(canonical, last_n)
    ]
