#!/usr/bin/python

#Challenge 1: Write a script that builds three 512 MB Cloud Servers that following a
#similar naming convention. (ie., web1, web2, web3) and returns
#the IP and login credentials for each server. Use any image you want. Worth 1 point

import pyrax
import time

#set path to crednetial file:
pyrax.set_credential_file("~/.rackspace_cloud_credentials.txt")

cs = pyrax.cloudservers

#find ubuntu 12.04 image:

ubuntu124_image = [img for img in cs.images.list()
        if "Ubuntu 12.04" in img.name][0]

#select 512MB flavor:

flavor_512 = [flavor for flavor in cs.flavors.list()
        if flavor.ram == 512][0]

#create 3 servers - web1, web2 and web3:

n = 1
while n <4:
    name = "web" + str(n)
    server  = cs.servers.create(name, ubuntu124_image.id, flavor_512.id)
    print "=" * 40
    print "Provisioning Server Name: ", server.name
    print "Server ID:", server.id
    print "Server Status:", server.status
    print "Admin password:", server.adminPass
    print "Waiting for network provisioning..."
    while not (server.networks):
        time.sleep(15)
        server = cs.servers.get(server.id)
    print "Public Network Address(es) provisioned:", str(server.networks["public"])
    print "Private Network Address(es) provisioned: ", str(server.networks["private"])
    print "'",server.name,"' successfully provisioned."   
    print "=" * 40
    n += 1
    
