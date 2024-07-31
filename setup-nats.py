import os
import subprocess
import sys

subprocess.run(['dnf', 'install', 'git'], check=True)

# Define the directories and files
dir_path = "/etc/eventflux/conf"
nats_file = os.path.join(dir_path, "nats.conf")
kafka_file = os.path.join(dir_path, "kafka.conf")
postgresql_file = os.path.join(dir_path, "postgresql.conf")
sqlite_file = os.path.join(dir_path, "sqlite.conf")
usr_local_bin_path = "/usr/local/bin"
continuous_file = os.path.join(usr_local_bin_path, "continuous.conf")
run_script_file = os.path.join(usr_local_bin_path, "run_eventflux.sh")

# Define the content for nats.conf
nats_conf_content = '''{
  "configs": [
    {
      "forward_config_key": "natsconfig1",
      "uri": "nats://192.168.40.20:4222",
      "topic": "weather",
      "eventEnable": true
    },
    {
      "forward_config_key": "natsconfig2",
      "uri": "nats://another_host:4222",
      "topic": "your_second_topic",
      "eventEnable": false
    }
  ]
}'''

# Define the content for other config files
other_conf_content = '''{
  "configs": [

  ]
}'''

# Define the content for continuous.conf
continuous_conf_content = '''{
    "collectorlabel": "$HOSTNAME",
    "commands": [
        {
            "collectorlabel": "$HOSTNAME",
            "command": "while true; do data=$(curl -s 'http://wttr.in/Dallas?format=%t+%h+%w&u'); echo \\"{\\\\\\"temp\\\\\\": \\\\\\"$(echo $data | awk '{print $1}')\\\\\\", \\\\\\"humidity\\\\\\": \\\\\\"$(echo $data | awk '{print $2}')\\\\\\", \\\\\\"wind\\\\\\": \\\\\\"$(echo $data | awk '{print $3}')\\\\\\"}\\"; sleep 10; done",
            "command_type": "continuous",
            "datalabel": "continuous_test1",
            "description": "Echo command outputting continuous value 1",
            "forward_config_key": [
                "natsconfig1"
            ],
            "port": 5556
        }
    ]
}'''

# Define the content for the run script
run_script_content = '''#!/bin/bash
/usr/local/bin/EventFlux -f /usr/local/bin/continuous.conf
'''

# Create the directory structure for /etc/eventflux/conf
os.makedirs(dir_path, exist_ok=True)

# Create and write to nats.conf
with open(nats_file, "w") as file:
    file.write(nats_conf_content)

# Create and write to kafka.conf, postgresql.conf, and sqlite.conf
for conf_file in [kafka_file, postgresql_file, sqlite_file]:
    with open(conf_file, "w") as file:
        file.write(other_conf_content)

# Create the directory structure for /usr/local/bin if it doesn't exist
os.makedirs(usr_local_bin_path, exist_ok=True)

# Create and write to continuous.conf
with open(continuous_file, "w") as file:
    file.write(continuous_conf_content)

# Create and write to the run script
with open(run_script_file, "w") as file:
    file.write(run_script_content)

# Make the run script executable
os.chmod(run_script_file, 0o755)

# Confirm the creation of files
print(f"Configuration files created in {dir_path}:")
for file_name in [nats_file, kafka_file, postgresql_file, sqlite_file]:
    print(file_name)

print(f"Configuration file created in {usr_local_bin_path}:")
print(continuous_file)
print(f"Run script created in {usr_local_bin_path}:")
print(run_script_file)
