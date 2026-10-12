import gzip, json
import numpy as np

# Load Indianapolis
p_sim = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\indianapolis 2022 road-Road Course.shtl"
d_sim = json.loads(gzip.decompress(open(p_sim, "rb").read()))
sim_coords = [pt['Value'] for pt in d_sim['CarCoordinates']]
sx = np.array([c[0] for c in sim_coords])
sz = np.array([c[2] for c in sim_coords])

# Load PitHouse mztrack
p_mz = r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"
d_mz = json.load(open(p_mz))
mz_pts = d_mz['sectors'][0]['data']
mx = np.array([p[0] * 0.0001 for p in mz_pts])
my = np.array([p[1] * 0.0001 for p in mz_pts])

# Current AZOM FromBounds:
min_x, max_x = sx.min(), sx.max()
min_z, max_z = sz.min(), sz.max()
ext = max(max_x - min_x, max_z - min_z)
FieldX = 1048576.0 # 2^20
BoundsCenterX = 0x480000 # 4718592
BoundsCenterZ = 0x800000 # 8388608
BoundsFill = 0.9

s = BoundsFill * FieldX / ext
scale_x = s
scale_z = 16.0 * s
cx = BoundsCenterX - s * (min_x + max_x) / 2.0
cz = BoundsCenterZ - 16.0 * s * (min_z + max_z) / 2.0

fx_curr = cx + sx * scale_x
fz_curr = cz + sz * scale_z

# Let's see: How does the wheel map fx and fz to screen pixels?
# In Map.qml (lines 125-127):
# canvas_width = width * 0.75
# offset = (width - canvas_width) / 2
# ctx.lineTo(pt.x * canvas_width + offset, pt.y * canvas_width + offset)
#
# Notice that pt.x and pt.y in mztrack are in 0..1!
# In mztrack:
# min(mx) = 0.0, max(mx) = 1.0
# min(my) = 0.0, max(my) = 1.0
# BUT d_mz has:
# x_max = 0.47475, y_max = 1.0!
# WAIT! Does the wheel multiply mx by x_max?!
# Let's check!
print("mztrack metadata: x_max =", d_mz['x_max'], "y_max =", d_mz['y_max'])

# Compare normalized SimHub vs mztrack at 10 lap points:
N = 10
for i in range(0, len(sx), len(sx)//N):
    # SimHub normalized:
    nx = (sx[i] - min_x) / (max_x - min_x)
    nz = (sz[i] - min_z) / (max_z - min_z)
    
    # mztrack at same lap pct:
    mz_i = int(i / len(sx) * len(mx))
    if mz_i >= len(mx): mz_i = len(mx) - 1
    
    print(f"pct={i/len(sx)*100:4.1f}%: SimHub (nx={nx:.3f}, nz={nz:.3f}) | mztrack (mx={mx[mz_i]:.3f}, my={my[mz_i]:.3f})")

