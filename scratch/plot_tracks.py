import gzip, json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, axs = plt.subplots(3, 3, figsize=(15, 15))

tracks = [
    ("Indianapolis", 
     r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\indianapolis 2022 road-Road Course.shtl",
     r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"),
    ("Bathurst",
     r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\bathurst-6144.1.shtl",
     r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\bathurst.mztrack"),
    ("Nurburgring Combined Short B",
     r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecordsCloud\nurburgring combinedshortb-24154.4.shtl",
     r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\nurburgring combinedShortB.mztrack")
]

for row, (name, shtl, mz) in enumerate(tracks):
    # SimHub
    d_sim = json.loads(gzip.decompress(open(shtl, 'rb').read()))
    sim_pts = [pt['Value'] for pt in d_sim.get('CarCoordinates', []) if pt.get('Value')]
    sx = np.array([p[0] for p in sim_pts])
    sz = np.array([p[2] for p in sim_pts])
    
    # mztrack
    d_mz = json.load(open(mz, 'r', encoding='utf-8'))
    mz_pts = d_mz['sectors'][0]['data']
    mx = np.array([p[0] * 0.0001 for p in mz_pts])
    my = np.array([p[1] * 0.0001 for p in mz_pts])
    
    # Col 0: SimHub (X vs Z)
    ax0 = axs[row, 0]
    ax0.plot(sx, sz, 'b-', label='path')
    ax0.plot(sx[0], sz[0], 'go', label='start (0%)')
    ax0.plot(sx[len(sx)//4], sz[len(sz)//4], 'ro', label='25%')
    ax0.set_title(f"{name}\nSimHub (X vs Z)")
    ax0.set_aspect('equal')
    ax0.grid(True)
    ax0.legend(fontsize=8)
    
    # Col 1: mztrack (X vs Y raw)
    ax1 = axs[row, 1]
    ax1.plot(mx, my, 'm-', label='mz path')
    ax1.plot(mx[0], my[0], 'go', label='start (0%)')
    ax1.plot(mx[len(mx)//4], my[len(my)//4], 'ro', label='25%')
    ax1.set_title(f"{name}\nmztrack (X vs Y)")
    ax1.set_aspect('equal')
    ax1.grid(True)
    ax1.legend(fontsize=8)
    
    # Col 2: mztrack with Y flipped (X vs -Y)
    ax2 = axs[row, 2]
    ax2.plot(mx, -my, 'r-', label='mz (X, -Y)')
    ax2.plot(mx[0], -my[0], 'go', label='start (0%)')
    ax2.plot(mx[len(mx)//4], -my[len(my)//4], 'ro', label='25%')
    ax2.set_title(f"{name}\nmztrack (X vs -Y)")
    ax2.set_aspect('equal')
    ax2.grid(True)
    ax2.legend(fontsize=8)

plt.tight_layout()
plt.savefig(r"c:\Users\Marc Mas\Documents\AZOM\scratch\tracks_comparison.png", dpi=100)
print("Saved tracks_comparison.png successfully")

