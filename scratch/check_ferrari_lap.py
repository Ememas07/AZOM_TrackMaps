import gzip, json

p = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\PersistantTracker\nurburgring combinedshortb\ferrari296gt3\00.07.55.3630_20261010_123336.tm.gz"
d = json.loads(gzip.decompress(open(p, "rb").read()))

coords = d.get('CarCoordinates', [])
print("Total CarCoordinates:", len(coords))
if coords:
    print("pt[0]:", coords[0])
    print("pt[10]:", coords[10])
    print("pt[-1]:", coords[-1])

