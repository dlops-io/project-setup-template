# One image for development and for running as a job: see docker-entrypoint.sh.
# The Vertex AI SDK reads GOOGLE_APPLICATION_CREDENTIALS by itself, so there is no gcloud here.
FROM python:3.13-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/home/app/.venv \
    UV_LINK_MODE=copy \
    PATH="/home/app/.venv/bin:$PATH"

RUN pip install --no-cache-dir uv==0.13.6 && \
    useradd -ms /bin/bash app -d /home/app -u 1000 && \
    mkdir -p /app && \
    chown app:app /app

USER app
WORKDIR /app

# Dependencies first: they only reinstall when pyproject.toml or uv.lock change
COPY --chown=app:app pyproject.toml uv.lock ./
RUN uv sync --frozen

# The code is in the image, so it runs as a job with nothing mounted. In development, the
# bind-mounted checkout covers it.
COPY --chown=app:app . ./

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
