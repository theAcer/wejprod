FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.10

FROM redis:latest

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends postgresql-client redis-server \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Expose the default Redis port
EXPOSE 6379

CMD ["redis-server", "--port", "6379"]
