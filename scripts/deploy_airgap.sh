#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/release"

sha256sum -c SHA256SUMS
docker load -i images.tar

cp .env.example .env
echo "Edit release/.env and set a strong POSTGRES_PASSWORD."
echo "Then run: docker compose up -d --no-build --pull never"
