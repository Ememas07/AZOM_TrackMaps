import gzip, json, os
import numpy as np

def analyze_track_alignment(name, shtl_path, mztrack_path):
    print("=" * 70)
    print(f"ALIGNMENT ANALYSIS: {name}")
    print("=" * 70)
    
    # 1. SimHub map
    d_sim = json.loads(gzip.decompress(open(shtl_path, 'rb').read()))
    sim_pts = [pt['Value'] for pt in d_sim.get('CarCoordinates', []) if pt.get('Value')]
    sim_x = np.array([p[0] for p in sim_pts])
    sim_z = np.array([p[2] for p in sim_pts])
    
    # 2. PitHouse map
    d_mz = json.load(open(mztrack_path, 'r', encoding='utf-8'))
    mz_data = d_mz['sectors'][0]['data']
    mz_x = np.array([p[0] for p in mz_data], dtype=float)
    mz_y = np.array([p[1] for p in mz_data], dtype=float)
    
    # Both sets of points trace the track starting at lap start (0%) to lap end (100%).
    # Let's resample both to N=500 points along the path (0% to 100% of lap)
    N = 500
    sim_idx = np.linspace(0, len(sim_x)-1, N).astype(int)
    mz_idx = np.linspace(0, len(mz_x)-1, N).astype(int)
    
    sx = sim_x[sim_idx]
    sz = sim_z[sim_idx]
    mx = mz_x[mz_idx]
    my = mz_y[mz_idx]
    
    # Normalize both to zero-mean and unit variance or [0, 1] bounding box
    # Let's inspect bounding boxes
    print(f"SimHub bounding box: X=[{sim_x.min():.1f}, {sim_x.max():.1f}], Z=[{sim_z.min():.1f}, {sim_z.max():.1f}]")
    print(f"mztrack bounding box: X=[{mz_x.min():.1f}, {mz_x.max():.1f}], Y=[{mz_y.min():.1f}, {mz_y.max():.1f}]")
    print(f"mztrack metadata: x_max={d_mz.get('x_max')}, y_max={d_mz.get('y_max')}")
    
    # Notice: In SimHub, X is lateral, Z is forward (or vice versa in world frame).
    # In mztrack, points are [x, y, 5000].
    # Which axis in mztrack corresponds to which axis in SimHub?
    # Let's test all 8 possible 2D alignments (permutations of axes and reflections):
    # (mz_x, mz_y) vs (sim_x, sim_z):
    # Candidates for (target_x, target_z) from (mx, my):
    # 1. (+mx, +my)
    # 2. (-mx, +my)
    # 3. (+mx, -my)
    # 4. (-mx, -my)
    # 5. (+my, +mx)
    # 6. (-my, +mx)
    # 7. (+my, -mx)
    # 8. (-my, -mx)
    
    # Let's center both
    sx_c = sx - sx.mean()
    sz_c = sz - sz.mean()
    mx_c = mx - mx.mean()
    my_c = my - my.mean()
    
    # Let's check correlations between the progressions
    corrs = {
        "(+mx, +my)": (np.corrcoef(sx_c, mx_c)[0,1], np.corrcoef(sz_c, my_c)[0,1]),
        "(-mx, +my)": (np.corrcoef(sx_c, -mx_c)[0,1], np.corrcoef(sz_c, my_c)[0,1]),
        "(+mx, -my)": (np.corrcoef(sx_c, mx_c)[0,1], np.corrcoef(sz_c, -my_c)[0,1]),
        "(-mx, -my)": (np.corrcoef(sx_c, -mx_c)[0,1], np.corrcoef(sz_c, -my_c)[0,1]),
        "(+my, +mx)": (np.corrcoef(sx_c, my_c)[0,1], np.corrcoef(sz_c, mx_c)[0,1]),
        "(-my, +mx)": (np.corrcoef(sx_c, -my_c)[0,1], np.corrcoef(sz_c, mx_c)[0,1]),
        "(+my, -mx)": (np.corrcoef(sx_c, my_c)[0,1], np.corrcoef(sz_c, -mx_c)[0,1]),
        "(-my, -mx)": (np.corrcoef(sx_c, -my_c)[0,1], np.corrcoef(sz_c, -mx_c)[0,1]),
    }
    
    print("\nCorrelations (X-corr, Z-corr):")
    for k, (cx, cz) in corrs.items():
        print(f"  {k:12s}: corr_X = {cx:+.4f}, corr_Z = {cz:+.4f}, avg = {(abs(cx)+abs(cz))/2:.4f}")

analyze_track_alignment(
    "Indianapolis",
    r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\indianapolis 2022 road-Road Course.shtl",
    r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"
)

analyze_track_alignment(
    "Bathurst",
    r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\bathurst-6144.1.shtl",
    r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\bathurst.mztrack"
)

analyze_track_alignment(
    "Nurburgring Combined Short B",
    r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\nurburgring combinedshortb-24154.4.shtl",
    r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\nurburgring combinedShortB.mztrack"
)

