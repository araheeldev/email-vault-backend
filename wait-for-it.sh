#!/usr/bin/env bash
set -e

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <host> <port> [command]"
  exit 1
fi

HOST=$1
PORT=$2
shift 2

echo "Waiting for $HOST:$PORT to be available..."

for i in $(seq 1 40); do
  if (echo > /dev/tcp/$HOST/$PORT) &> /dev/null; then
    echo "$HOST:$PORT is up and running!"
    exec "$@"
    exit 0
  fi
  echo "Attempt $i: Waiting for $HOST:$PORT..."
  sleep 2
done

echo "Timeout reached: $HOST:$PORT is not available"
exit 1
