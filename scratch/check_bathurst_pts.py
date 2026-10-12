import gzip, json

p = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\bathurst-6144.1.shtl"
d = json.loads(gzip.decompress(open(p, "rb").read()))

coords = d['CarCoordinates']
print(f"Total points: {len(coords)}")
for i in [0, 1, 2, 10, 100, 500, 1000, 1500, 2000, 2500, 3000, len(coords)-2, len(coords)-1]:
    c = coords[i]
    print(f"idx {i:4d}: p={c['p']:.4f}, val={c['Value']}")

