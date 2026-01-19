# Custom CI image for toolbox repository
# Pre-installs dependencies to avoid apt-get calls on every CI run
#
# This image is built and published by the build-ci-image.yml workflow
# and used by the build-and-test.yml workflow.

FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies that are needed for CI
# - libncurses5: Required for clang-format/llvm_toolchain (libtinfo.so.5)
# - graphviz, graphviz-dev: Required for code visualization tools
# - git: Required for checkout and git operations
# - curl, ca-certificates: Required for downloading tools
# - python3, python3-pip: Required for Python tooling
# - lcov: Required for coverage report generation
RUN apt-get update && apt-get install -y --no-install-recommends \
    libncurses5 \
    graphviz \
    graphviz-dev \
    git \
    curl \
    ca-certificates \
    python3 \
    python3-pip \
    lcov \
    && rm -rf /var/lib/apt/lists/*

# Install Bazelisk (Bazel version manager)
# This downloads the correct Bazel version based on .bazelversion file
ARG BAZELISK_VERSION=1.25.0
RUN curl -fsSL "https://github.com/bazelbuild/bazelisk/releases/download/v${BAZELISK_VERSION}/bazelisk-linux-amd64" \
    -o /usr/local/bin/bazel \
    && chmod +x /usr/local/bin/bazel

# Create a non-root user for running builds
# GitHub Actions runs as uid 1001 by default
RUN useradd -m -u 1001 -s /bin/bash runner

# Set up bazel cache directory with correct permissions
RUN mkdir -p /home/runner/.cache/bazel && chown -R runner:runner /home/runner/.cache

USER runner
WORKDIR /home/runner

# Verify installations
RUN bazel version && python3 --version && git --version
