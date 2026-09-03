#!/bin/bash
# In free mode (no --projectKey) the virtual package feed that serves grafts
# (the strongly-typed client for the remote service) changes on every Graftcode
# Vision / gateway restart. GUID / registry URL rotates. See the current
# `npm install --registry …` in Graftcode Vision (backend, e.g. /GV or the
# Vision UI on the gateway port).
#
# Normally you copy that command by hand and run the latest install.
# This script automates that: wait for /npm (or GRAFT_NPM_URL) and eval the
# current command so the frontend always gets a fresh graft after a free-mode
# restart — never reuse a stored registry URL.
#
# To skip this step: create a free account at https://portal.graftcode.com ,
# get a project key, and start gg with --projectKey. The virtual feed then
# stays stable for the whole project (GUID no longer rotates on restart).
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
