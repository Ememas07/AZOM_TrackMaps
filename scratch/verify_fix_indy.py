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

# Current AZOM output:
fx_curr = cx + sx * scale_x
fz_curr = cz + sz * scale_z

# Now let's test PROPOSED FIX: Invert Z axis (sz -> -sz)
# With Z inverted:
# fz = BoundsCenterZ - 16.0 * s * (-z - (-min_z + -max_z)/2)
# which is: scale_z_inv = -16.0 * s, cz_inv = BoundsCenterZ - scale_z_inv * (min_z + max_z)/2
scale_z_inv = -16.0 * s
cz_inv = BoundsCenterZ - scale_z_inv * (min_z + max_z) / 2.0
fz_fixed = cz_inv + sz * scale_z_inv

# Let's compare normalized 0..1 coordinates:
# The wheel normalizes X by low 20 bits: (fx - (BoundsCenterX - 0.5*FieldX)) / FieldX
# and Z by full 24 bits: fz / 2^24
norm_x_curr = (fx_curr - (BoundsCenterX - 0.5 * FieldX)) / FieldX
norm_z_curr = fz_curr / (1 << 24)
norm_z_fixed = fz_fixed / (1 << 24)

# In mztrack: mx is 0..1 (X), my is 0..1 (Y on screen, top-down!)
# On screen, top-down Y = 1 - norm_z!
# Let's check correlation with mztrack:
# In mztrack: resampled to same length
N = len(sx)
mz_idx = np.linspace(0, len(mx)-1, N).astype(int)
target_mx = mx[mz_idx]
target_my = my[mz_idx]

print("Current AZOM vs mztrack:")
print("  Correlation X:", np.corrcoef(norm_x_curr, target_mx)[0, 1])
# mztrack Y is top-down (0 at top, 1 at bottom). Wheel Z is bottom-up (0 at bottom, 1 at top).
# So target_my should correspond to 1 - norm_z.
screen_y_curr = 1.0 - norm_z_curr
screen_y_fixed = 1.0 - norm_z_fixed

print("  Current screen Y correlation with mztrack Y:", np.corrcoef(screen_y_curr, target_my)[0, 1])
print("  Fixed screen Y correlation with mztrack Y:  ", np.corrcoef(screen_y_fixed, target_my)[0, 1])

# Check distance error between fixed dot and mztrack track line!
err_curr = np.mean(np.sqrt((norm_x_curr - target_mx)**2 + (screen_y_curr - target_my)**2))
err_fixed = np.mean(np.sqrt((norm_x_curr - target_mx)**2 + (screen_y_fixed - target_my)**2))
print(f"Mean tracking error (0..1 screen units): Current = {err_curr:.4f}, Fixed = {err_fixed:.4f}")

