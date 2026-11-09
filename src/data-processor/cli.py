"""Data processor: one command-line entry point for every step of the job.

    python cli.py --check      show the settings, and check that ChromaDB and PostgreSQL answer
    python cli.py --process    the processing step: replace it with your own

The same commands run in the interactive shell (docker-shell.sh), in docker compose
(`docker compose run --rm data-processor cli.py --check`), and as a Kubernetes Job or a Vertex AI
pipeline step (args: ["cli.py", "--process"]).
"""

import argparse
import os
import socket
import urllib.request

GCP_PROJECT = os.getenv("GCP_PROJECT")
CHROMADB_HOST = os.getenv("CHROMADB_HOST", "vector-db")
CHROMADB_PORT = int(os.getenv("CHROMADB_PORT", "8000"))
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))


def check():
    print(f"GCP_PROJECT: {GCP_PROJECT}")
    print(f"GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")

    url = f"http://{CHROMADB_HOST}:{CHROMADB_PORT}/api/v2/heartbeat"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            print(f"ChromaDB at {url}: {response.status}")
    except OSError as e:
        print(f"ChromaDB at {url}: not reachable ({e})")

    try:
        with socket.create_connection((POSTGRES_HOST, POSTGRES_PORT), timeout=5):
            print(f"PostgreSQL at {POSTGRES_HOST}:{POSTGRES_PORT}: accepting connections")
    except OSError as e:
        print(f"PostgreSQL at {POSTGRES_HOST}:{POSTGRES_PORT}: not reachable ({e})")


def process():
    # TODO: read the raw data, clean it, write the result (to GCS, PostgreSQL or ChromaDB)
    print("Processing: nothing to do yet. Write your step in process() in cli.py.")


def main():
    parser = argparse.ArgumentParser(description="Data processor")
    parser.add_argument("--check", action="store_true", help="Check settings and services")
    parser.add_argument("--process", action="store_true", help="Run the processing step")
    args = parser.parse_args()

    if not (args.check or args.process):
        parser.print_help()
    if args.check:
        check()
    if args.process:
        process()


if __name__ == "__main__":
    main()
