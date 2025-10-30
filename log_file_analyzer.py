import re
from collections import Counter
import argparse

# Function to parse a single log line (common combined log format-ish)
def parse_log_line(line):
    pattern = re.compile(
        r'(?P<ip>[\d\.]+) - - \[(?P<date_time>[^\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+|-)'
    )
    match = pattern.match(line)
    if match:
        return match.groupdict()
    return None

def analyze_log_file(log_file_path):
    request_counter = Counter()
    status_counter = Counter()
    ip_counter = Counter()
    page_counter = Counter()

    with open(log_file_path, 'r', errors='replace') as file:
        for line in file:
            log_data = parse_log_line(line)
            if log_data:
                request = log_data['request']
                status = log_data['status']
                ip = log_data['ip']

                request_counter[request] += 1
                status_counter[status] += 1
                ip_counter[ip] += 1

                parts = request.split(' ')
                if len(parts) > 1:
                    page = parts[1]
                    page_counter[page] += 1
            else:
                # skip malformed lines silently
                continue

    return request_counter, status_counter, ip_counter, page_counter

def generate_report(log_file_path):
    request_counter, status_counter, ip_counter, page_counter = analyze_log_file(log_file_path)

    lines = []
    lines.append("===== Web Server Log Analysis Report =====")
    num_404_errors = status_counter.get('404', 0)
    lines.append(f"Number of 404 errors: {num_404_errors}")
    lines.append('\nTop 10 Most Requested Pages:')
    for page, count in page_counter.most_common(10):
        lines.append(f"{page}: {count} requests")
    lines.append('\nTop 10 IP Addresses with Most Requests:')
    for ip, count in ip_counter.most_common(10):
        lines.append(f"{ip}: {count} requests")
    lines.append('==========================================')
    report = '\n'.join(lines)
    print(report)
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze a web server log file')
    parser.add_argument('logfile', help='Path to the log file to analyze')
    args = parser.parse_args()
    generate_report(args.logfile)
