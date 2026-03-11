#!/usr/bin/env python3

import argparse
import sys
import urllib.error
import urllib.request


def parse_args():
    parser = argparse.ArgumentParser(description="Check an application's HTTP health.")
    parser.add_argument("url", help="Application URL to probe")
    parser.add_argument("--timeout", type=int, default=10)
    return parser.parse_args()


def main():
    args = parse_args()
    request = urllib.request.Request(args.url, method="GET")

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            status_code = response.getcode()
    except urllib.error.HTTPError as exc:
        status_code = exc.code
    except urllib.error.URLError as exc:
        print(f"DOWN - request failed: {exc.reason}")
        raise SystemExit(1)

    if 200 <= status_code < 400:
        print(f"UP - HTTP {status_code}")
        raise SystemExit(0)

    print(f"DOWN - HTTP {status_code}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
