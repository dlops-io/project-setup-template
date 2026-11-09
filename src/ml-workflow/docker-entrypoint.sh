#!/bin/bash

echo "Container is running!!!"
echo "Architecture: $(uname -m)"
echo "Python version: $(python --version)"
echo "UV version: $(uv --version)"

# The Python SDKs (kfp, Vertex AI) read GOOGLE_APPLICATION_CREDENTIALS by themselves. gcloud needs
# its own login, for `gcloud storage` and for pushing to Artifact Registry.
if [[ -f "$GOOGLE_APPLICATION_CREDENTIALS" ]]; then
    gcloud auth activate-service-account --key-file "$GOOGLE_APPLICATION_CREDENTIALS" --quiet
    gcloud config set project "$GCP_PROJECT" --quiet
    gcloud auth configure-docker "${GCP_REGION}-docker.pkg.dev" --quiet 2>/dev/null
else
    echo -e "\033[93mNo key at $GOOGLE_APPLICATION_CREDENTIALS: --compile-only works, submitting and pushing do not.\033[0m"
fi
docker info >/dev/null 2>&1 || echo -e "\033[93mCannot reach Docker through /var/run/docker.sock: build-push.sh will not work.\033[0m"

# With arguments, run them as a command and stop: ./docker-shell.sh cli.py --pipeline
if [[ $# -gt 0 ]]; then
    exec python "$@"
fi

echo -en "\033[92m
The following commands are available:
    python cli.py --sample
        Submit the sample pipeline (no images needed): checks your project, bucket and service account
    ./scripts/create-registry.sh
        Create the Artifact Registry repository for the step images (once)
    ./scripts/build-push.sh data-processor
        Build a step image for Vertex AI (linux/amd64) and push it to Artifact Registry
    python cli.py --data-processor | --model-training | --model-deploy
        Submit one step as its own pipeline
    python cli.py --pipeline
        Submit the whole pipeline: data-processor -> model-training -> model-deploy
    Add --compile-only to any of them to write compiled/<name>.yaml without submitting
\033[0m
"

exec /bin/bash
