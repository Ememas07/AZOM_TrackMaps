import gzip, json
import numpy as np

# Load SimHub map for Bathurst
p_sim = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\bathurst-6144.1.shtl"
d_sim = json.loads(gzip.decompress(open(p_sim, "rb").read()))
sim_coords = [pt['Value'] for pt in d_sim['CarCoordinates']]
sx = np.array([c[0] for c in sim_coords])
sy = np.array([c[1] for c in sim_coords])
sz = np.array([c[2] for c in sim_coords])

# TrackMapTransform.FromBounds logic:
# Percentile trim 1.0%
xs_sorted = sorted(sx)
zs_sorted = sorted(sz)
def percentile(s, pct):
    i = int(round(pct / 100.0 * (len(s) - 1)))
    return s[i]

min_x = percentile(xs_sorted, 1.0)
max_x = percentile(xs_sorted, 99.0)
min_z = percentile(zs_sorted, 1.0)
max_z = percentile(zs_sorted, 99.0)

print(f"Bathurst SimHub trimmed bounds: X=[{min_x:.1f}, {max_x:.1f}], Z=[{min_z:.1f}, {max_z:.1f}]")

FieldX = 1048576.0 # 2^20
BoundsCenterX = 0x480000 # 4718592
BoundsCenterZ = 0x800000 # 8388608
BoundsFill = 0.9

ext = max(max_x - min_x, max_z - min_z)
s = BoundsFill * FieldX / ext
scale_x = s
scale_z = 16.0 * s
center_x = round(BoundsCenterX - s * (min_x + max_x) / 2.0)
center_z = round(BoundsCenterZ - 16.0 * s * (min_z + max_z) / 2.0)

print(f"ScaleX={scale_x:.1f}, ScaleZ={scale_z:.1f}, CenterX={center_x}, CenterZ={center_z}")

# Now let's calculate fx and fz for car at start/finish:
start_x, start_z = sx[0], sz[0]
fx_start = center_x + round(start_x * scale_x)
fz_start = center_z + round(start_z * scale_z)
print(f"Start (0%): sx={start_x:.1f}, sz={start_z:.1f} -> fx={fx_start}, fz={fz_start}")

# Now let's compare with PitHouse mztrack for Bathurst:
p_mz = r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\bathurst.mztrack"
d_mz = json.load(open(p_mz))
mz_pts = d_mz['sectors'][0]['data']
print(f"mztrack start: {mz_pts[0]}")
print(f"mztrack middle: {mz_pts[len(mz_pts)//2]}")
print(f"mztrack metadata: x_max={d_mz.get('x_max')}, y_max={d_mz.get('y_max')}")

