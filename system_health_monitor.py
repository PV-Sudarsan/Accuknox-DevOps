#!/usr/bin/env python3

import argparse
import logging
import sys
import time
from logging.handlers import RotatingFileHandler

import psutil

DEFAULT_CPU_THRESHOLD = 80.0
DEFAULT_MEMORY_THRESHOLD = 80.0
DEFAULT_DISK_THRESHOLD = 80.0
DEFAULT_PROCESS_THRESHOLD = 300


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor Linux system health.")
    parser.add_argument("--cpu-threshold", type=float, default=DEFAULT_CPU_THRESHOLD)
    parser.add_argument("--memory-threshold", type=float, default=DEFAULT_MEMORY_THRESHOLD)
    parser.add_argument("--disk-threshold", type=float, default=DEFAULT_DISK_THRESHOLD)
    parser.add_argument("--process-threshold", type=int, default=DEFAULT_PROCESS_THRESHOLD)
    parser.add_argument("--disk-path", default="/")
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--watch", action="store_true", help="Run continuously.")
    parser.add_argument("--log-file", default="system_health.log")
    return parser.parse_args()


def configure_logging(log_file):
    handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler, logging.StreamHandler(sys.stdout)],
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def collect_metrics(disk_path):
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage(disk_path).percent,
        "processes": len(psutil.pids()),
    }


def emit_alerts(metrics, args):
    alerts = []
    if metrics["cpu"] > args.cpu_threshold:
        alerts.append(f"CPU usage {metrics['cpu']}% exceeded {args.cpu_threshold}%")
    if metrics["memory"] > args.memory_threshold:
        alerts.append(f"Memory usage {metrics['memory']}% exceeded {args.memory_threshold}%")
    if metrics["disk"] > args.disk_threshold:
        alerts.append(f"Disk usage {metrics['disk']}% exceeded {args.disk_threshold}% on {args.disk_path}")
    if metrics["processes"] > args.process_threshold:
        alerts.append(
            f"Running process count {metrics['processes']} exceeded {args.process_threshold}"
        )
    for alert in alerts:
        logging.warning(alert)
    return alerts


def run_check(args):
    metrics = collect_metrics(args.disk_path)
    logging.info(
        "System Health - CPU: %.1f%%, Memory: %.1f%%, Disk: %.1f%%, Processes: %s",
        metrics["cpu"],
        metrics["memory"],
        metrics["disk"],
        metrics["processes"],
    )
    alerts = emit_alerts(metrics, args)
    return 1 if alerts else 0


def main():
    args = parse_args()
    configure_logging(args.log_file)

    if args.watch:
        while True:
            run_check(args)
            time.sleep(args.interval)

    raise SystemExit(run_check(args))


if __name__ == "__main__":
    main()
