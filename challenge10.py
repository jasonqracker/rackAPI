# Challenge 10: Write an application that will:
# - Create 2 servers, supplying a ssh key to be installed at /root/.ssh/authorized_keys.
# - Create a load balancer
# - Add the 2 new servers to the LB
# - Set up LB monitor and custom error page. 
# - Create a DNS record based on a FQDN for the LB VIP. 
# - Write the error page html to a file in cloud files for backup.
# Whew! That one is worth 8 points!

import pyrax
import time
import sys
import os

#set path to crednetial file:
pyrax.set_credential_file("/Users/jaso4210/.rackspace_cloud_credentials.txt")

cs = pyrax.cloudservers

#find ubuntu 12.04 image:

ubuntu124_image = [img for img in cs.images.list()
        if "Ubuntu 12.04" in img.name][0]

#select 512MB flavor:

flavor_512 = [flavor for flavor in cs.flavors.list()
        if flavor.ram == 512][0]


# read ~/.ssh/id_rsa.pub:
#content = open('~/.ssh/id_rsa.pub', 'r')
sshPath = os.path.expanduser("~/.ssh/id_rsa.pub")
with open(sshPath, "r") as root_ssh_auth_keys:
        content=root_ssh_auth_keys.read().replace('\n', '')
files = {"/root/.ssh/authorized_keys" : content}

#create 2 servers:

n = 1
servers = {}
while n < 3:
    name = "chal9Srv" + str(n)
    servers[name]  = cs.servers.create(name, ubuntu124_image.id, flavor_512.id, files=files)
    print "=" * 40
    print "Provisioning Server Name: ", servers[name].name
    print "Server ID:", servers[name].id
    print "Server Status:", servers[name].status
    print "Admin password:", servers[name].adminPass
    print "Waiting for network provisioning..."
    while not (servers[name].networks):
        time.sleep(15)
        servers[name] = cs.servers.get(servers[name].id)
    print "Public Network Address(es) provisioned:", str(servers[name].networks["public"])
    print "Private Network Address(es) provisioned: ", str(servers[name].networks["private"])
    print "'",servers[name].name,"' successfully provisioned."   
    print "=" * 40
    n += 1

# create LB:

print "Creating loadbalancer..."

# Obtain the servers' private IPs: 
server1_ip = servers['chal9Srv1'].networks["private"][0]
server2_ip = servers['chal9Srv2'].networks["private"][0]

# Create the nodes
node1 = clb.Node(address=server1_ip, port=80, condition="ENABLED")
node2 = clb.Node(address=server2_ip, port=80, condition="ENABLED")

# Create a VIP:
# Create the Virtual IP
vip = clb.VirtualIP(type="PUBLIC")

lb = clb.create("test_lb", port=80, protocol="HTTP",
        nodes=[node1, node2], virtual_ips=[vip])

print " Cloud loadbalancer provisioned:"
print [(lb.name, lb.id) for lb in clb.list()]

print "Provisioning LB monitor and custom error page..."
lb.add_health_monitor(type="HTTP", delay=10, timeout=10,
        attemptsBeforeDeactivation=3, path="/",
        statusRegex="^[234][0-9][0-9]$",
        bodyRegex=".* testing .*",
        hostHeader="apichallenge.com")

html = "<html><body>Something is afoot at the CircleK!</body></html>"
lb.set_error_page(html)
