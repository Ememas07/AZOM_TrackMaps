import re

b = open(r"C:\Program Files (x86)\SimHub\ICarsReader.dll", "rb").read()

# Search for calls or usages of GD_RelativeCarCoordinates or RelativeCarCoordinates
pos = b.find(b"GD_RelativeCarCoordinates")
print("GD_RelativeCarCoordinates pos:", pos)

pos2 = b.find(b"RelativeCarCoordinates")
print("RelativeCarCoordinates pos:", pos2)

# Is there any other reference to RelativeCarCoordinates in the binary?
indices = [m.start() for m in re.finditer(b"RelativeCarCoordinates", b)]
print("All matches:", indices)

