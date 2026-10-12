import gzip, json
import numpy as np

# Indianapolis SimHub
p_sim = r"C:\Program Files (x86)\SimHub\PluginsData\IRacing\MapRecords\indianapolis 2022 road-Road Course.shtl"
d_sim = json.loads(gzip.decompress(open(p_sim, 'rb').read()))
sim_pts = [pt['Value'] for pt in d_sim['CarCoordinates']]
sx = np.array([p[0] for p in sim_pts])
sz = np.array([p[2] for p in sim_pts])

# Indianapolis mztrack
p_mz = r"C:\Program Files (x86)\MOZA Pit House\bin\GameConfigs\TrackData\iracing\indianapolis 2022 road.mztrack"
d_mz = json.load(open(p_mz))
mz_pts = d_mz['sectors'][0]['data']
mx = np.array([p[0] * 0.0001 for p in mz_pts])
my = np.array([p[1] * 0.0001 for p in mz_pts])

# Let's inspect where Turn 1 is:
# At Indianapolis Road Course:
# Start/finish is on the main straight.
# In SimHub:
# Start is at sx[0] = -8.6, sz[0] = 5.9.
# Then the car moves to sz = -600.
# Then it turns into Turn 1!
# In SimHub, does Turn 1 turn to positive X or negative X?
# sx goes from -16 to +335! It turns to POSITIVE X!
# Now look at mztrack:
# Start is at mx[0] = 0.0122, my[0] = 0.3865.
# Then my increases to ~0.85.
# Then mx goes from 0.0122 to 0.50! It turns to POSITIVE X!
print("SimHub Turn 1 dx:", sx[500] - sx[0])
print("mztrack Turn 1 dx:", mx[500] - mx[0])

# But now: where is Turn 1 on the screen?
# In mztrack: my increases (goes DOWN on screen).
# Then at the bottom of the screen, mx increases (turns RIGHT).
# Then it goes back UP (my decreases towards 0).
# Then at the top of the screen (Oval turn 4 / north turns):
# mx goes from 0.5 to 1.0 (towards the right), then curves around and comes down the back straight!
# WAIT!
# At the top of the screen:
# In mztrack: Oval Turn 4 is at mx = 0.5..1.0?
# Wait! On the real Indianapolis Motor Speedway:
# Where is Oval Turn 4?
# Oval Turn 4 is at the NORTH end of the main straight!
# Oval Turn 1 is at the SOUTH end of the main straight!
# The main straight is on the WEST side!
# The back straight is on the EAST side!
# If the main straight is on the WEST (LEFT):
# And cars on the road course drive NORTH up the main straight:
# Then cars drive UP towards the top of the screen, turn RIGHT (EAST) into the infield,
# meander south through the infield, and come onto the oval in the south!
# BUT IN SIMHUB:
# The car drove DOWN (sz decreased from 0 to -887), turned RIGHT into the infield at the SOUTH!
# That means SimHub's map is UPSIDE DOWN compared to the real track orientation!

