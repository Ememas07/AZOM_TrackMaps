import gzip, json
import numpy as np

# 1. SimHub
p_sim = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\indianapolis 2022 road-Road Course.shtl"
d_sim = json.loads(gzip.decompress(open(p_sim, 'rb').read()))
sim_pts = [pt['Value'] for pt in d_sim['CarCoordinates']]
sx = np.array([p[0] for p in sim_pts])
sz = np.array([p[2] for p in sim_pts])

# 2. mztrack
p_mz = r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"
d_mz = json.load(open(p_mz))
mz_pts = d_mz['sectors'][0]['data']
mx = np.array([p[0] * 0.0001 for p in mz_pts])
my = np.array([p[1] * 0.0001 for p in mz_pts])

# Compute signed area (winding order):
# 2D polygon area = 0.5 * sum(x_i * y_{i+1} - x_{i+1} * y_i)
# Positive = CCW, Negative = CW in standard (X right, Y up) coordinates.
area_sim = 0.5 * np.sum(sx[:-1] * sz[1:] - sx[1:] * sz[:-1])
area_mz = 0.5 * np.sum(mx[:-1] * my[1:] - mx[1:] * my[:-1])

print(f"SimHub (sx, sz) signed area: {area_sim:.1f}")
print(f"mztrack (mx, my) signed area: {area_mz:.6f}")

# If screen has X right, Y down (standard Canvas / Qt):
# In screen coords, Y_screen = my.
# What is the winding order of mztrack on screen?
print("mztrack winding on screen (X right, Y down):", "CLOCKWISE" if area_mz > 0 else "COUNTER-CLOCKWISE")

# What is the winding order of SimHub on screen if X_screen = sx, Y_screen = -sz?
sz_screen = -sz
area_sim_screen = 0.5 * np.sum(sx[:-1] * sz_screen[1:] - sx[1:] * sz_screen[:-1])
print("SimHub winding on screen (X=sx, Y=-sz):", "CLOCKWISE" if area_sim_screen > 0 else "COUNTER-CLOCKWISE")

# What is the winding order of SimHub on screen if X_screen = sx, Y_screen = +sz?
area_sim_raw = 0.5 * np.sum(sx[:-1] * sz[1:] - sx[1:] * sz[:-1])
print("SimHub winding on screen (X=sx, Y=+sz):", "CLOCKWISE" if area_sim_raw > 0 else "COUNTER-CLOCKWISE")

