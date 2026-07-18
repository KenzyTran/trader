import gradio as gr
import pandas as pd
import plotly.express as px

from .accounts import Account
from .database import read_logs
from .floor import TRADER_NAMES


def snapshot(name: str):
    account = Account.get(name)
    value, pnl = account.portfolio_value(), account.profit_loss()
    summary = f"## {name}\nPortfolio **${value:,.2f}** · P/L **${pnl:+,.2f}**\n\n{account.strategy}"
    history = pd.DataFrame(account.portfolio_value_time_series, columns=["datetime", "value"])
    chart = px.line(history, x="datetime", y="value", title="Portfolio value") if not history.empty else None
    holdings = pd.DataFrame([{"symbol": key, "quantity": value} for key, value in account.holdings.items()])
    transactions = pd.DataFrame([tx.model_dump() for tx in account.transactions[-20:]])
    logs = "\n".join(f"{ts} [{kind}] {message}" for ts, kind, message in read_logs(name))
    return summary, chart, holdings, transactions, logs


def create_ui() -> gr.Blocks:
    with gr.Blocks(title="Strands Trading Floor") as app:
        gr.Markdown("# Strands Trading Floor")
        with gr.Tabs():
            for name in TRADER_NAMES:
                with gr.Tab(name):
                    summary = gr.Markdown()
                    chart = gr.Plot()
                    holdings = gr.Dataframe()
                    transactions = gr.Dataframe()
                    logs = gr.Textbox(lines=10, label="Activity")
                    refresh = gr.Button("Refresh")
                    refresh.click(lambda trader=name: snapshot(trader), outputs=[summary, chart, holdings, transactions, logs])
                    app.load(lambda trader=name: snapshot(trader), outputs=[summary, chart, holdings, transactions, logs])
    return app
