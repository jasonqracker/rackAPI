# Challenge 10: Write an application that will:
# - Create 2 servers, supplying a ssh key to be installed at /root/.ssh/authorized_keys.
# - Create a load balancer
# - Add the 2 new servers to the LB
# - Set up LB monitor and custom error page. 
# - Create a DNS record based on a FQDN for the LB VIP. 
# - Write the error page html to a file in cloud files for backup.
# Whew! That one is worth 8 points!
#!/usr/bin/python

import pyrax, time, sys, os

#set path to crednetial file:
pyrax.set_credential_file("~/.rackspace_cloud_credentials.txt")

cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
dns = pyrax.cloud_dns

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
#find ubuntu 12.04 image:

ubuntu124_image = [img for img in cs.images.list()
        if "Ubuntu 12.04" in img.name][0]

#select 512MB flavor:

flavor_512 = [flavor for flavor in cs.flavors.list()
        if flavor.ram == 512][0]

#create 2 servers - server1 and server2:

server1 = cs.servers.create("server1", ubuntu124_image, flavor_512)
print "=" * 40
print "Provisioning Server Name: ", server1.name
print "Server ID:", server1.id
print "Server Status:", server1.status
print "Admin password:", server1.adminPass
print "Waiting for network provisioning..."
while not (server1.networks):
    time.sleep(15)
    server1 = cs.servers.get(server1.id)
print "Public Network Address(es) provisioned:", str(server1.networks["public"])
print "Private Network Address(es) provisioned: ", str(server1.networks["private"])
print "'",server1.name,"' successfully provisioned."   
print "=" * 40
print ""
        
        
server2 = cs.servers.create("server2", ubuntu124_image, flavor_512)
print "=" * 40
print "Provisioning Server Name: ", server2.name
print "Server ID:", server2.id
print "Server Status:", server2.status
print "Admin password:", server2.adminPass
print "Waiting for network provisioning..."
while not (server2.networks):
    time.sleep(15)
    server2= cs.servers.get(server2.id)
print "Public Network Address(es) provisioned:", str(server2.networks["public"])
print "Private Network Address(es) provisioned: ", str(server2.networks["private"])
print "'",server2.name,"' successfully provisioned."   
print "=" * 40
print ""

# create LB:

print "Creating loadbalancer..."

# Obtain the servers' private IPs: 
server1_ip = server1.networks["private"][0]
server2_ip = server2.networks["private"][0]

# Create the nodes
node1 = clb.Node(address=server1_ip, port=80, condition="ENABLED")
node2 = clb.Node(address=server2_ip, port=80, condition="ENABLED")

# Create a VIP:
# Create the Virtual IP
vip = clb.VirtualIP(type="PUBLIC")

lb = clb.create("test_lb", port=80, protocol="HTTP",
        nodes=[node1, node2], virtual_ips=[vip])

vipAdd = lb.virtual_ips[0].address
#print vipAdd


#wait
while str(lb.status) != "ACTIVE":
    time.sleep(10)
    lb = clb.get(lb.id)
    

print " Cloud loadbalancer provisioned:"
print "=" * 40
print [(lb.name, lb.id) for lb in clb.list()]
print "Virtual IP: %s" % vipAdd
print "=" * 40
print
print "Provisioning LB monitor and custom error page..."
lb.add_health_monitor(type="HTTP", delay=10, timeout=10,
        attemptsBeforeDeactivation=3, path="/",
        statusRegex="^[234][0-9][0-9]$",
        bodyRegex=".* testing .*",
        hostHeader="apichallenge.com")

#wait moar for all teh thingz
lb = clb.get(lb.id)
while str(lb.status) != "ACTIVE":
    time.sleep(10)
    lb = clb.get(lb.id)

html = "<html><body>Something is afoot at the CircleK!</body></html>"
lb.set_error_page(html)
print "=" * 40
print "Custom error page: "
print html
print "=" * 40

print "HTTP monitor and custom error page provisioned, let's create a DNS record for your new VIP."
print
domain = raw_input("Enter domain: ")
fqdn = raw_input("Enter FQDN of new A record (Must not exist): ")



try:
    dom = dns.find(name=domain)
except pyrax.exceptions.NotFound:
    answer = raw_input("The domain '%s' was not found. Do you want to create it? [y/n]" % domain)
    if not answer.lower().startswith("y"):
        sys.exit()
    try:
        dom = dns.create(name=domain, emailAddress="sample@example.edu",
                ttl=900, comment="sample domain")
    except pyrax.exceptions.DomainCreationFailed as e:
        print "Domain creation failed:", e
    print "Domain created:", dom
    print

# record contents
a_rec = {"type": "A",
        "name": fqdn,
        "data": vipAdd,
        "ttl": 3600}

recs = dom.add_records([a_rec])
print "=" * 40
print "The following DNS record has been created: "
print recs
print "=" * 40



