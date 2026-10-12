import gzip, json, os

tracks = [
    ("Indianapolis", 
     r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\indianapolis 2022 road-Road Course.shtl",
     r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"),
    ("Bathurst",
     r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\bathurst-6144.1.shtl",
     r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\bathurst.mztrack"),
    ("Nurburgring_Combined",
     r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\nurburgring combinedshortb-24154.4.shtl",
     r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\nurburgring combinedShortB.mztrack")
]

svg_parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" style="background:#222">']

def to_path(pts, ox, oy, scale, flip_y=False):
    d = []
    for i, (x, y) in enumerate(pts):
        py = -y if flip_y else y
        sx = ox + x * scale
        sy = oy + py * scale
        d.append(f"{'M' if i == 0 else 'L'}{sx:.1f},{sy:.1f}")
    return " ".join(d)

for idx, (name, shtl, mz) in enumerate(tracks):
    y_off = idx * 380 + 30
    
    # 1. SimHub
    d_sim = json.loads(gzip.decompress(open(shtl, 'rb').read()))
    sim_pts = [pt['Value'] for pt in d_sim.get('CarCoordinates', []) if pt.get('Value')]
    sx = [p[0] for p in sim_pts]
    sz = [p[2] for p in sim_pts]
    
    min_x, max_x = min(sx), max(sx)
    min_z, max_z = min(sz), max(sz)
    span = max(max_x - min_x, max_z - min_z)
    norm_sim = [((x - min_x) / span, (z - min_z) / span) for x, z in zip(sx, sz)]
    
    # 2. mztrack
    d_mz = json.load(open(mz, 'r', encoding='utf-8'))
    mz_pts = d_mz['sectors'][0]['data']
    mx = [p[0] * 0.0001 for p in mz_pts]
    my = [p[1] * 0.0001 for p in mz_pts]
    min_mx, max_mx = min(mx), max(mx)
    min_my, max_my = min(my), max(my)
    span_m = max(max_mx - min_mx, max_my - min_my)
    norm_mz = [((x - min_mx) / span_m, (y - min_my) / span_m) for x, y in zip(mx, my)]

    svg_parts.append(f'<text x="20" y="{y_off + 20}" fill="#fff" font-size="16" font-family="sans-serif">{name}</text>')
    
    # SimHub (col 0: x=50, y=y_off+40)
    p_sim = to_path(norm_sim, 50, y_off + 40, 300)
    svg_parts.append(f'<text x="50" y="{y_off + 35}" fill="#4af" font-size="12" font-family="sans-serif">SimHub (X, Z)</text>')
    svg_parts.append(f'<path d="{p_sim}" fill="none" stroke="#4af" stroke-width="2"/>')
    # start dot
    svg_parts.append(f'<circle cx="{50 + norm_sim[0][0]*300:.1f}" cy="{y_off + 40 + norm_sim[0][1]*300:.1f}" r="4" fill="#0f0"/>')

    # mztrack raw (col 1: x=420)
    p_mz = to_path(norm_mz, 420, y_off + 40, 300)
    svg_parts.append(f'<text x="420" y="{y_off + 35}" fill="#fa4" font-size="12" font-family="sans-serif">mztrack Raw (X, Y)</text>')
    svg_parts.append(f'<path d="{p_mz}" fill="none" stroke="#fa4" stroke-width="2"/>')
    svg_parts.append(f'<circle cx="{420 + norm_mz[0][0]*300:.1f}" cy="{y_off + 40 + norm_mz[0][1]*300:.1f}" r="4" fill="#0f0"/>')

    # mztrack with inverted Y (col 2: x=790)
    norm_mz_flip = [(x, 1.0 - y) for x, y in norm_mz]
    p_mz_flip = to_path(norm_mz_flip, 790, y_off + 40, 300)
    svg_parts.append(f'<text x="790" y="{y_off + 35}" fill="#f44" font-size="12" font-family="sans-serif">mztrack (X, 1-Y)</text>')
    svg_parts.append(f'<path d="{p_mz_flip}" fill="none" stroke="#f44" stroke-width="2"/>')
    svg_parts.append(f'<circle cx="{790 + norm_mz_flip[0][0]*300:.1f}" cy="{y_off + 40 + norm_mz_flip[0][1]*300:.1f}" r="4" fill="#0f0"/>')

svg_parts.append('</svg>')

with open(r"c:\Users\Marc Mas\Documents\AZOM\scratch\tracks_comparison.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg_parts))

print("Saved tracks_comparison.svg")

