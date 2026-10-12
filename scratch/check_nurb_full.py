import gzip, json
import numpy as np

p = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\nurburgring combinedshortb-24154.4.shtl"
d = json.loads(gzip.decompress(open(p, "rb").read()))
coords = [c['Value'] for c in d['CarCoordinates']]
sx = [c[0] for c in coords]
sy = [c[1] for c in coords]
sz = [c[2] for c in coords]

def pc(s, p):
    s = sorted(s)
    return s[int(round(p / 100.0 * (len(s) - 1)))]

min_x, max_x = pc(sx, 1.0), pc(sx, 99.0)
min_z, max_z = pc(sz, 1.0), pc(sz, 99.0)
min_y, max_y = min(sy), max(sy)

print(f"Nurburgring Combined bounds: X=[{min_x:.1f}, {max_x:.1f}] (span={max_x-min_x:.1f})")
print(f"                             Z=[{min_z:.1f}, {max_z:.1f}] (span={max_z-min_z:.1f})")
print(f"                             Y=[{min_y:.1f}, {max_y:.1f}] (span={max_y-min_y:.1f})")

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

print(f"ScaleX={scale_x:.2f}, ScaleZ={scale_z:.2f}")
print(f"CenterX={center_x}, CenterZ={center_z}")

# Check field ranges:
fxs = [center_x + round(x * scale_x) for x in sx]
fzs = [center_z + round(z * scale_z) for z in sz]

print(f"fx range: min={min(fxs)}, max={max(fxs)} (limit 0..16777215)")
print(f"fz range: min={min(fzs)}, max={max(fzs)} (limit 0..16777215)")

# Where is GP section vs Nords section?
# GP section is the first ~3.5 km. Let's see the extent of GP section:
gp_pts = [coords[i] for i, pt in enumerate(d['CarCoordinates']) if pt['p'] < 0.15]
gp_x = [c[0] for c in gp_pts]
gp_z = [c[2] for c in gp_pts]
print(f"GP section bounds: X=[{min(gp_x):.1f}, {max(gp_x):.1f}], Z=[{min(gp_z):.1f}, {max(gp_z):.1f}]")

