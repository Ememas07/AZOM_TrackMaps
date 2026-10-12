import gzip, json

p_sim = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\indianapolis 2022 road-Road Course.shtl"
d_sim = json.loads(gzip.decompress(open(p_sim, 'rb').read()))
sim_pts = [pt['Value'] for pt in d_sim['CarCoordinates']]

p_mz = r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"
d_mz = json.load(open(p_mz))
mz_pts = d_mz['sectors'][0]['data']

# Let's find when X starts changing significantly (turn 1)
print("SimHub points around turn 1:")
for i in range(100, 250, 10):
    p = sim_pts[i]
    print(f"  idx {i:3d}: x={p[0]:7.1f}, z={p[2]:7.1f}")

print("\nmztrack points around turn 1:")
for i in range(80, 200, 10):
    p = mz_pts[i]
    print(f"  idx {i:3d}: x={p[0]*0.0001:7.4f}, y={p[1]*0.0001:7.4f}")

