#!/usr/bin/python

# Challenge 8: Write a script that will create a static webpage served out of
# Cloud Files. The script must create a new container, cdn enable it, enable
# it to serve an index file, create an index file object, upload the object
# to the container, and create a CNAME record pointing to the CDN URL of the
# container. Worth 3 Points

import pyrax
import os
import sys
import pyrax.exceptions as exc

pyrax.set_credential_file("/Users/hal/.rackspace_cloud_credentials.txt")

cf = pyrax.cloudfiles
dns = pyrax.cloud_dns

print "Let's create a CDN enabled CloudFiles container."
name = raw_input("Name your container: ")

cont = cf.create_container(name)
print "Container created: ", cont.name

cf.make_container_public(cont.name, ttl=1800)

print "cdn base URI: ", cont.cdn_uri

index = open('index.htm', 'w')
index.write('Hello, World!')
index.close()

fname = os.path.basename('index.htm')
print
print "Uploading: %s" % fname

cf.upload_file(cont, fname, content_type="text/text")

fobj = cont.get_object(fname)
obj_uri = cont.cdn_uri + "/" + fobj.name

print ""
print "Stored object name: ", fobj
print "Stored object URI: ", obj_uri
print
print "File contents: "
print "- " * 24
print fobj.get()
print "- " * 24

print "Let's create a CNAME record for this container."
domain = raw_input("Enter a domain from your cloud DNS: ")
try:
    dom = dns.find(name=domain)
except exc.NotFound:
    answer = raw_input("The domain '%s' was not found. Do you want to create "
            "it? [y/n]" % domain)
    if not answer.lower().startswith("y"):
        sys.exit()
    try:
        dom = dns.create(name=domain, emailAddress="sample@example.edu",
                ttl=900, comment="sample domain")
    except exc.DomainCreationFailed as e:
        print "Domain creation failed:", e
        print
        sys.exit()
    print "Domain created:", dom
    print

sub = raw_input("Enter the CNAME content (subdomain): ")
email = raw_input("Enter an email address: ")
target = cont.cdn_uri[7:]
fqdn = sub + "." + domain

cname = {"type": "CNAME",
         "name" : fqdn,
         "data" : target,
         "ttl" : 600}

recs = dom.add_records([cname])

print recs



