#!/usr/bin/python
#Copyright (c) 2015 James Sun, MapR Technologies
''' 
Utility to be executed on individual data node to turn on UCS disk LED if MapR
detects the disk is sick, possibly before UCS detects it at HW level
'''
import os,sys,json
controller_cmd="/opt/MegaRAID/storcli/storcli64"

j='{"data":['
tmp = os.popen("ls -l /sys/block/sd*/device").readlines()
for line in tmp:
   idchain=line.split('/')[7]
   j = j + '{"disk":"/dev/' + line.split('/')[3] + '","id":"' + idchain.split(':')[2] + '"},'

j=j[:-1]
j=j+ ']}'
a=json.loads(j)

hostname = os.popen("hostname -f").readline().strip()

fd = os.popen("maprcli alarm list -type NODE |grep faileddisk | awk -F\/ '{print $5}' | awk '{print $2}'").readlines()

for h in fd:
 h=h.strip()
 if h == hostname:
  cmd = "maprcli disk list -host " + h + " -output terse | grep Failed_disk | awk '{print $5}'"
  hd = os.popen(cmd).readlines()

  for d in hd:
   d=d.strip()
   cmd = controller_cmd + " -PDList -aALL | grep 'Enclosure Device ID' | uniq | awk -F: '{print $2}'"
   enclosureID=os.popen(cmd).readline().replace(" ","").strip()
   cmd = controller_cmd + " -PDList -aAll | grep Adapter"
   adapterID=os.popen(cmd).readline().replace(" ","").replace("#","").replace("Adapter","").strip()
   adapterID='a' + adapterID
   for entry in a['data']:
      cmd = "" if entry['disk'] in d else "stop"
      led_cmd = "ssh %s %s -PDLocate %s PhysDrv[%s:%s] %s" % (h, controller_cmd, cmd, enclosureID, entry['id'], adapterID)
      opt = os.popen(led_cmd).readlines()
