# Data Processor

Cleans and transforms raw data, engineers features, and generates embeddings for vector search.

This is the template's example of a **job**: a container that runs one command and stops. Copy it for
`data-collector`, `model-training`, or any other step of a pipeline.

## Run it

In a shell, from this folder:

```bash
./docker-shell.sh
```

| Command | What it does |
|---|---|
| `python cli.py --check` | Show the settings, and check that ChromaDB and PostgreSQL answer |
| `python cli.py --process` | The processing step: write your own in `cli.py` |
| `uv add <package>` | Add a dependency (then run `docker-shell.sh` again to rebuild) |

Start the databases first (`docker compose up -d postgres vector-db` in `src`), or `--check` reports
them as not reachable.

As a job, with the same image:

```bash
./docker-shell.sh cli.py --check
```

```bash
docker compose run --rm data-processor cli.py --process
```

On a cluster, a Kubernetes Job or a Vertex AI pipeline step runs it with `args: ["cli.py", "--process"]`:
see `data_processor()` in [`../ml-workflow/components.py`](../ml-workflow/components.py). Vertex AI pulls the
image from Artifact Registry, so push it after every change with `./scripts/build-push.sh data-processor`
in the workflow shell. Give each argument its own list item: `["--bucket", name]`, never `"--bucket name"`.

## Files

| File | What it does |
|---|---|
| `cli.py` | Every step of the job, as a command-line flag |
| `Dockerfile` | The one image: dependencies, then the code, so it runs as a job with nothing mounted |
| `docker-entrypoint.sh` | With arguments, runs `python <args>` and stops; otherwise opens a shell |
| `docker-shell.sh` | Builds the image and starts a container, with the code and `../secrets` mounted |
