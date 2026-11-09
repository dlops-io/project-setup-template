#!/bin/bash

echo "Container is running!!!"
echo "Architecture: $(uname -m)"
echo "Python version: $(python --version)"
echo "UV version: $(uv --version)"

# The image has the dependencies; this only picks up a change to uv.lock since it was built.
uv sync --frozen
source /home/app/.venv/bin/activate

api_server() {
    local server=(uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload --reload-dir api/ "$@")
    # In the shell, Ctrl-C stops it and gives the prompt back. From docker compose, uvicorn takes
    # this script's place, so it gets Docker's stop signal.
    if [[ $- == *i* ]]; then "${server[@]}"; else exec "${server[@]}"; fi
}

export -f api_server

# With arguments (the `command:` in docker-compose.yml), run them instead of opening a shell
if [[ $# -gt 0 ]]; then
    if [[ $(type -t "$1") == function ]]; then
        "$@"
        exit
    fi
    exec "$@"
fi

echo -en "\033[92m
The following commands are available:
    api_server
        Run the API server: http://localhost:9000/api/docs
    pytest
        Run the tests
\033[0m
"

exec /bin/bash
