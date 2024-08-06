import os
import subprocess
import sys

# Install required Python packages for DNF
def install_packages():
    try:
        subprocess.run(['dnf', 'install', 'pip'], check=True)
        subprocess.run(['pip', 'install', 'nats-py'], check=True)
    except subprocess.CalledProcessError:
        print("Failed to install required packages. Please install them manually.")
        sys.exit(1)

# Content of the nats_client.py script
nats_client_content = '''import asyncio
from nats.aio.client import Client as NATS

async def run():
    nc = NATS()

    # Connect to the NATS server
    await nc.connect("nats://192.168.40.20:4222")

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print(f"Received a message on \'{subject} {reply}\': {data}")

    # Subscribe to a subject
    await nc.subscribe("weather", cb=message_handler)

    # Keep the connection alive to receive messages
    print("Listening for messages on \'weather\' subject...")
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(run())
'''

# Define the directory and file name
directory = '/dstax-apps'
file_name = 'nats_client.py'
file_path = os.path.join(directory, file_name)

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Write the content to the file
with open(file_path, 'w') as file:
    file.write(nats_client_content)

print(f'{file_name} has been created in {directory}')

# Install required Python packages
install_packages()

# Run the nats_client.py script
try:
    subprocess.run(['python3', file_path], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running the script: {e}")
