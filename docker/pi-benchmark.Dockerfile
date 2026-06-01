FROM node:22-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PI_SKIP_VERSION_CHECK=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        git \
        python3 \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g --ignore-scripts @earendil-works/pi-coding-agent

WORKDIR /workspace/vibe-browser
COPY . .

CMD ["python3", "scripts/pi_docker_benchmark.py", "--help"]
