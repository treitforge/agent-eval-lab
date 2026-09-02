FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates curl git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY codebase/ /app/
RUN python -m pip install --no-cache-dir -e . \
    && rm -rf /app/src/*.egg-info

RUN git config --global user.email "fixture@local" \
    && git config --global user.name "Public Fixture" \
    && git init -b main \
    && git add -A \
    && git commit -m "initialize public scan ledger fixture" \
    && git tag v0.1.0-init

CMD ["bash"]
