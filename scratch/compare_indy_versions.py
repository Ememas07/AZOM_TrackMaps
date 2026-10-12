import json

p1 = r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"
p2 = r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis road.mztrack"

d1 = json.load(open(p1))
d2 = json.load(open(p2))

pts1 = d1['sectors'][0]['data']
pts2 = d2['sectors'][0]['data']

print("indianapolis 2022 road: pts=", len(pts1), "x_max=", d1.get('x_max'), "y_max=", d1.get('y_max'))
print("  pt[0]=", pts1[0], "pt[len/2]=", pts1[len(pts1)//2])

print("indianapolis road: pts=", len(pts2), "x_max=", d2.get('x_max'), "y_max=", d2.get('y_max'))
print("  pt[0]=", pts2[0], "pt[len/2]=", pts2[len(pts2)//2])

