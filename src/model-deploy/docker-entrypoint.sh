#!/bin/bash

echo "Container is running!!!"
echo "Architecture: $(uname -m)"
echo "Python version: $(python --version)"
echo "UV version: $(uv --version)"

[[ -f "$GOOGLE_APPLICATION_CREDENTIALS" ]] || \
    echo -e "\033[93mNo key at $GOOGLE_APPLICATION_CREDENTIALS: the commands below need one.\033[0m"

# With arguments, run them as a command and stop: ./docker-shell.sh cli.py --predict
if [[ $# -gt 0 ]]; then
    exec python "$@"
fi

echo -en "\033[92m
The following commands are available:
    python cli.py --upload
        Register the trained model in the Model Registry, as a new version
    python cli.py --deploy
        Deploy the newest version to the endpoint (often 10-20 minutes; billed until --cleanup)
    python cli.py --predict
        Send a sample request to the endpoint
    python cli.py --cleanup
        Undeploy the model and delete the endpoint, so it stops billing
\033[0m
"

exec /bin/bash
