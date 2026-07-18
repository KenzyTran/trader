from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field

from .database import read_account, write_account, write_log
from .market import get_share_price

INITIAL_BALANCE = 10_000.0
SPREAD = 0.002


class Transaction(BaseModel):
    symbol: str
    quantity: int
    price: float
    timestamp: str
    rationale: str


class Account(BaseModel):
    name: str
    balance: float = INITIAL_BALANCE
    strategy: str = ""
    holdings: dict[str, int] = Field(default_factory=dict)
    transactions: list[Transaction] = Field(default_factory=list)
    portfolio_value_time_series: list[tuple[str, float]] = Field(default_factory=list)

    @classmethod
    def get(cls, name: str) -> Self:
        stored = read_account(name)
        account = cls(**stored) if stored else cls(name=name.lower())
        if not stored:
            account.save()
        return account

    def save(self) -> None:
        write_account(self.name, self.model_dump())

    def reset(self, strategy: str) -> None:
        self.balance, self.strategy = INITIAL_BALANCE, strategy
        self.holdings, self.transactions, self.portfolio_value_time_series = {}, [], []
        self.save()

    def buy(self, symbol: str, quantity: int, rationale: str) -> str:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        symbol, price = symbol.upper(), get_share_price(symbol) * (1 + SPREAD)
        if price * quantity > self.balance:
            raise ValueError("Insufficient cash")
        self.balance -= price * quantity
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append(Transaction(symbol=symbol, quantity=quantity, price=price, timestamp=str(datetime.now()), rationale=rationale))
        self.save()
        write_log(self.name, "tool", f"Bought {quantity} {symbol}")
        return self.report()

    def sell(self, symbol: str, quantity: int, rationale: str) -> str:
        if quantity <= 0 or self.holdings.get(symbol.upper(), 0) < quantity:
            raise ValueError("Insufficient shares")
        symbol, price = symbol.upper(), get_share_price(symbol) * (1 - SPREAD)
        self.balance += price * quantity
        self.holdings[symbol] -= quantity
        if not self.holdings[symbol]:
            del self.holdings[symbol]
        self.transactions.append(Transaction(symbol=symbol, quantity=-quantity, price=price, timestamp=str(datetime.now()), rationale=rationale))
        self.save()
        write_log(self.name, "tool", f"Sold {quantity} {symbol}")
        return self.report()

    def portfolio_value(self) -> float:
        return self.balance + sum(get_share_price(symbol) * qty for symbol, qty in self.holdings.items())

    def profit_loss(self) -> float:
        return self.portfolio_value() - INITIAL_BALANCE

    def report(self, record: bool = False) -> str:
        value = self.portfolio_value()
        if record:
            self.portfolio_value_time_series.append((str(datetime.now()), value))
            self.save()
        return self.model_dump_json(exclude={"portfolio_value_time_series"}) + f"\nPortfolio value: {value:.2f}; P/L: {self.profit_loss():.2f}"
