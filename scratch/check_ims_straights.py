import gzip, json

p_sim = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\indianapolis 2022 road-Road Course.shtl"
d_sim = json.loads(gzip.decompress(open(p_sim, 'rb').read()))
sim_pts = [pt['Value'] for pt in d_sim['CarCoordinates']]
sx = [p[0] for p in sim_pts]
sz = [p[2] for p in sim_pts]

p_mz = r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"
d_mz = json.load(open(p_mz))
mz_pts = d_mz['sectors'][0]['data']
mx = [p[0] * 0.0001 for p in mz_pts]
my = [p[1] * 0.0001 for p in mz_pts]

print("SimHub Start/Finish (Main Straight):")
print(f"  sx[0] = {sx[0]:.1f} (min={min(sx):.1f}, max={max(sx):.1f})")
print(f"  sz[0] = {sz[0]:.1f} (min={min(sz):.1f}, max={max(sz):.1f})")

print("\nmztrack Start/Finish (Main Straight):")
print(f"  mx[0] = {mx[0]:.4f} (min={min(mx):.4f}, max={max(mx):.4f})")
print(f"  my[0] = {my[0]:.4f} (min={min(my):.4f}, max={max(my):.4f})")

