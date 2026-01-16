Use `uv` for local development, Docker container for incompatible environments

Create & update requirements.txt using `uv pip compile pyproject.toml -o requirements.txt`
Build Docker image from Dockerfile.
.dockerignore excludes the virtual environment and uv-related files (including pyproject.toml) from the build

Run Docker image:
`docker run --rm --env-file .env -p 8000:8000 kimymania/ournote-backend:dev`
