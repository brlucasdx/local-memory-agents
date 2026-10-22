#!/usr/bin/env bash
# E8: start llama-server once per arm, run the workloads, stop it. Usage: bash run_all.sh
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SERVER="$HOME/.local/src/llama.cpp-v0.7.0/build/bin/llama-server"
TARGET="/usr/share/ollama/.ollama/models/blobs/sha256-b6f76e74f86245b3caee014b797c10dca931c4dfdaabfb134eab655f81e4154a"
DRAFT="$HOME/.cache/local-memory/models/ornith-dflash-Q4_K_M.gguf"
COMMON=(-m "$TARGET" --no-mmproj -ngl 99 -c 16384 -fa on -np 1 --host 127.0.0.1 --port 8080 --jinja)

declare -A ARMS=(
  [base]=""
  [dflash-n4]="--spec-type draft-dflash --spec-draft-model $DRAFT --spec-draft-ngl 99 --spec-draft-n-max 4"
  [dflash-n8]="--spec-type draft-dflash --spec-draft-model $DRAFT --spec-draft-ngl 99 --spec-draft-n-max 8"
  [ngram-mod]="--spec-type ngram-mod"
  [ngram-cache]="--spec-type ngram-cache"
)

for arm in base dflash-n4 dflash-n8 ngram-mod ngram-cache; do
  # shellcheck disable=SC2086
  "$SERVER" "${COMMON[@]}" ${ARMS[$arm]} > "$HERE/results/server-$arm.log" 2>&1 &
  pid=$!
  for _ in $(seq 1 120); do
    curl -s -m 2 http://127.0.0.1:8080/health | grep -q ok && break
    kill -0 "$pid" 2>/dev/null || break
    sleep 1
  done
  if curl -s -m 2 http://127.0.0.1:8080/health | grep -q ok; then
    python3 -I "$HERE/run.py" --arm "$arm"
  else
    echo "$arm: server failed to start (see results/server-$arm.log)"; tail -5 "$HERE/results/server-$arm.log"
  fi
  kill "$pid" 2>/dev/null; wait "$pid" 2>/dev/null
done
