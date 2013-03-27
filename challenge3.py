#Challenge 3: Write a script that accepts a directory as an argument as well as a container name.
#The script should upload the contents of the specified directory to the
#container (or create it if it doesn't exist). The script should handle errors
#appropriately. (Check for invalid paths, etc.) Worth 2 Points

# Copyright 2012 Jason Quiroga

# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pyrax
import os
import sys
import time

pyrax.set_credential_file("/Users/jaso4210/.rackspace_cloud_credentials.txt")

cf = pyrax.cloudfiles

args = sys.argv[0:]

path = args[1]
container = args[2]

if args is None:
    path = raw_input("Enter full path to the directory you want to upload: ")
    container = raw_input("Enter the name of the target container. \ If the container does not exist, it will be created: ")

if os.path.exists(path) == False:
    print "File not found"
    path = raw_input("Enter full path to the directory you want to upload: ")

# This will upload the contents of the target folder to a container
# named 'software'. If that container does not exist, it will be created.
upload_key, total_bytes = cf.upload_folder(path, container=container)

uploaded = cf.get_uploaded(upload_key)

print "%s bytes will be uploaded" % (total_bytes)
print ""

while uploaded < total_bytes:
    uploaded = cf.get_uploaded(upload_key)
#    print "%s of %s bytes uploaded" % (uploaded, total_bytes)
    print "Progress: %3.0f%%" % ((uploaded * 100.0) / total_bytes)
    time.sleep(2)
    
print "Upload complete"



