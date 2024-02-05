import bpy

count = 0
clear = True
for distModel in bpy.data.objects:
    if distModel.name[-5:] == "_dist":
        highModel = bpy.data.objects[distModel.name[:-5]]
        if(highModel):
            bpy.ops.object.select_all(action='DESELECT')
            highModel.select_set(True)
            distLocation = distModel.location.copy()
            distModel.location = highModel.location
            distModel.select_set(True)
            bpy.context.view_layer.objects.active = distModel
            bpy.ops.object.bake(
                type = "DIFFUSE", 
                pass_filter = {"COLOR"}, 
                margin = 4, 
                margin_type = "ADJACENT_FACES",
                use_selected_to_active = True,
                cage_extrusion = 64,
                use_clear = clear,
            )
            distModel.location = distLocation
            count = count + 1
            clear = False
            #if count == 4:
            #    break