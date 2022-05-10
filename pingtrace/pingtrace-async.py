#coding: utf-8
#author: Nagy Richárd Antal
#neptun: V7BFDU

import sys
import json
import platform
import subprocess
from subprocess import Popen
from datetime import date

#Read file
fileName = sys.argv[1]
with open(fileName, 'r') as f:
   fileContent = f.readlines()
selectedLines = fileContent

#Convert entries
addresses = []
for i in selectedLines:
   addresses.append(i.split(",")[1][0:-1]) #remove line break

#Prepare output objects
ping = {}
traceroute = {}
ping["date"] = traceroute["date"] = date.today().strftime("%Y%m%d")
ping["system"] = traceroute["system"] = platform.system().lower()
ping["pings"] = []
traceroute["traces"] = []

#Start processes
pingProcesses = []
traceProcesses = []
for address in addresses:
   pingProcesses.append(Popen(['ping', address], stdout=subprocess.PIPE))
   traceProcesses.append(Popen(['tracert', address, '-h', '30', '-w', '5000'], stdout=subprocess.PIPE))

#Wait for pings
for i in range(len(pingProcesses)):
   entry = {}
   entry["target"] = addresses[i]
   entry["output"] = pingProcesses[i].communicate()[0].decode("utf-8")
   ping["pings"].append(entry)
   print("Ping %i complete" % (i+1))

#Wait for traces
for i in range(len(traceProcesses)):
   entry = {}
   entry["target"] = addresses[i]
   entry["output"] = traceProcesses[i].communicate()[0].decode("utf-8")
   traceroute["traces"].append(entry)
   print("Trace %i complete" % (i+1))

#Write files
print("Saving operations...")
file = open("ping.json","w")
file.write(json.dumps(ping))
file.close()

file = open("traceroute.json","w")
file.write(json.dumps(traceroute))
file.close()

print("Completed")