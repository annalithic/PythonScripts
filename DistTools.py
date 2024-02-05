bl_info = {
    "name": "Dist Tools",
    "blender": (4, 0, 0),
    "category": "Object",
}


import bpy


def bake():
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
                
def export():
    for distModel in bpy.data.objects:
        if distModel.name[-5:] == "_dist":
            bpy.ops.object.select_all(action='DESELECT')
            distModel.select_set(True)
            bpy.context.view_layer.objects.active = distModel
            path = "D:\\Desktop\\export\\" + distModel.name + ".nif"
            bpy.ops.export_scene.mw(filepath=path, use_selection=True)
        
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