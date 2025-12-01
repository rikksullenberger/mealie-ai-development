#!/usr/bin/env python3
import paramiko
import time

# Server credentials
hostname = "192.168.30.238"
username = "rikksullenber"
password = "your-ssh-password-here"

# Create SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Connecting to remote server...")
    client.connect(hostname, username=username, password=password)
    
    # Create deployment directory
    print("Creating deployment directory...")
    stdin, stdout, stderr = client.exec_command("mkdir -p ~/mealie-ai-deployment")
    stdout.channel.recv_exit_status()
    
    # Transfer file using SFTP
    print("Transferring docker-compose.deploy.yml...")
    sftp = client.open_sftp()
    sftp.put("docker-compose.deploy.yml", "/home/rikksullenber/mealie-ai-deployment/docker-compose.deploy.yml")
    sftp.close()
    
    # Pull Docker image
    print("Pulling Docker image...")
    stdin, stdout, stderr = client.exec_command("cd ~/mealie-ai-deployment && docker compose -f docker-compose.deploy.yml pull")
    print(stdout.read().decode())
    
    # Start container
    print("Starting container...")
    stdin, stdout, stderr = client.exec_command("cd ~/mealie-ai-deployment && docker compose -f docker-compose.deploy.yml up -d")
    print(stdout.read().decode())
    
    # Check container status
    print("Checking container status...")
    time.sleep(3)
    stdin, stdout, stderr = client.exec_command("docker ps | grep mealie-ai")
    output = stdout.read().decode()
    print(output)
    
    # Get logs
    print("\nContainer logs:")
    stdin, stdout, stderr = client.exec_command("docker logs mealie-ai --tail 50")
    print(stdout.read().decode())
    
    print("\n✅ Deployment complete!")
    
finally:
    client.close()
