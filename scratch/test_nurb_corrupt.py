import gzip, json

p = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\nurburgring combinedshortb.shtl"
d = json.loads(gzip.decompress(open(p, "rb").read()))
coords = d['CarCoordinates']
pcts = [c['p'] for c in coords]
vals = [c['Value'] for c in coords]

import bisect

def to_abs(p_val):
    if p_val <= pcts[0]: return vals[0]
    if p_val >= pcts[-1]: return vals[-1]
    idx = bisect.bisect_right(pcts, p_val) - 1
    idx = min(max(idx, 0), len(pcts) - 2)
    p0, p1 = pcts[idx], pcts[idx+1]
    r = (p_val - p0) / (p1 - p0)
    v0, v1 = vals[idx], vals[idx+1]
    return [v0[k] + (v1[k] - v0[k]) * r for k in range(3)]

# Let's test progression through the lap:
# GP section is roughly 0% to 15% (3.6 km out of 24.1 km)
# Nordschleife entrance is at ~15%
for p_test in [0.0001, 0.0005, 0.001, 0.01, 0.05, 0.10, 0.15, 0.20, 0.50, 0.90]:
    v = to_abs(p_test)
    print(f"p={p_test*100:5.2f}%: X={v[0]:8.1f}, Z={v[2]:8.1f}")

