# Frontend App

Web UI for interacting with the system: data upload, predictions, and RAG queries. A React app built with
Vite. It talks to `api-service` through `/api` on its own origin.

## Run it

With the whole stack, from `src`: `docker compose up --build`, then http://localhost:3000.

In a shell, from this folder:

```bash
./docker-shell.sh
```

| Command | What it does |
|---|---|
| `npm run dev` | Run the dev server: http://localhost:3000 |
| `npm run check` | Lint, format check and production build |
| `npm run format` | Format the code with Prettier |
| `npm install <package>` | Add a dependency |

## Files

| File | What it does |
|---|---|
| `src/App.jsx` | The page: replace it with your app |
| `vite.config.js` | In development, forwards `/api` to `http://api-service:9000` |
| `nginx.conf.template` | In production, serves the built files and forwards `/api` to `API_URL` |
| `Dockerfile` | Production image: builds with Vite, then nginx serves `dist/` |
| `Dockerfile.dev` | Development image: Node; the code is mounted, `node_modules` is a named volume |
| `docker-entrypoint.dev.sh` | Installs dependencies; with arguments runs them, otherwise opens a shell |
| `docker-shell.sh` | Shell in the running container, or builds and starts one |

## Production image

```bash
docker build -t mlops-app-frontend-app-prod .
```

```bash
docker run --rm -p 8080:80 -e API_URL=http://api-service:9000 --network mlops-app-network mlops-app-frontend-app-prod
```

`API_URL` is where nginx sends `/api`; on Kubernetes it is the API's Service name.
