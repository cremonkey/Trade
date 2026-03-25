from __future__ import annotations

import os
from urllib.parse import urlparse

import requests


DEFAULT_PORTS = [9222, 9223, 9234, 51054]


def get_candidate_ports() -> list[int]:
    raw_ports = os.getenv("CDP_PORTS", "")
    if not raw_ports.strip():
        return DEFAULT_PORTS

    ports: list[int] = []
    for chunk in raw_ports.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            ports.append(int(chunk))
        except ValueError:
            continue
    return ports or DEFAULT_PORTS


def find_cdp() -> str | None:
    for port in get_candidate_ports():
        try:
            print(f"Checking port {port}...")
            response = requests.get(f"http://127.0.0.1:{port}/json/version", timeout=1)
            if response.status_code == 200:
                payload = response.json()
                print(f"Found CDP on port {port}!")
                return payload.get("webSocketDebuggerUrl")
        except requests.RequestException:
            continue
    return None


def find_cdp_endpoint() -> str | None:
    websocket_url = find_cdp()
    if not websocket_url:
        return None

    parsed = urlparse(websocket_url)
    if not parsed.scheme or not parsed.netloc:
        return None

    return f"http://{parsed.netloc}"


if __name__ == "__main__":
    websocket_url = find_cdp()
    endpoint_url = find_cdp_endpoint() if websocket_url else None
    if websocket_url:
        print(f"CDP_WS_URL={websocket_url}")
    if endpoint_url:
        print(f"CDP_ENDPOINT={endpoint_url}")
    if not websocket_url:
        print("No CDP found.")
