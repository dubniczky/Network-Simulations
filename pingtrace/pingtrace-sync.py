#coding: utf-8

import sys
import json
import platform
import subprocess
from datetime import date

#Read file
fileName = sys.argv[1]
with open(fileName, 'r') as f:
   fileContent = f.readlines()
selectedLines = fileContent

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

#Pinging
for address in addresses:
   process = subprocess.run(['ping', address], stdout=subprocess.PIPE)
   entry = {}
   entry["target"] = address
   entry["output"] = process.stdout.decode()
   ping["pings"].append(entry)
   print("Pinging done")

file = open("ping.json","w")
file.write(json.dumps(ping))
file.close()

#Tracing
for address in addresses:
   process = subprocess.run(['tracert', address], stdout=subprocess.PIPE)
   entry = {}
   entry["target"] = address
   entry["output"] = process.stdout.decode()
   traceroute["traces"].append(entry)
   print("Tracing done")

file = open("traceroute.json","w")
file.write(json.dumps(traceroute))
file.close()

print("Completed")


#win
#subprocess.run(['tracert', "google.com"], shell=True)

#lin
#subprocess.run(['traceroute', "google.com"])