# EO/IR Detection Stack - Deployment Challenge

A containerized challenge implementation with a Vision API, an inference-worker
status service, a PostgreSQL dependency, model checksum validation, and CI.

## Requirements

- Docker Engine
- Docker Compose v2
- Git
- Python 3.11 for running tests locally

## Quick start

1. Copy `.env.example` to `.env`.
2. Set a strong PostgreSQL password in `.env`.
3. Run:

   ```bash
   docker compose up -d --build
   ```

4. Check services:

   ```bash
   docker compose ps
   docker compose logs
   ```

5. Test API:

   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/api/v1/detect
   ```

Expected healthy response:

```json
{"status":"healthy","worker_ready":true}
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Model artifact

The model checksum is recorded in `models/manifest.json`. The worker validates
the engine file against that SHA256 before reporting readiness.

The supplied engine file is approximately 4 KB. Its checksum can be verified,
but that does not establish that it is a runnable TensorRT engine or compatible
with a particular GPU, TensorRT runtime, CUDA version, or JetPack release.

## Important implementation limitation

This challenge implementation simulates inference readiness using checksum
validation. `/api/v1/detect` returns a sample detection response; it does not
load TensorRT or perform GPU inference. A production implementation needs
TensorRT runtime integration, a compatible CUDA/TensorRT base image, GPU
runtime access, and actual model execution code.

## GitHub

```bash
git init
git add .
git commit -m "Add EOIR deployment challenge solution"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Do not commit `.env` or production secrets.
