import sys
from es3 import nif
from pathlib import Path

path = Path("E:/Extracted/Morrowind/combinedmeshesforconvenience")
for nifPath in path.rglob("*.nif"):
    stream = nif.NiStream()
    stream.load(nifPath)

    print(nifPath, end="|")
    for texture in stream.objects_of_type(nif.NiSourceTexture):
        print(texture.filename, end="|")
    print()