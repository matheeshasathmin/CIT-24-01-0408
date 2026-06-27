#!/bin/bash
echo "Removing app..."
docker compose down
docker rmi cybernote_flask 2>/dev/null || true
docker volume rm pgdata 2>/dev/null || true
docker network rm cybernet 2>/dev/null || true
echo "Removed app."
