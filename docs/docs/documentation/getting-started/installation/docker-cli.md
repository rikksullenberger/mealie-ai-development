# Docker Command Line Installation

If you prefer using the Docker CLI directly instead of Docker Compose, you can run Mealie using the `docker run` command.

## SQLite (Simple Setup)

Run the following command to start Mealie with a local SQLite database and persistent volume:

```bash
docker run -d \
  --name mealie \
  -p 9925:9000 \
  -v mealie-data:/app/data/ \
  -e ALLOW_SIGNUP="true" \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ="America/New_York" \
  -e BASE_URL="http://localhost:9925" \
  --restart always \
  ghcr.io/mealie-recipes/mealie:latest
```

### Breakdown of Flags:
- `-d`: Run in detached mode (background).
- `--name mealie`: Assigns the name "mealie" to the container.
- `-p 9925:9000`: Maps port 9925 on your host to port 9000 in the container. Access via `http://localhost:9925`.
- `-v mealie-data:/app/data/`: Persists data to a Docker volume named `mealie-data`.
- `-e ...`: Sets environment variables (see [Backend Configuration](./backend-config.md) for full list).

## With OpenAI Enabled

To enable AI features directly via CLI:

```bash
docker run -d \
  --name mealie \
  -p 9925:9000 \
  -v mealie-data:/app/data/ \
  -e OPENAI_API_KEY="sk-..." \
  -e OPENAI_ENABLE_IMAGE_SERVICES="true" \
  --restart always \
  ghcr.io/mealie-recipes/mealie:latest
```
