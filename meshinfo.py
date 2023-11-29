from es3 import nif
from dataclasses import dataclass
from pathlib import Path
import sys
import math

@dataclass
class MeshInfo:
    triCount: int
    shapeCount: int
    xMin: float
    yMin: float
    zMin: float
    xMax: float
    yMax: float
    zMax: float
    

def ExpandNode(node, info, x, y, z, scale):
    if node:
        #print(node)
        if hasattr(node, 'translation'):
            x = x + node.translation[0] * scale
            y = y + node.translation[1] * scale
            z = z + node.translation[2] * scale
        if hasattr(node, 'scale'):
            scale = scale * node.scale

        
        if isinstance(node, nif.NiLODNode):
            ExpandNode(node.children[0], info, x, y, z, scale) #skip other lods
        elif isinstance(node, nif.NiTriShape):
                info.shapeCount = info.shapeCount + 1
                info.triCount = info.triCount + len(node.data.triangles)
                xMin = float("inf")
                yMin = float("inf")
                zMin = float("inf")
                xMax = float("-inf")
                yMax = float("-inf")
                zMax = float("-inf")

                for vert in node.data.vertices:
                    if vert[0] < xMin:
                        xMin = vert[0]
                    if vert[0] > xMax:
                        xMax = vert[0]
                    if vert[1] < yMin:
                        yMin = vert[1]
                    if vert[1] > yMax:
                        yMax = vert[1]
                    if vert[2] < zMin:
                        zMin = vert[2]
                    if vert[2] > zMax:
                        zMax = vert[2]
                xMax = xMax * scale + x
                yMax = yMax * scale + y
                zMax = zMax * scale + z
                xMin = xMin * scale + x
                yMin = yMin * scale + y
                zMin = zMin * scale + z
                
                if xMin < info.xMin:
                    info.xMin = xMin
                if yMin < info.yMin:
                    info.yMin = yMin
                if zMin < info.zMin:
                    info.zMin = zMin
                if xMax > info.xMax:
                    info.xMax = xMax
                if yMax > info.yMax:
                    info.yMax = yMax
                if zMax > info.zMax:
                    info.zMax = zMax
                
                                
                                                                                                
                #print("SHAPE: ", x, y, z, scale)
                #print("(", math.floor(xMin), ",", math.floor(xMax), ") (", math.floor(yMin), ",", math.floor(yMax), ") (", math.floor(zMin), ",", math.floor(zMax), ")", sep='')

                
        elif hasattr(node, 'children') and not isinstance(node, nif.RootCollisionNode):
            childTriCount = 0
            childShapeCount = 0
            for child in node.children:
                ExpandNode(child, info, x, y, z, scale)
            #print("ninode", childTriCount, childShapeCount)



def PrintNifStats(folder):
    path = Path(folder)

    for mesh in path.rglob("*.nif"):
        #mesh = "C:/Games/MorrowindMods/Morrowind Optimization Patch/00 Core/meshes/x/ex_v_foundation_03.nif"
        
        stream = nif.NiStream()
        stream.load(mesh)

        info = MeshInfo(0, 0, float("inf"), float("inf"), float("inf"), float("-inf"), float("-inf"), float("-inf"))

        for root in stream.roots:
            ExpandNode(root, info, 0, 0, 0, 1)

        if(info.triCount > 0):
            print(mesh, info.triCount, info.shapeCount, math.floor((info.xMax - info.xMin) * (info.yMax - info.yMin) * (info.zMax - info.zMin)), sep='|')
        #break
        #print("(", info.xMin, ",", info.xMax, ") (", info.yMin, ",", info.yMax, ") (", info.zMin, ",", info.zMax, ")", sep='')
        #print("(", math.floor(info.xMin), ",", math.floor(info.xMax), ") (", math.floor(info.yMin), ",", math.floor(info.yMax), ") (", math.floor(info.zMin), ",", math.floor(info.zMax), ")", sep='')

#mesh = "E:/Extracted/Morrowind/meshes/f/terrain_rock_wg_09.nif"
#mesh = "E:/Extracted/Morrowind/meshes/f/aaafricked.nif"
#mesh = "F:/Anna/Desktop/bad.nif"

PrintNifStats("E:/Extracted/Morrowind/combinedmeshesforconvenience")

#triCount = 0
#shapeCount = 0

#def PrintShapeData(shape, triCount, shapeCount):
#    material = shape.get_property(nif.NiMaterialProperty)
#    if not material:
#        return triCount, shapeCount
#    #print(len(shape.data.triangles))
#    return triCount + len(shape.data.triangles), shapeCount + 1


#hasLod = False
#for lodNode in stream.objects_of_type(nif.NiLODNode):
#    for node in lodNode.children[0].descendants():
#        if isinstance(node, nif.NiTriShape):
#            triCount, shapeCount = PrintShapeData(node, triCount, shapeCount)
#    hasLod = True
    
#if not hasLod:
#    for shape in stream.objects_of_type(nif.NiTriShape):
#        triCount, shapeCount = PrintShapeData(shape, triCount, shapeCount)

#print("OLD TEST", mesh, triCount, shapeCount, sep='|')
