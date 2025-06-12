bl_info = {
    "name": "Dist Tools",
    "blender": (4, 0, 0),
    "category": "Object",
}


import bpy
import mathutils

def bake():
    count = 0
    clear = True
    for distModel in bpy.context.view_layer.objects:
        print(distModel.name)
        if distModel.name[-5:] == "_dist":
            highModel = bpy.context.view_layer.objects[distModel.name[:-5]]
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
                print("K")
                count = count + 1
                clear = False
                #if count == 4:
                #    break
                
def export():
    models = {}
    for distModel in bpy.context.view_layer.objects:
        if distModel.name[-5:] == "_dist" or distModel.name[-5:] == "_clon":
            keyName = distModel.name[:-5]

            if keyName[-7:-2] == "_part":
                keyName = keyName[:-7]
                
            if keyName in models:
                models[keyName] = models[keyName] + [distModel.name]
            else:
                models[keyName] = [distModel.name]
            print(keyName)
            
    for key in models.keys():
        bpy.ops.object.select_all(action='DESELECT')
        
        for model in models[key]:
                bpy.context.view_layer.objects[model].select_set(True)
                
        bpy.context.view_layer.objects.active = bpy.context.view_layer.objects[models[key][0]]
        
        if len(models[key]) > 1:
            bpy.ops.object.duplicate()
            bpy.ops.object.join()
            bpy.context.view_layer.objects.active.name = key + "_dist"

        distLocation = bpy.context.view_layer.objects.active.location.copy()
        bpy.context.view_layer.objects.active.location = mathutils.Vector((0.0, 0.0, 0.0))

        path = "E:\\export\\" + key + "_dist.nif"
        bpy.ops.export_scene.mw(filepath=path, use_selection=True)
        
        if len(models[key]) > 1:
            bpy.ops.object.delete()
        else:
            bpy.context.view_layer.objects.active.location = distLocation

            
class BakeDist(bpy.types.Operator):
    bl_idname = "object.bake_dist"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Bake Dist Meshes"         # Display name in the interface.

    def execute(self, context):        # execute() is called when running the operator.
        bake()
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

class ExportDist(bpy.types.Operator):
    bl_idname = "object.export_dist"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Export Dist Meshes"         # Display name in the interface.

    def execute(self, context):        # execute() is called when running the operator.
        export()
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.
        
def bake_menu_func(self, context):
    self.layout.operator(BakeDist.bl_idname)

def export_menu_func(self, context):
    self.layout.operator(ExportDist.bl_idname)

def register():
    bpy.utils.register_class(BakeDist)
    bpy.types.VIEW3D_MT_object.append(bake_menu_func)
    bpy.utils.register_class(ExportDist)
    bpy.types.VIEW3D_MT_object.append(export_menu_func)  
    

def unregister():
    bpy.utils.unregister_class(BakeDist)
    bpy.utils.unregister_class(ExportDist)