import os, re

# Let's inspect the IL or implementation of GetMap in SimHub.Plugins.dll
# We can search for the method definition of GetMap
b = open(r"C:\Program Files (x86)\SimHub\SimHub.Plugins.dll", "rb").read()
pos = 0
matches = []
while True:
    pos = b.find(b"GetMap", pos)
    if pos == -1: break
    matches.append(pos)
    pos += 6

print("GetMap string matches:", matches)
for m in matches:
    print(b[max(0, m-20):m+40])

