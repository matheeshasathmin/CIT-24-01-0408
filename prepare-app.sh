#!/bin/bash
echo "Preparing app..."
docker network create cybernet 2>/dev/null || true
docker volume create pgdata 2>/dev/null || true
docker build -t cybernote_flask ./app
echo "Preparation complete!"
