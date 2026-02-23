#!/usr/bin/env python3
"""
Plex Linker entrypoint. Single Python entrypoint; no shell wrappers.

  serve   — Run FastAPI (health, UI, API) and background link job.
  (default) — Run link job once (cron or one-shot).
"""
import argparse
import os
import threading
import time
from typing import NoReturn

import uvicorn

from app import app


def _job_loop(interval_minutes: int) -> NoReturn:
    import link_tv_specials
    while True:
        link_tv_specials.run_link_job()
        time.sleep(max(60, interval_minutes * 60))


def main() -> None:
    parser = argparse.ArgumentParser(prog="plex-linker")
    sub = parser.add_subparsers(dest="command", help="command")

    serve_parser = sub.add_parser("serve", help="run web app and background link job")
    serve_parser.add_argument("--host", default="0.0.0.0", help="bind host")
    serve_parser.add_argument("--port", type=int, default=8080, help="bind port")
    serve_parser.add_argument(
        "--interval",
        type=int,
        default=None,
        help="link job interval in minutes (default: env PLEX_LINKER_SCAN_INTERVAL_MINUTES or 15)",
    )
    args = parser.parse_args()

    if args.command == "serve":
        interval = args.interval
        if interval is None:
            interval = int(os.environ.get("PLEX_LINKER_SCAN_INTERVAL_MINUTES", "15"))
        threading.Thread(target=_job_loop, args=(interval,), daemon=True).start()
        uvicorn.run(app, host=args.host, port=args.port, log_level="info")
        return

    # default: run link job once
    import link_tv_specials
    link_tv_specials.run_link_job()


if __name__ == "__main__":
    main()
