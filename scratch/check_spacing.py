import json
import numpy as np

p = r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"
d = json.load(open(p))
pts = d['sectors'][0]['data']

# Let's calculate the cumulative distance along mztrack points:
dists = []
tot = 0.0
for i in range(len(pts)):
    p0 = pts[i-1]
    p1 = pts[i]
    # dx, dy in mztrack
    dx = (p1[0] - p0[0]) * d['x_max'] # scale by aspect ratio
    dy = (p1[1] - p0[1]) * d['y_max']
    seg = np.sqrt(dx*dx + dy*dy)
    tot += seg
    dists.append(tot)

dists = np.array(dists) / tot # 0..1

# Now compare: does index i / len(pts) equal dists[i]?
linear_pct = np.linspace(0, 1, len(pts))
diff = dists - linear_pct
print(f"Max diff between index/len and cumulative distance: {np.max(np.abs(diff)):.4f}")
print("Index 25% dist:", dists[len(pts)//4])
print("Index 50% dist:", dists[len(pts)//2])
print("Index 75% dist:", dists[3*len(pts)//4])

