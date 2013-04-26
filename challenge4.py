#!/usr/bin/python

# Challenge 4: Write a script that uses Cloud DNS to create a new A record when passed a
# FQDN and IP address as arguments.
# Worth 1 Point

import pyrax
import pyrax.exceptions
import sys

pyrax.set_credential_file("/Users/jaso4210/.rackspace_cloud_credentials.txt")

dns = pyrax.cloud_dns

domain = raw_input("Enter domain: ")
fqdn = raw_input("Enter FQDN of new A record: ")
ip = raw_input("Enter IP address for new A record: ")
email = raw_input("Enter an email address: ")

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
        "name": domain,
        "data": ip,
        "ttl": 3600}

recs = dom.add_records([a_rec])
print recs
print
