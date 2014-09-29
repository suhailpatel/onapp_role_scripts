#!/usr/bin/python

# Import OnApp role Script
# Written by Suhail Patel <suhail@onapp.com>
# Copyright 2014 - OnApp Limited 

from __future__ import print_function

import sys, argparse
import urllib, urllib2, base64
import json
import os


def import_role(args):
  try:
    print("> Parsing role file")
    file_response = parse_role_file(args.role_file)
  except Exception as e:
    sys.exit("! Failed to load role due to an error: %s" % e)

  try:
    label = args.role_label
    print("> Creating role with label '%s'" % label)
    base_response = create_role(args, file_response, label)
    role_response = json.load(base_response, encoding="utf-8")
  except Exception as e:
    sys.exit("! Failed to create role due to an error: %s" % e)

  try:
    role_id = role_response['role']['id']
  except Exception as e:
    sys.exit("! Failed to create role due to an error: %s" % e)

  print("""
Your role has been imported successfully! 
Check it out at %s/roles/%d.json""" % (args.host, role_id))


def parse_role_file(filename):
  handler = open(filename, 'r')
  data = json.load(handler)
  handler.close()

  return data


def create_role(args, role, label):
  permissions = [p['permission']['id'] for p in role['permissions']]

  values = {
    'role': {
      'label': label,
      'permission_ids': permissions
    }
  }

  url = "%s/roles.json" % args.host
  auth = base64.encodestring('%s:%s' % (args.user, args.password))
  # Remove new line character because it's not required
  if auth[-1] == "\n": auth = auth[:-1]

  print("> - POST request to %s" % url)
  return post_request(url, auth, values)


def post_request(url, auth, values):
  request = urllib2.Request(url, json.dumps(values))
  request.add_header("Authorization", "Basic %s" % auth)
  request.add_header("Accept", "application/json")
  request.add_header("Content-type", "application/json")

  return urllib2.urlopen(request)


if __name__ == '__main__':
  print("""OnApp Role Import Script - Version 0.1
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

  parser = argparse.ArgumentParser(description='Export your OnApp Roles quickly and easily to use with the OnApp Import role Script.')
  parser.add_argument('host', help='Hostname of the cloud (eg. http://myonapp.cloud.com)')
  parser.add_argument('user', help='OnApp Cloud Username (or email address if using API token)')
  parser.add_argument('password', help='OnApp Cloud Password (or API token)')
  parser.add_argument('role_file', help='Role file to import')
  parser.add_argument('role_label', help='Label to give to the new role')

  args = parser.parse_args()
  import_role(args)