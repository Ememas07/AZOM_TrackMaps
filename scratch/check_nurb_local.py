import gzip, json

p = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\nurburgring combinedshortb.shtl"
d = json.loads(gzip.decompress(open(p, "rb").read()))

print("TrackDisplayName:", d.get("TrackDisplayName"))
print("ReportedTrackLength:", d.get("ReportedTrackLength"))
print("HasRelativeCarCoordinates:", d.get("HasRelativeCarCoordinates"))
pts = d.get("CarCoordinates", [])
print(f"Total points: {len(pts)}")
for i, pt in enumerate(pts):
    print(f"  pt[{i}]: p={pt.get('p')}, val={pt.get('Value')}")

