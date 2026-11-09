# The workflow tools: kfp and the Vertex AI SDK to compile and submit pipelines, the gcloud CLI, and
# the Docker CLI to build and push the step images (through the laptop's Docker, see docker-shell.sh).
# Used from a shell; it never runs as a pipeline step itself.
FROM python:3.13-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/home/app/.venv \
    UV_LINK_MODE=copy \
    PATH="/home/app/.venv/bin:$PATH"

# The gcloud CLI, and the Docker CLI with buildx (it talks to the laptop's Docker; no daemon here)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /etc/apt/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
        > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian bookworm stable" \
        > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-cloud-cli docker-ce-cli docker-buildx-plugin && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv==0.13.6 && \
    useradd -ms /bin/bash app -d /home/app -u 1000 && \
    mkdir -p /app && \
    chown app:app /app

USER app
WORKDIR /app

# Dependencies first: they only reinstall when pyproject.toml or uv.lock change
COPY --chown=app:app pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY --chown=app:app . ./

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
