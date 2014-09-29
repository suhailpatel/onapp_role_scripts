#!/usr/bin/python

# Export OnApp Role Script
# Written by Suhail Patel <suhail@onapp.com>
# Copyright 2014 - OnApp Limited 

from __future__ import print_function

import sys, argparse
import urllib2, base64
import json
import os


def export_role(args):
  try:
    print("> Attempting to grab role")
    response = request_role(args)
  except Exception as e:
    sys.exit("! Failed to grab role from server due to an error: %s" % e)

  try:
    print("> Parsing Role JSON")
    role = json.load(response, encoding="utf-8")
  except Exception as e:
    sys.exit("! Could not load JSON role due to an error: %s" % e)

  try:
    role_export = parse_role(role)

    filename = '%s.role.json' % args.role
    if os.path.isfile(filename):
      raise Exception("File '%s' already exists" % filename)

    print("> Saving role to file '%s'" % filename)
    save_role(role_export, filename)
  except Exception as e:
    sys.exit("! Could not export role due to an error: %s" % e)

  print("Your role has been exported to '%s'!" % filename)


def parse_role(role):
  role = role['role']
  print("> Processing Role '%s'" % role['label'])

  return {
    'label': role['label'],
    'permissions': role['permissions']
  }

def save_role(role_export, filename):
  with open(filename, 'w') as out:
    json.dump(role_export, out, encoding="utf-8")


def request_role(args):
  url = "%s/roles/%d.json" % (args.host, args.role)
  print("> - Connecting to %s" % url)

  auth = base64.encodestring('%s:%s' % (args.user, args.password))
  # Remove new line character because it's not required
  if auth[-1] == "\n": auth = auth[:-1]

  request = urllib2.Request(url)
  request.add_header("Authorization", "Basic %s" % auth)   
  return urllib2.urlopen(request)


if __name__ == '__main__':
  print("""OnApp Role Export Script - Version 0.1
Developed by Suhail Patel <suhail@onapp.com>
Copyright OnApp Limited 2014

IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN 
WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO 
MODIFIES AND/OR CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE 
LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, 
INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR 
INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS 
OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED 
BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE 
WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY 
HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
""")

  parser = argparse.ArgumentParser(description='Export your OnApp roles quickly and easily to use with the OnApp Import role Script.')
  parser.add_argument('host', help='Hostname of the cloud (eg. http://myonappcloud.test.com)')
  parser.add_argument('user', help='OnApp Cloud Username (or email if using API token')
  parser.add_argument('password', help='OnApp Cloud Password (or API token)')
  parser.add_argument('role', type=int, help='role ID in the URL bar of the role you want to export (eg. http://myonappcloud.test.com/roles/9 means an ID of 9)')

  args = parser.parse_args()
  export_role(args)