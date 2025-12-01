#!/bin/bash

# SSH credentials
REMOTE_USER="rikksullenber"
REMOTE_HOST="37.27.100.190"
REMOTE_PASS='your-ssh-password-here'

# Create deployment directory
expect << EOF
spawn ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} "mkdir -p ~/mealie-ai-deployment"
expect "password:"
send "${REMOTE_PASS}\r"
expect eof
EOF

# Transfer docker-compose file
expect << EOF
spawn scp -o StrictHostKeyChecking=no docker-compose.deploy.yml ${REMOTE_USER}@${REMOTE_HOST}:~/mealie-ai-deployment/
expect "password:"
send "${REMOTE_PASS}\r"
expect eof
EOF

# Deploy on remote server
expect << EOF
spawn ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST}
expect "password:"
send "${REMOTE_PASS}\r"
expect "$ "
send "cd ~/mealie-ai-deployment\r"
expect "$ "
send "docker-compose -f docker-compose.deploy.yml pull\r"
expect "$ "
send "docker-compose -f docker-compose.deploy.yml up -d\r"
expect "$ "
send "docker ps | grep mealie-ai\r"
expect "$ "
send "exit\r"
expect eof
EOF
