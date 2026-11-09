#!/bin/bash

echo "Container is running!!!"
echo "Architecture: $(uname -m)"
echo "Python version: $(python --version)"
echo "UV version: $(uv --version)"

# With arguments, run them as a command and stop. A cluster's Job or a pipeline step works this way:
#   args: ["cli.py", "--process"]
if [[ $# -gt 0 ]]; then
    exec python "$@"
fi

echo -en "\033[92m
The following commands are available:
    python cli.py --check
        Show the settings, and check that ChromaDB and PostgreSQL answer
    python cli.py --process
        Run the processing step (replace it with your own)
\033[0m
"

exec /bin/bash
