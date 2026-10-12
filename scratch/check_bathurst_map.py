import gzip, json

p = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\bathurst-6144.1.shtl"
d = json.loads(gzip.decompress(open(p, "rb").read()))

print("TrackDisplayName:", d.get("TrackDisplayName"))
print("ReportedTrackLength:", d.get("ReportedTrackLength"))
print("HasRelativeCarCoordinates:", d.get("HasRelativeCarCoordinates"))
pts = d.get("CarCoordinates", [])
print("CarCoordinates count:", len(pts))
if pts:
    print("pt[0]:", pts[0])
    print("pt[10]:", pts[10])
    print("pt[-1]:", pts[-1])

