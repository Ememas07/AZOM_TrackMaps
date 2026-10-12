import os, re

p = r"C:\Program Files (x86)\SimHub\SimHub.Plugins.dll"
b = open(p, "rb").read()

print("SimHub.Plugins.dll size:", len(b))

# Search for PersistantTracker in strings
matches = re.findall(b"[A-Za-z0-9_]{4,}", b)
pt_strings = [m.decode('ascii', errors='ignore') for m in matches if 'persistanttracker' in m.decode('ascii', errors='ignore').lower()]
print("PersistantTracker strings:", len(pt_strings))
for s in sorted(set(pt_strings))[:30]:
    print(" ", s)

