"""Mede latência (média e p95) dos endpoints de leitura da API em execução.

Uso: poetry run python scripts/benchmark.py [--base-url http://localhost:8000] [-n 50]
Requer o backend rodando em modo development (usa os headers X-Dev-*).
"""

import argparse
import statistics
import time

import httpx

ENDPOINTS = ["/api/v1/health", "/api/v1/me", "/api/v1/runops/templates", "/api/v1/runops/requests", "/api/v1/cloudwise/dashboard"]


def p95(values: list[float]) -> float:
    ordered = sorted(values)
    return ordered[max(0, int(round(0.95 * len(ordered))) - 1)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("-n", type=int, default=50)
    args = parser.parse_args()

    headers = {"X-Dev-User-Id": "dev-user", "X-Dev-User-Email": "dev-user@dev.local"}
    print(f"{'endpoint':<36}{'n':>4}{'média (ms)':>13}{'p95 (ms)':>11}")
    with httpx.Client(base_url=args.base_url, headers=headers, timeout=10) as client:
        for path in ENDPOINTS:
            samples: list[float] = []
            for _ in range(args.n):
                start = time.perf_counter()
                response = client.get(path)
                samples.append((time.perf_counter() - start) * 1000)
                response.raise_for_status()
            print(f"{path:<36}{args.n:>4}{statistics.mean(samples):>13.1f}{p95(samples):>11.1f}")


if __name__ == "__main__":
    main()
