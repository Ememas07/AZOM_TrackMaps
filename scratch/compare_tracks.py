import gzip, json, os
import numpy as np

def inspect_track(track_name, shtl_path, mztrack_path):
    print("=" * 60)
    print(f"TRACK: {track_name}")
    print("=" * 60)

    # SimHub map
    if os.path.exists(shtl_path):
        d_simhub = json.loads(gzip.decompress(open(shtl_path, 'rb').read()))
        sim_coords = [pt['Value'] for pt in d_simhub.get('CarCoordinates', []) if pt.get('Value')]
        sim_x = np.array([c[0] for c in sim_coords])
        sim_y = np.array([c[1] for c in sim_coords])
        sim_z = np.array([c[2] for c in sim_coords])
        print(f"SimHub ({len(sim_coords)} pts):")
        print(f"  X: min={sim_x.min():.1f}, max={sim_x.max():.1f}, span={sim_x.max()-sim_x.min():.1f}")
        print(f"  Y: min={sim_y.min():.1f}, max={sim_y.max():.1f}, span={sim_y.max()-sim_y.min():.1f}")
        print(f"  Z: min={sim_z.min():.1f}, max={sim_z.max():.1f}, span={sim_z.max()-sim_z.min():.1f}")
        print(f"  Start: X={sim_x[0]:.1f}, Y={sim_y[0]:.1f}, Z={sim_z[0]:.1f}")
    else:
        print(f"SimHub file not found: {shtl_path}")
        sim_x, sim_z = None, None

    # PitHouse mztrack
    if os.path.exists(mztrack_path):
        d_mz = json.load(open(mztrack_path, 'r', encoding='utf-8'))
        sec = d_mz.get('sectors', [{}])[0]
        mz_pts = sec.get('data', [])
        mz_t = d_mz.get('transform', 0.0001)
        mz_x = np.array([p[0] * mz_t for p in mz_pts])
        mz_y = np.array([p[1] * mz_t for p in mz_pts])
        print(f"PitHouse mztrack ({len(mz_pts)} pts):")
        print(f"  transform: {mz_t}, x_max: {d_mz.get('x_max')}, y_max: {d_mz.get('y_max')}")
        print(f"  Raw X: min={mz_x.min():.4f}, max={mz_x.max():.4f}")
        print(f"  Raw Y: min={mz_y.min():.4f}, max={mz_y.max():.4f}")
        print(f"  Start pt: X={mz_x[0]:.4f}, Y={mz_y[0]:.4f}")
    else:
        print(f"PitHouse file not found: {mztrack_path}")

inspect_track(
    "Indianapolis",
    r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\indianapolis 2022 road-Road Course.shtl",
    r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"
)

inspect_track(
    "Bathurst",
    r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\bathurst-6144.1.shtl",
    r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\bathurst.mztrack"
)

inspect_track(
    "Nurburgring Combined Short B",
    r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\nurburgring combinedshortb-24154.4.shtl",
    r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\nurburgring combinedShortB.mztrack"
)

inspect_track(
    "Nurburgring Combined Short B (local MapRecords)",
    r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\nurburgring combinedshortb.shtl",
    r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\nurburgring combinedShortB.mztrack"
)

