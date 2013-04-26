#!/usr/bin/python

# challenge6 Write a script
# that creates a CDN-enabled container in
# Cloud Files. Worth 1 Point

import pyrax

pyrax.set_credential_file("~/.rackspace_cloud_credentials.txt")

cf = pyrax.cloudfiles

print "Let's create a CDN enabled CloudFiles container."
name = raw_input("Name your container: ")

cont = cf.create_container(name)
print "Container created: ", cont.name

cf.make_container_public(cont.name, ttl=1800)

