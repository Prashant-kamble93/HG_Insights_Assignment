#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

if [[ "$#" -ne 1 ]]; then
  echo "ERROR: Exactly one argument required: 'runtime' or 'dev'"
  exit 1
fi

INSTALL_TYPE="$1"

RUNTIME_PACKAGES="libffi8 libssl3 libldap-2.5-0 netcat-openbsd curl lsb-release"
DEV_PACKAGES="build-essential git libffi-dev libssl-dev libldap2-dev"

echo "Updating package lists..."
apt-get update -y

case "$INSTALL_TYPE" in
  runtime)
    echo "Installing runtime dependencies..."
    apt-get install -y --no-install-recommends $RUNTIME_PACKAGES
    ;;
  dev)
    echo "Installing development dependencies..."
    apt-get install -y --no-install-recommends $DEV_PACKAGES
    ;;
  *)
    echo "ERROR: Invalid argument '$INSTALL_TYPE'. Use 'runtime' or 'dev'."
    exit 1
    ;;
esac

echo "Cleaning up apt cache..."
apt-get clean
rm -rf /var/lib/apt/lists/*
