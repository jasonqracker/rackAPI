import pyrax
import time

pyrax.set_credential_file("/home/hal/.rackspace_cloud_credentials.txt")

cs = pyrax.cloudservers

servers = cs.servers.list()

servDict = {}

print "Choose a server to clone from the list"
print ""

for num, server in enumerate(servers):
  print ("%s " + " Name: " + "%s" + "  ID: " + "%s") % (num, server.name, server.id)
  servDict[str(num)] = server.id

choice = raw_input("Select server number: ")
while choice not in servDict:
  if choice is not None:
    print "Selection not valid, please choose again "
    choice = raw_input("Select server number: ")

server_id = servDict[str(choice)]

imageName = raw_input("Name the image to be created: ")

flavors = cs.flavors.list()

flavDict = {}

print "Choose a flavor for the new server: "

for num, flavor in enumerate(flavors):
  print "%s    %s" % (num, flavor)
  flavDict[str(num)] = flavor

choice = raw_input("Select flavor number: ")
while choice not in flavDict:
  if choice is not None:
    print "Selection not valid, please choose again: "
    choice = raw_input("Select flavor number: ")

flavor_id = flavDict[choice]

image_id = [cs.servers.create_image(server_id, imageName)][0]

print "Image %s is being created with the ID: %s" % (imageName, image_id)
print ""
print "Image saving. Please stand by..."
print ""
images = cs.images.list()
while str(images[0].status) != 'ACTIVE':
  time.sleep(10)
  images = cs.images.list()

serverName = raw_input("Name the new cloud server: ")

server = cs.servers.create(serverName, image_id, flavor_id.id)
print "ID: ", server.id
print "Status: ", server.status
print "Admin Password: ", server.adminPass
print "Waiting for network provisioning..."
while not (server.networks):
  time.sleep(2)
  server = cs.servers.get(server.id)
print "Networks: ", server.networks
