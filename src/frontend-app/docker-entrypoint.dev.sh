#!/bin/bash

echo "Container is running!!!"
echo "Architecture: $(uname -m)"
echo "Node version: $(node --version)"
echo "npm version: $(npm --version)"

# node_modules is a named volume, so this is a full install only the first time.
echo "Installing dependencies..."
npm install --no-fund --no-audit || echo -e "\033[91mnpm install failed: fix the error above, then run it again.\033[0m"

# With arguments (the `command:` in docker-compose.yml), run them instead of opening a shell
if [[ $# -gt 0 ]]; then
    exec "$@"
fi

echo -en "\033[92m
The following commands are available:
    npm run dev
        Run the dev server: http://localhost:3000 (/api goes to the API container)
    npm run check
        Lint, format check and production build
\033[0m
"

exec /bin/bash
