import sys
import time
import signal
import argparse
import requests
import yaml
from urllib.parse import urlparse


def parse_args():
    parser = argparse.ArgumentParser(description="HTTP endpoint health checker.")
    parser.add_argument(
        "config_file",
        help=r"C:\\path\\to\\your\\.yaml\\file"
    )
    return parser.parse_args()


def load_configuration(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def extract_domain(url):
    parsed = urlparse(url)  # won't parse the domain if it does not start with http or https which follows the assumption given in the task.
    return parsed.netloc


def is_up(status_code, latency_ms):
    return 200 <= status_code <= 299 and latency_ms < 500


def send_request(endpoint):
    url = endpoint.get("url")
    method = endpoint.get("method", "GET").upper()      # default method is GET if not given
    headers = endpoint.get("headers", {})               # no headers are added if not given
    body = endpoint.get("body", None)                   # default is None if no body is provided
    domain = extract_domain(url)

    start_time = time.perf_counter()
    try:
        response = requests.request(method=method, url=url, headers=headers, data=body, timeout=5)
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000.0  # convert seconds to milliseconds
        up_status = is_up(response.status_code, latency_ms)
    except requests.RequestException:
        up_status = False

    return domain, up_status


def print_availability(availability_tracker):
    for domain, stats in availability_tracker.items():
        up_count = stats["up"]
        total_count = stats["total"]
        percentage = round(100.0 * up_count / total_count) if total_count > 0 else 0
        print(f"{domain} has {percentage}% availability percentage")
    print()


def main():
    def handle_exit(signum, frame):
        print("\nReceived interrupt signal, exiting.")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    
    args = parse_args()

    # Load .yaml file
    endpoints = load_configuration(args.config_file)
    if not isinstance(endpoints, list):
        print("The configuration file must be a YAML list.")
        sys.exit(1)

    availability_tracker = {}

    while True:
        for endpoint in endpoints:
            domain, up_status = send_request(endpoint)

            if domain not in availability_tracker:
                availability_tracker[domain] = {"up": 0, "total": 0}
            availability_tracker[domain]["total"] += 1
            if up_status:
                availability_tracker[domain]["up"] += 1

        print_availability(availability_tracker)

        time.sleep(15)


if __name__ == "__main__":
    main()