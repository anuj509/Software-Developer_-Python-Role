"""Entry point of build project"""
import subprocess
import shutil
import os
import zipfile
import os
from os import getenv, path
from config import (
    SCP_DESTINATION_FOLDER,
    SSH_KEY_FILEPATH,
    SSH_PASSWORD,
    SSH_REMOTE_HOST,
    SSH_USERNAME,
)
from paramiko_client import initiate_client
from paramiko_client.client import RemoteClient
import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)
logging.debug('started')

# Create SSH remote client connection
ssh_remote_client = RemoteClient(
    SSH_REMOTE_HOST,
    SSH_USERNAME,
    SSH_PASSWORD,
    SSH_KEY_FILEPATH,
    SCP_DESTINATION_FOLDER,
)
create_n_files = input("Create How many files on remote? :")
commandInput = input("Enter Command to execute on remote server: (For Multiple commands use |||) :")
local_file_dir_to_upload = input("Local File Upload directory (Relative path): ")
commands = [
            # "df -h",
            # "df -i /",
            # "ls -l /usr/home",
            "touch /home/admin/test{0001..000"+str(create_n_files)+"}.txt"
        ]

for command in commandInput.split("|||"):
    commands.append(command)        

zipallfiles = "zip -m output.zip test*"
commands.append(zipallfiles)
        
initiate_client(ssh_remote_client,commands,local_file_dir_to_upload)
proc = subprocess.Popen('"C:\Program Files\7-Zip\7z.exe" x output.zip', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out, err = proc.communicate()
    
