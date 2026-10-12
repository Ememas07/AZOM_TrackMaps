import json, os

td = r'C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing'
tracks = [
    'indianapolis 2022 road.mztrack',
    'bathurst.mztrack',
    'nurburgring combinedShortB.mztrack',
    'nurburgring nordschleife.mztrack'
]

for name in tracks:
    p = os.path.join(td, name)
    if not os.path.exists(p):
        print(f"File not found: {name}")
        continue
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    sec = d.get('sectors', [{}])[0]
    pts = sec.get('data', [])
    xs = [pt[0] for pt in pts]
    ys = [pt[1] for pt in pts]
    zs = [pt[2] for pt in pts]
    print(name)
    print(f"  count={len(pts)} transform={d.get('transform')}")
    print(f"  x_min={d.get('x_min')} x_max={d.get('x_max')} y_min={d.get('y_min')} y_max={d.get('y_max')}")
    print(f"  pt[0]={pts[0]} pt[-1]={pts[-1]}")
    print(f"  xs: min={min(xs)} max={max(xs)} span={max(xs)-min(xs)}")
    print(f"  ys: min={min(ys)} max={max(ys)} span={max(ys)-min(ys)}")
    print(f"  zs: min={min(zs)} max={max(zs)} span={max(zs)-min(zs)}")

