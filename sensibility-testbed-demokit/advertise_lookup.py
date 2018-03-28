import sys

if len(sys.argv) == 1:
  print """advertise_lookup.py -- 
  resolve keys to values on the Seattle advertise services, 
  or look up public keys.

Usage:
  python advertise_lookup.py ONE_ID [ FURTHER_IDs... ]
  python advertise_lookup.py --key PUBKEY_FILE_NAME [ FURTHER_FILENAMEs....]

Examples:
  python advertise_lookup.py time_server
  python advertise_lookup.py --key servicevessel.publickey
"""
  exit()

from repyportability import *
add_dy_support(locals())

advertise = dy_import_module("advertise.r2py")
experimentlib = dy_import_module("experimentlib.r2py")

# Default to looking up IDs, not public keys
lookup_function = advertise.advertise_lookup

# If we are told to look up keys from files (and not the single 
# string "--key"), use a different lookup function.
if sys.argv[1] == "--key" and len(sys.argv)>2:
  def load_key_and_look_it_up(key_file_name):
    identity = experimentlib.create_identity_from_key_files(key_file_name)
    return experimentlib.lookup_node_locations_by_identity(identity)
  lookup_function = load_key_and_look_it_up
  # Drop "--keys" from argv, this is not a key file name!
  sys.argv.pop(1)


for identifier in sys.argv[1:]:
  try:
    resultslist = lookup_function(identifier)
    print "'" + identifier + "' maps to", len(resultslist), "value(s):", resultslist 
  except Exception, e:
    # Do a blanket except because there are many possible exception types
    print "(Error looking up " + identifier + ": " + repr(e) + ")"

