# Network reservation simulation

import sys
import json

#Helper methods
def printReserve(stepCount, node1, node2, time, isSuccessful):
   msg = "{}. reserve: {} <-> {} st: {} - {}".format(stepCount, node1, node2, time, successText if isSuccessful else failureText)
   print(msg)

def printFree(stepCount, node1, node2, time):
   msg = "{}. free: {} <-> {} st: {}".format(stepCount, node1, node2, time)
   print(msg)

#Read file
with open(sys.argv[1], 'r') as f:
   fileContent = f.read()
file = json.loads(fileContent)
#print("File read successfully")

#Extract
endPoints = file['end-points']
switches = file['switches']
links = file['links']
circuits = file['possible-circuits']
simulation = file['simulation']['demands']
simTime = file['simulation']['duration']

#Prepare
step = 1
successText = "successful"
failureText = "fail"
states = []
finals = []

#Simulate
for i in simulation:
   node1 = i["end-points"][0]
   node2 = i["end-points"][1]

   circuit = []
   for j in circuits:
      if j[0] == node1 and j[-1] == node2:
         circuit = j

   slinks = []
   for j in range(len(circuit) - 1):
      for k in links:
         if k["points"][0] == circuit[j] and k["points"][1] == circuit[j + 1]:
            slinks.append(True)
         else:
            slinks.append(False)
      states.append(slinks)
      slinks = []
      temp = False

   for j in range(len(states[0])):
      for k in (0, len(states)-1):
         temp = states[k][j] or temp
      slinks.append(temp)
      temp = False

   states = slinks
   finals.append(states)
   states = []
   step += 1

step = 1

printReserve(step, simulation[0]["end-points"][0], simulation[0]["end-points"][1], simulation[0]["start-time"], True)

endTimes = []
endTimes.append(simulation[0]["end-time"])

for i in range(1, len(simulation)):
   #Free
   if len(endTimes) > 0:
      if simulation[i]["start-time"] > min(endTimes):
         step += 1
         end = endTimes.index(min(endTimes))
         printFree(step, simulation[end]["end-points"][0], simulation[end]["end-points"][1], simulation[end]["end-time"])
         endTimes[end] = sys.maxsize
         for j in range (0, len(finals[end])):
            finals[end][j] = False

   #Reserve
   success = True
   for j in range(i):
      for k in range(len(finals[0])):
         if (finals[i][k] == True) and (finals[j][k] == True):
            success = False
   
   step += 1
   printReserve(step, simulation[i]["end-points"][0], simulation[i]["end-points"][1], simulation[i]["start-time"], success)
   if not success:
      for j in range(len(finals[i])):
         finals[i][j] = False

#Free
temp = False
for i in range(len(finals)):
   for j in finals[i]:
      temp += j
   if temp and (simulation[i]["end-time"] <= simTime):
      step += 1
      printFree(step, simulation[i]["end-points"][0], simulation[i]["end-points"][1], simulation[i]["end-time"])

#print("Completed")