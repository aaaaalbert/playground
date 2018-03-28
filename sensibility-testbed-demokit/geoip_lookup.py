import sys

if len(sys.argv) < 2:
  print """geoip_lookup.py ---
  "resolve" IP addresses to approximate geo-information

Usage:
  python geoip_lookup.py IP [ GEOIP_SERVER ]

where IP is the address to resolve, and
GEOIP_SERVER is an optional GeoIP server to contact.

(The Seattle network testbed provides two GeoIP servers,
http://geoipserver.poly.edu:12679 and http://geoipserver2.poly.edu:12679 )
"""
  sys.exit(0)

from repyportability import *
add_dy_support(locals())

geoip_client = dy_import_module("geoip_client.r2py")

try:
  geoipserver = sys.argv[2]
  geoip_client.geoip_init_client(url=geoipserver)
except IndexError:
  geoip_client.geoip_init_client()


ip = sys.argv[1]

print "Address", ip, "is located in", geoip_client.geoip_record_by_addr(ip)
