#!/usr/bin/python

#Challenge 7: Write a script that will create 2 Cloud Servers and add them
#as nodes to a new Cloud Load Balancer. Worth 3 Points

import pyrax
import time


pyrax.set_credential_file("/Users/hal/.rackspace_cloud_credentials.txt")

cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers

#find ubuntu 12.04 image:

ubuntu124_image = [img for img in cs.images.list()
        if "Ubuntu 12.04" in img.name][0]

#select 512MB flavor:

flavor_512 = [flavor for flavor in cs.flavors.list()
        if flavor.ram == 512][0]

#create 2 servers - server1 and server2:

server1 = cs.servers.create("server1", ubuntu124_image, flavor_512)
print "Creating server..."
print ""
print "ID:", server1.id
print "Status:", server1.status
print "Admin password:", server1.adminPass
print "Waiting for network provisioning..."
while not (server1.networks):
        time.sleep(3)
        server1 = cs.servers.get(server1.id)
print "Networks:", server1.networks
print "Server provisioning complete"
print ""
        
        
server2 = cs.servers.create("server2", ubuntu124_image, flavor_512)
print "Creating server..."
print ""
print "ID:", server2.id
print "Status:", server2.status
print "Admin password:", server2.adminPass
print "Waiting for network provisioning..."
while not (server2.networks):
        time.sleep(3)
        server2 = cs.servers.get(server2.id)
print "Networks:", server2.networks
print "Server provisioning complete"
print ""

print ""
print "Let's load balance these servers. Creating nodes and LB..."

# Get the private network IPs for the servers
server1_ip = server1.networks["private"][0]
server2_ip = server2.networks["private"][0]

# Use the IPs to create the nodes
node1 = clb.Node(address=server1_ip, port=80, condition="ENABLED")
node2 = clb.Node(address=server2_ip, port=80, condition="ENABLED")

# Create the Virtual IP
vip = clb.VirtualIP(type="PUBLIC")

lb = clb.create("test_lb", port=80, protocol="HTTP",
        nodes=[node1, node2], virtual_ips=[vip])

print " Loadbalancer name and ID, respectively:"
print [(lb.name, lb.id) for lb in clb.list()]
