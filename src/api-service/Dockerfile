# Production image (development uses Dockerfile.dev).
# Dependencies are installed in a first stage; the image that runs has only the virtualenv and the code.
FROM python:3.13-slim-bookworm AS dependencies
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1
RUN pip install --no-cache-dir uv==0.13.6
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM python:3.13-slim-bookworm
ENV PYTHONUNBUFFERED=1 \
    PATH=/opt/venv/bin:${PATH}
RUN useradd -ms /bin/bash app -d /home/app -u 1000
COPY --from=dependencies /opt/venv /opt/venv
WORKDIR /app
COPY api ./api
# Numeric, so Kubernetes can check runAsNonRoot (it cannot resolve the name `app`)
USER 1000:1000
EXPOSE 9000
CMD ["uvicorn", "api.service:app", "--host", "0.0.0.0", "--port", "9000"]
