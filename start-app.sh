#!/bin/bash
echo "Running app..."
sudo fuser -k 5000/tcp 2>/dev/null
docker rm -f $(docker ps -aq) 2>/dev/null
docker compose up -d
echo ""
echo "The app is available at http://localhost:5000"
