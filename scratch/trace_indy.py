import gzip, json
import numpy as np

# 1. SimHub
p_sim = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\indianapolis 2022 road-Road Course.shtl"
d_sim = json.loads(gzip.decompress(open(p_sim, 'rb').read()))
sim_pts = [pt['Value'] for pt in d_sim['CarCoordinates']]
sim_x = [p[0] for p in sim_pts]
sim_z = [p[2] for p in sim_pts]

# 2. mztrack
p_mz = r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"
d_mz = json.load(open(p_mz))
mz_pts = d_mz['sectors'][0]['data']
mz_x = [p[0] * 0.0001 for p in mz_pts]
mz_y = [p[1] * 0.0001 for p in mz_pts]

print(f"SimHub has {len(sim_pts)} pts. Start: x={sim_x[0]:.2f}, z={sim_z[0]:.2f}")
print(f"mztrack has {len(mz_pts)} pts. Start: x={mz_x[0]:.4f}, y={mz_y[0]:.4f}")

# First 100 points
print("\nSimHub first 10 steps:")
for i in range(0, 50, 5):
    print(f"  idx {i:3d}: x={sim_x[i]:7.2f}, z={sim_z[i]:7.2f}")

print("\nmztrack first 10 steps:")
for i in range(0, 50, 5):
    print(f"  idx {i:3d}: x={mz_x[i]:7.4f}, y={mz_y[i]:7.4f}")

