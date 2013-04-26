#!/usr/bin/python

import pyrax
import time

pyrax.set_credential_file("~/.rackspace_cloud_credentials.txt")

cdb = pyrax.cloud_databases

nam = raw_input("Let's create a new instance. Please enter a name: ")

flavors = cdb.list_flavors()

flavDict = {}
for f, flavor in enumerate(flavors):
    print "Available flavors:"
    print "%s: %s" % (f, flavor.name)
    flavDict[str(f)] = flavor.id
    
selection = raw_input("Select a flavor number: ")

while selection not in flavDict:
    print "Selection not valid, please choose again "
    selection = raw_input("Select flavor number: ")

choice = flavors[int(selection)]
size = int(raw_input("Enter the volume size in GB (1-50): "))

instance = cdb.create(nam, flavor=choice, volume=size)
print "Creating new instance: "
print "Name:", instance.name
print "ID:", instance.id
print "Status:", instance.status
print "Hostname: ", instance.hostname

while instance.status != 'ACTIVE':
    instance = cdb.get(instance)
    time.sleep(10)
    print "Building..."
    
print "New instance status: Active"

print ""
print "Great, now let's create a new database."

db_name = raw_input("Name the new DB: ")

db = cdb.create_database(instance, db_name)
print "DB created: ", db

print ""
print "Now, let's create a DB user account..."
username = raw_input("Enter account name: ")
passwd = raw_input("Enter password for new DB user: ")
user = instance.create_user(name=username, password=passwd, database_names=[db])
print "User account created: ", user






    

