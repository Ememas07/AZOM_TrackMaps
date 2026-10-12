import gzip, json
import numpy as np

# Load SimHub map for Bathurst
p_sim = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\bathurst-6144.1.shtl"
d_sim = json.loads(gzip.decompress(open(p_sim, "rb").read()))
sim_coords = [pt['Value'] for pt in d_sim['CarCoordinates']]
sx = [c[0] for c in sim_coords]
sz = [c[2] for c in sim_coords]

# Load mztrack
p_mz = r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\bathurst.mztrack"
d_mz = json.load(open(p_mz))
mz_pts = d_mz['sectors'][0]['data']

print("Bathurst first 10 steps:")
for i in range(0, 50, 5):
    print(f"  SimHub idx {i:2d}: x={sx[i]:7.1f}, z={sz[i]:7.1f}")
for i in range(0, 50, 5):
    print(f"  mztrack idx {i:2d}: x={mz_pts[i][0]*0.0001:7.4f}, y={mz_pts[i][1]*0.0001:7.4f}")

