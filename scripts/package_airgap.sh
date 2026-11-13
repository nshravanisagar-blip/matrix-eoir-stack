#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

command -v docker >/dev/null
command -v sha256sum >/dev/null

docker compose build
mkdir -p release

docker save \
  matrix-eoir-stack:1.4.2 \
  postgres:15-alpine \
  -o release/images.tar

cp docker-compose.yml .env.example README.md RUNBOOK.md release/
cp -R models release/

(
  cd release
  find . -type f ! -name SHA256SUMS -print0 |
    sort -z |
    xargs -0 sha256sum > SHA256SUMS
)

echo "Air-gap package created in $ROOT/release"
