#!/usr/bin/env python3
"""
Plex Linker entrypoint.

  serve     — Run FastAPI (health, UI, API) and a background link job.
  (default) — Run the link job once (one-shot / cron).
"""
from __future__ import annotations

import argparse
import logging
import threading
import time
from typing import NoReturn

import uvicorn

from app import app
from config import get_settings
from linker import run_link_job

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(name)-14s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _job_loop(interval_minutes: int) -> NoReturn:
    settings = get_settings()
    while True:
        try:
            run_link_job(settings)
        except Exception:
            logging.getLogger(__name__).exception("Link job failed")
        time.sleep(max(60, interval_minutes * 60))


def main() -> None:
    parser = argparse.ArgumentParser(prog="plex-linker")
    sub = parser.add_subparsers(dest="command")

    serve_p = sub.add_parser("serve", help="run web app and background link job")
    serve_p.add_argument("--host", default="0.0.0.0")
    serve_p.add_argument("--port", type=int, default=8080)
    serve_p.add_argument(
        "--interval",
        type=int,
        default=None,
        help="link-job interval in minutes (default: env PLEX_LINKER_SCAN_INTERVAL_MINUTES or 15)",
    )

    args = parser.parse_args()

    if args.command == "serve":
        settings = get_settings()
        interval = args.interval if args.interval is not None else settings.scan_interval_minutes
        threading.Thread(target=_job_loop, args=(interval,), daemon=True).start()
        uvicorn.run(app, host=args.host, port=args.port, log_level="info")
        return

    run_link_job(get_settings())


if __name__ == "__main__":
    main()
