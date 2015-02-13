#!/usr/bin/python

import sys, argparse
import time
from pysphere import VIServer


parser = argparse.ArgumentParser()
parser.add_argument("host", help="the hostname of the vsphere server")
parser.add_argument("user", help="username")
parser.add_argument("password", help="password")
args = parser.parse_args()
host = args.host
user = args.user
password = args.password

print 'Connecting to %s.' % host

server = VIServer()
server.connect(host, user, password)

vmlist = server.get_registered_vms()

for vmpath in vmlist:
 vm = server.get_vm_by_path(vmpath)
 if ("backup-machine" not in vm.get_property("name") and "Windows 7" not in vm.get_property("name")) :
  if vm.properties.guest.toolsStatus == 'toolsOk':
   print "Shutting down guest %s." % vm.get_property("name")
   vm.shutdown_guest()
  else:
   print "Suspending %s." % vm.get_property("name")
   vm.suspend(sync_run=False)

runningList = server.get_registered_vms(status='poweredOn')
while len(runningList) > 2:
 print "Waiting for %s machines to shut down" % (len(runningList) - 1)
 runningList = server.get_registered_vms(status='poweredOn')
 time.sleep(10)

server.disconnect()
