# Operations Runbook

## Start

```bash
docker compose up -d --build
docker compose ps
```

## Health

```bash
curl -i http://localhost:8000/health
docker compose ps
docker compose logs --tail=100 vision_api inference_worker
```

The API reports healthy only when the worker returns HTTP 200 and both
`engine_loaded` and `checksum_valid` are true.

## Checksum failure

1. Inspect `models/manifest.json`.
2. Calculate the actual file hash:

   ```bash
   sha256sum models/eo_detector_fp16.engine
   ```

3. Confirm the engine is the approved artifact.
4. Update the manifest only with the checksum of the approved engine.
5. Restart:

   ```bash
   docker compose restart inference_worker vision_api
   ```

Do not update the manifest merely to make an untrusted or corrupted file pass.

## Logs

```bash
docker compose logs -f inference_worker
docker compose logs -f vision_api
docker compose logs -f postgres
```

## Rollback

Restore the previous matching application image, engine binary, and manifest
as one release. Then run:

```bash
docker compose up -d
```

Do not use `docker compose down -v` for routine rollback; it deletes the
PostgreSQL data volume.
