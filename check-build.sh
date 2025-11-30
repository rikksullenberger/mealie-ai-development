#!/bin/bash
# Monitor Docker build progress

echo "=== Docker Build Status ==="
docker ps -a | grep -i build || echo "No build containers running"

echo -e "\n=== System Resource Usage ==="
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}'

echo "Memory Usage:"
free -h | grep Mem | awk '{print $3 "/" $2}'

echo "Disk Usage:"
df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}'

echo -e "\n=== Docker Disk Usage ==="
docker system df

echo -e "\n=== Running Build Processes ==="
ps aux | grep -E "docker|yarn|node" | grep -v grep | head -10
