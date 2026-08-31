#!/bin/bash
# Install the current Gateway graft. GUID rotates without --projectKey, so
# always pull the command from /npm rather than reusing a stored registry URL.
set -euo pipefail

NPM_URL="${GRAFT_NPM_URL:-http://localhost:8000/npm}"

echo "Waiting for Graftcode Gateway at ${NPM_URL}"
ready=0
for _ in $(seq 1 90); do
  if curl -sS --max-time 5 "${NPM_URL}" 2>/dev/null | grep -q "npm install"; then
    ready=1
    break
  fi
  sleep 2
done

if [ "${ready}" -ne 1 ]; then
  echo "Gateway /npm did not become ready at ${NPM_URL}" >&2
  exit 1
fi

INSTALL_CMD="$(curl -sS --max-time 5 "${NPM_URL}")"
echo "Installing graft from Gateway /npm"
eval "${INSTALL_CMD} --no-fund --no-audit"
