import gzip, json, os
import numpy as np

def correlate(track_name, shtl_path, mztrack_path):
    print("=" * 60)
    print(f"ANALYZING: {track_name}")
    print("=" * 60)
    
    d_sim = json.loads(gzip.decompress(open(shtl_path, 'rb').read()))
    sim_pts = [pt['Value'] for pt in d_sim.get('CarCoordinates', []) if pt.get('Value')]
    sim_pct = [pt['p'] for pt in d_sim.get('CarCoordinates', []) if pt.get('Value')]
    
    d_mz = json.load(open(mztrack_path, 'r', encoding='utf-8'))
    mz_data = d_mz['sectors'][0]['data']
    
    print(f"SimHub points: {len(sim_pts)}, mztrack points: {len(mz_data)}")
    
    # Let's inspect SimHub X and Z over progress p (0..1)
    sim_x = np.array([p[0] for p in sim_pts])
    sim_z = np.array([p[2] for p in sim_pts])
    
    # mztrack data points: [x, y, 5000]
    # Note mz_data order is around the lap!
    mz_x = np.array([p[0] for p in mz_data], dtype=float)
    mz_y = np.array([p[1] for p in mz_data], dtype=float)
    
    print(f"SimHub start: ({sim_x[0]:.1f}, {sim_z[0]:.1f}), mid: ({sim_x[len(sim_x)//2]:.1f}, {sim_z[len(sim_z)//2]:.1f})")
    print(f"mztrack start: ({mz_x[0]}, {mz_y[0]}), mid: ({mz_x[len(mz_x)//2]}, {mz_y[len(mz_y)//2]})")
    
    # Let's check aspect ratio of both:
    sim_w = sim_x.max() - sim_x.min()
    sim_h = sim_z.max() - sim_z.min()
    mz_w = mz_x.max() - mz_x.min()
    mz_h = mz_y.max() - mz_y.min()
    
    print(f"SimHub span: dx={sim_w:.1f}, dz={sim_h:.1f}, ratio (dx/dz) = {sim_w/sim_h:.4f}, (dz/dx) = {sim_h/sim_w:.4f}")
    print(f"mztrack metadata: x_max={d_mz.get('x_max')}, y_max={d_mz.get('y_max')}")
    print(f"mztrack span: dx={mz_w}, dy={mz_h}, ratio = {mz_w/mz_h:.4f}")

correlate(
    "Indianapolis",
    r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\indianapolis 2022 road-Road Course.shtl",
    r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"
)

correlate(
    "Bathurst",
    r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\bathurst-6144.1.shtl",
    r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\bathurst.mztrack"
)

correlate(
    "Nurburgring Combined Short B",
    r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\nurburgring combinedshortb-24154.4.shtl",
    r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\nurburgring combinedShortB.mztrack"
)

