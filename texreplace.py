import sys
from es3 import nif

nifPath = sys.argv[1]
outPath = sys.argv[2]
texname = sys.argv[3]

stream = nif.NiStream()
stream.load(nifPath)

for texture in stream.objects_of_type(nif.NiSourceTexture):
    texture.filename = texname

stream.save(outPath)