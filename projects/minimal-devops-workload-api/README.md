## CI/CD Release Pipeline

This project includes a GitHub Actions pipeline that validates the application before publishing a container image.

The pipeline runs on push, pull request, and manual workflow dispatch. It performs the following checks:

```text
pytest test suite
→ Docker image build
→ container smoke test using /health
→ GHCR image push on push events
→ release tag publishing for Git tags such as v0.2.0
```

The Docker image is published to GitHub Container Registry:

```text
ghcr.io/almutaz97/minimal-devops-workload-api
```

Each pushed commit produces an immutable image tag based on the Git commit SHA. Release tags such as `v0.2.0` are also published when a Git tag is pushed.

Example release image:

```bash
docker pull ghcr.io/almutaz97/minimal-devops-workload-api:v0.2.0
```

Run the release image locally:

```bash
docker rm -f minimal-api-release 2>/dev/null || true

docker run -d \
  --name minimal-api-release \
  -p 18000:8000 \
  ghcr.io/almutaz97/minimal-devops-workload-api:v0.2.0

curl -i http://localhost:18000/health
```

Expected result:

```text
HTTP/1.1 200 OK
```

## Rollback Strategy

Rollback is performed by switching from the current release image tag to a previous known-good image tag.

Example rollback from `v0.2.0` to `v0.1.0`:

```bash
docker rm -f minimal-api-release

docker run -d \
  --name minimal-api-release \
  -p 18000:8000 \
  ghcr.io/almutaz97/minimal-devops-workload-api:v0.1.0

curl -i http://localhost:18000/health
```

This rollback does not rebuild the image or change source code. It simply runs a previously built and published image artifact.

The key release principle is:

```text
Build once
test the image
publish the image
deploy the tested image
rollback by selecting a previous image tag
```

