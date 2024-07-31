import os
import subprocess
import sys


subprocess.run(['dnf', 'install', 'git'], check=True)

# Define the commands to be executed
commands = [
    "wget https://github.com/nats-io/nats-server/releases/download/v2.10.2/nats-server-v2.10.2-linux-amd64.tar.gz",
    "tar -zxvf nats-server-v2.10.2-linux-amd64.tar.gz",
    "mv nats-server-v2.10.2-linux-amd64/nats-server /usr/local/bin/",
]

# Execute the commands
for command in commands:
    subprocess.run(command, shell=True, check=True)

# Create the start_nats.sh script
start_nats_script = '''#!/bin/bash
# Get the IP address of the host machine dynamically using the ip command
HOST_IP=$(ip addr show backchan0 | grep "inet " | awk '{print $2}' | cut -d/ -f1)
# Start the NATS server with the dynamically retrieved IP address
nats-server -a $HOST_IP -p 4222
'''

# Write the start_nats.sh script to a file
with open("start_nats.sh", "w") as file:
    file.write(start_nats_script)

# Make the start_nats.sh script executable
os.chmod("start_nats.sh", 0o755)

# Execute the start_nats.sh script
subprocess.run("./start_nats.sh", shell=True, check=True)