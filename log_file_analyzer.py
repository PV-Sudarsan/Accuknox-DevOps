#!/usr/bin/env python3

import argparse
import re
from collections import Counter

LOG_PATTERN = re.compile(
    r'(?P<ip>[\d\.]+)\s+\S+\s+\S+\s+\[(?P<date_time>[^\]]+)\]\s+"(?P<request>[^"]+)"\s+'
    r"(?P<status>\d{3})\s+(?P<size>\d+|-)"
)


def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    return match.groupdict() if match else None


def analyze_log_file(log_file_path):
    status_counter = Counter()
    ip_counter = Counter()
    page_counter = Counter()
    malformed_lines = 0

    with open(log_file_path, "r", encoding="utf-8", errors="replace") as file_handle:
        for line in file_handle:
            log_data = parse_log_line(line)
            if not log_data:
                malformed_lines += 1
                continue

            request = log_data["request"].split()
            status_counter[log_data["status"]] += 1
            ip_counter[log_data["ip"]] += 1

            if len(request) >= 2:
                page_counter[request[1]] += 1

    return status_counter, ip_counter, page_counter, malformed_lines


def generate_report(log_file_path, top_n):
    status_counter, ip_counter, page_counter, malformed_lines = analyze_log_file(log_file_path)
    report_lines = [
        "===== Web Server Log Analysis Report =====",
        f"Number of 404 errors: {status_counter.get('404', 0)}",
        f"Malformed lines skipped: {malformed_lines}",
        "",
        f"Top {top_n} Most Requested Pages:",
    ]

    for page, count in page_counter.most_common(top_n):
        report_lines.append(f"{page}: {count} requests")

    report_lines.extend(
        [
            "",
            f"Top {top_n} IP Addresses with Most Requests:",
        ]
    )

    for ip, count in ip_counter.most_common(top_n):
        report_lines.append(f"{ip}: {count} requests")

    report_lines.append("==========================================")
    report = "\n".join(report_lines)
    print(report)
    return report


def main():
    parser = argparse.ArgumentParser(description="Analyze an Apache or Nginx access log.")
    parser.add_argument("logfile", help="Path to the log file to analyze")
    parser.add_argument("--top", type=int, default=10, help="Number of top results to show")
    args = parser.parse_args()
    generate_report(args.logfile, args.top)


if __name__ == "__main__":
    main()
