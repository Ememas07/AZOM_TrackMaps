import os

print("=== PITHOUSE TrackData/iracing ===")
p1 = r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing"
for f in os.listdir(p1):
    if 'nurb' in f.lower() or 'nord' in f.lower():
        print(" ", f)

print("\n=== SIMHUB MapRecords ===")
p2 = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords"
for f in os.listdir(p2):
    if 'nurb' in f.lower() or 'nord' in f.lower():
        print(" ", f)

print("\n=== SIMHUB MapRecordsCloud ===")
p3 = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud"
for f in os.listdir(p3):
    if 'nurb' in f.lower() or 'nord' in f.lower():
        print(" ", f)

print("\n=== SIMHUB PersistantTracker ===")
p4 = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\PersistantTracker"
for f in os.listdir(p4):
    if 'nurb' in f.lower() or 'nord' in f.lower():
        print(" ", f)

