import os, sys

# Let's inspect ICarsReader.dll
p = r"C:\Program Files (x86)\SimHub\ICarsReader.dll"
b = open(p, "rb").read()

# Let's find strings in ICarsReader.dll
print(f"ICarsReader.dll size: {len(b)}")

# Let's search for Yaw, Pitch, Roll, North, Dist, etc.
import re
matches = re.findall(b"[A-Za-z0-9_]{4,}", b)
for m in matches:
    s = m.decode('ascii', errors='ignore')
    if any(k in s.lower() for k in ['yaw', 'north', 'coordinate', 'persistant', 'tracker', 'addpoint']):
        print("Match:", s)

