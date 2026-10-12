import re

# Let's inspect GameReaderCommon.dll
p = r"C:\Program Files (x86)\SimHub\GameReaderCommon.dll"
b = open(p, "rb").read()
print("GameReaderCommon.dll size:", len(b))

# Find properties on StatusDataBase
props = re.findall(rb"get_([A-Za-z0-9_]+)", b)
prop_names = set(p.decode('ascii', errors='ignore') for p in props)
coords_props = [p for p in prop_names if 'coord' in p.lower() or 'car' in p.lower() or 'track' in p.lower() or 'relative' in p.lower()]
print("Matching props:", sorted(coords_props))

