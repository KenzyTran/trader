import argparse
import asyncio

from .floor import reset_accounts, run_forever, run_once
from .ui import create_ui


def main() -> None:
    parser = argparse.ArgumentParser(description="Strands autonomous trading floor")
    parser.add_argument("command", choices=("run", "once", "api", "ui", "reset"), nargs="?", default="ui")
    args = parser.parse_args()
    if args.command == "reset":
        reset_accounts()
    elif args.command == "ui":
        create_ui().launch()
    elif args.command == "api":
        import uvicorn

        uvicorn.run("trader.api:app", host="127.0.0.1", port=8000, reload=False)
    elif args.command == "once":
        asyncio.run(run_once())
    else:
        asyncio.run(run_forever())


if __name__ == "__main__":
    main()
