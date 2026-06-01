FROM node:22-bookworm-slim@sha256:7af03b14a13c8cdd38e45058fd957bf00a72bbe17feac43b1c15a689c029c732

ENV DEBIAN_FRONTEND=noninteractive
ENV PI_SKIP_VERSION_CHECK=1
ENV PI_CODING_AGENT_PACKAGE=@earendil-works/pi-coding-agent
ENV PI_CODING_AGENT_VERSION=0.75.5
ARG VIBE_BENCHMARK_BASE_COMMIT=unknown
ENV VIBE_BENCHMARK_BASE_COMMIT=${VIBE_BENCHMARK_BASE_COMMIT}

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        git \
        python3 \
        python3-tk \
        xvfb \
        xauth \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g --ignore-scripts "${PI_CODING_AGENT_PACKAGE}@${PI_CODING_AGENT_VERSION}"

WORKDIR /workspace/vibe-browser
COPY . .

RUN git init \
    && git config user.name "Vibe Benchmark" \
    && git config user.email "benchmark@example.invalid" \
    && git add . \
    && git commit -m "benchmark baseline"

CMD ["python3", "scripts/pi_docker_benchmark.py", "--help"]
