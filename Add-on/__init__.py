import bpy


# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

##### --- Modification Header --- #############
# 
# Date: 11 Oct 2023
# Author (of modifications only): Andreas Altmann
# Name/Version: importdepthmap_1.1.1_LI1.zip (added suffix to the original version denoting Leia Inc change #1)
# Description: This code is a modification of code developed originally by Elin. Modifications performed by Leia Inc. as noted using inline comments in code
# A thank you to Elin who provided the bulk of this code
#
# Original code can be found here: https://github.com/Ladypoly/Serpens-Bledner-Addons/tree/main/Serpens3
# Version used as base for the modifications: importdepthmap_1.1.1.zip
#
# Modifications Performed:
#  - changed default subdivision modifier levels from 6 to 8 for standard depth maps, and from 3 to 5 for panoramas
#  - changed color space for depth map from sRGB to Raw
#  - changed texture mapping from CLIP to EXTEND to avoid wrapping the UV
#  - Added a simple deform modifier that allows underlying plane to be curved for field of view simulation. For this also needed to add a empty object for orientation
# 
###############################################

bl_info = {
    "name" : "ImportDepthMap",
    "author" : "Elin", 
    "description" : "",
    "blender" : (3, 3, 0),
    "version" : (1, 1, 1),
    "location" : "Import",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "Import-Export" 
}


import bpy
import bpy.utils.previews
import math
import os
from bpy_extras.io_utils import ImportHelper, ExportHelper


addon_keymaps = {}
_icons = None
nodetree = {'sna_image': None, 'sna_depthimage': None, 'sna_normalempty': None, 'sna_camera': None, 'sna_pano': False, 'sna_aspectratio': 0.0, 'sna_usesepimages': False, }


def sna_subsurfsettings_8C39B(Name, Levels, Type, Index):
    list(bpy.context.view_layer.objects.active.modifiers)[Index].name = Name
    list(bpy.context.view_layer.objects.active.modifiers)[Index].subdivision_type = Type
    list(bpy.context.view_layer.objects.active.modifiers)[Index].render_levels = Levels
    list(bpy.context.view_layer.objects.active.modifiers)[Index].levels = Levels


def sna_materialsetup_AC51B():
    bpy.ops.object.material_slot_add('INVOKE_DEFAULT', )
    material_F46A0 = bpy.data.materials.new(name=nodetree['sna_image'].name, )
    material_F46A0.use_nodes = True
    bpy.context.object.active_material = material_F46A0
    node_A7B06 = material_F46A0.node_tree.nodes.new(type='ShaderNodeTexImage', )
    node_A7B06.location = (-300.0, 100.0)
    node_A7B06.image = nodetree['sna_image']
    material_F46A0.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.9900000095367432
    material_F46A0.node_tree.nodes['Principled BSDF'].inputs['Specular'].default_value = 0.009999999776482582
    link_B8FF1 = material_F46A0.node_tree.links.new(input=material_F46A0.node_tree.nodes['Principled BSDF'].inputs[0], output=node_A7B06.outputs[0], )
    link_F8C6B = material_F46A0.node_tree.links.new(input=material_F46A0.node_tree.nodes['Principled BSDF'].inputs['Emission'], output=node_A7B06.outputs[0], )
    if nodetree['sna_usesepimages']:
        pass
    else:
        node_4DD1D = material_F46A0.node_tree.nodes.new(type='ShaderNodeMapping', )
        node_4DD1D.location = (-500.0, 100.0)
        link_BF94B = material_F46A0.node_tree.links.new(input=node_A7B06.inputs[0], output=node_4DD1D.outputs[0], )
        node_125D2 = material_F46A0.node_tree.nodes.new(type='ShaderNodeTexCoord', )
        node_125D2.location = (-700.0, 100.0)
        link_0752D = material_F46A0.node_tree.links.new(input=node_4DD1D.inputs[0], output=node_125D2.outputs[2], )
        node_4DD1D.inputs['Scale'].default_value = (0.5, 1.0, 1.0)


def sna_normaleditsettings_DF45C(Index):
    bpy.context.active_object.modifiers[Index].target = nodetree['sna_normalempty']
    list(bpy.context.view_layer.objects.active.modifiers)[Index].mode = 'DIRECTIONAL'


class SNA_AddonPreferences_45548(bpy.types.AddonPreferences):
    bl_idname = 'importdepthmap'

    def draw(self, context):
        if not (False):
            layout = self.layout 
            row_BB4FF = layout.row(heading='', align=False)
            row_BB4FF.alert = False
            row_BB4FF.enabled = True
            row_BB4FF.active = True
            row_BB4FF.use_property_split = False
            row_BB4FF.use_property_decorate = False
            row_BB4FF.scale_x = 1.0
            row_BB4FF.scale_y = 1.0
            row_BB4FF.alignment = 'Expand'.upper()
            if not True: row_BB4FF.operator_context = "EXEC_DEFAULT"
            row_BB4FF.prop(bpy.context.scene, 'sna_camerasetup', text='Create Camera Setup', icon_value=0, emboss=True)


def sna_addcamera_41AE0():
    bpy.ops.object.camera_add('INVOKE_DEFAULT', location=nodetree['sna_normalempty'].location, rotation=(math.radians(90.0), 0.0, 0.0))
    nodetree['sna_camera'] = bpy.context.view_layer.objects.active
    constraint_238FE = nodetree['sna_normalempty'].constraints.new(type='COPY_TRANSFORMS', )
    constraint_238FE.target = nodetree['sna_camera']
    constraint_238FE.influence = 0.5


def sna_add_to_topbar_mt_file_import_04409(self, context):
    if not (False):
        layout = self.layout
        op = layout.operator('sna.load_image_ae495', text='Import Depth Map', icon_value=0, emboss=True, depress=False)
        op.sna_seperate_depth_map = False
        op.sna_pano = False


class SNA_OT_Load_Image_Ae495(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.load_image_ae495"
    bl_label = "Load Image"
    bl_description = "Load combined color and depth image or:"
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.png;*.jpg;*.exr', options={'HIDDEN'} )
    sna_seperate_depth_map: bpy.props.BoolProperty(name='Seperate Depth Map', description='Select a seperate depth map', default=False)
    sna_pano: bpy.props.BoolProperty(name='360Pano', description='', default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        image_736E6 = bpy.data.images.load(filepath=self.filepath, )
        nodetree['sna_usesepimages'] = self.sna_seperate_depth_map
        nodetree['sna_pano'] = self.sna_pano
        nodetree['sna_image'] = image_736E6
        nodetree['sna_aspectratio'] = (float(image_736E6.size[0] / image_736E6.size[1]) if nodetree['sna_usesepimages'] else float(float(image_736E6.size[0] / 2.0) / image_736E6.size[1]))
        if nodetree['sna_usesepimages']:
            bpy.ops.sna.load_depth_image_ec8b8('INVOKE_DEFAULT', )
        else:
            sna_buildsetup_63DA1()
        return {"FINISHED"}


class SNA_OT_Load_Depth_Image_Ec8B8(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.load_depth_image_ec8b8"
    bl_label = "Load Depth Image"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.png;*.jpg;*.exr', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        image_DC27F = bpy.data.images.load(filepath=self.filepath, )
        nodetree['sna_depthimage'] = image_DC27F
        sna_buildsetup_63DA1()
        return {"FINISHED"}


def sna_buildsetup_63DA1():
    if bpy.context.scene.sna_camerasetup:
        if nodetree['sna_pano']:
            pass
        else:
            bpy.ops.object.empty_add('INVOKE_DEFAULT', type='SINGLE_ARROW', radius=0.30000001192092896, location=(0.0, -2.0, 0.0), rotation=(math.radians(-90.0), 0.0, 0.0))
            bpy.context.view_layer.objects.active.name = nodetree['sna_image'].name.split(',')[0] + '_Align'
            nodetree['sna_normalempty'] = bpy.context.view_layer.objects.active
            sna_addcamera_41AE0()
    if nodetree['sna_pano']:
        bpy.ops.mesh.primitive_uv_sphere_add('INVOKE_DEFAULT', segments=32, ring_count=16, radius=50.0)
        bpy.context.view_layer.objects.active.name = nodetree['sna_image'].name.split(',')[0]
        bpy.ops.object.shade_smooth('INVOKE_DEFAULT', use_auto_smooth=True, auto_smooth_angle=math.radians(60.0))
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT', toggle=False)
        bpy.ops.mesh.flip_normals('INVOKE_DEFAULT', )
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT', toggle=False)
        bpy.ops.object.transform_apply('INVOKE_DEFAULT', location=True, rotation=True, scale=True)
        sna_materialsetup_AC51B()
        bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='SUBSURF')
        sna_subsurfsettings_8C39B('SIMPLE Subsurf', 5, 'CATMULL_CLARK', 0) #LeiaInc LI1 modifications: changed levels from 3 to 5
        bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='DISPLACE')
        sna_setdisplacesettings_E5830(1, 50.0)
        bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='SUBSURF')
        sna_subsurfsettings_8C39B('Smooth Subsurf', 1, 'CATMULL_CLARK', 2)
    else:
        if not bpy.data.objects.get('Empty_DepthMapReference'): #LeiaInc LI1 modification: create empty object for Simple Deform Modifier to use
            bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            bpy.context.view_layer.objects.active.name = "Empty_DepthMapReference"
            bpy.context.object.rotation_euler[2] = 3.14159 #rotate by 180 degrees around z axis
            bpy.context.view_layer.objects.active.hide_set(True)
            bpy.context.view_layer.objects.active.hide_render = True
        bpy.ops.mesh.primitive_plane_add('INVOKE_DEFAULT', size=1.0)
        bpy.context.view_layer.objects.active.name = nodetree['sna_image'].name.split(',')[0]
        bpy.ops.object.shade_smooth('INVOKE_DEFAULT', use_auto_smooth=True, auto_smooth_angle=math.radians(60.0))
        bpy.context.view_layer.objects.active.rotation_euler = (math.radians(90.0), 0.0, 0.0)
        bpy.context.view_layer.objects.active.location = (0.0, 0.0, 0.5)
        bpy.context.view_layer.objects.active.scale = (nodetree['sna_aspectratio'], 1.0, 1.0)
        bpy.ops.object.transform_apply('INVOKE_DEFAULT', location=True, rotation=True, scale=True)
        bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='SUBSURF')
        sna_subsurfsettings_8C39B('SIMPLE Subsurf', 8, 'SIMPLE', 0) #LeiaInc LI1 modifications: changed levels from 6 to 8
        bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='SIMPLE_DEFORM') #LeiaInc LI1 - Add Simple Deform Modifier
        leia_deformsettings(1) #LeiaInc LI1 - Add Simple Deform Modifier
        bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='NORMAL_EDIT')
        sna_normaleditsettings_DF45C(2) #LeiaInc LI1 - index incremented 1 to 2
        bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='DISPLACE')
        sna_setdisplacesettings_E5830(3, 1.0) #LeiaInc LI1 - index incremented 2 to 3
        bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='SUBSURF')
        sna_subsurfsettings_8C39B('Smooth Subsurf', 1, 'CATMULL_CLARK', 4) #LeiaInc LI1 - index incremented 3 to 4
        sna_materialsetup_AC51B()


def sna_setdisplacesettings_E5830(Index, Strength):
    list(bpy.context.view_layer.objects.active.modifiers)[Index].texture_coords = 'UV'
    list(bpy.context.view_layer.objects.active.modifiers)[Index].direction = 'CUSTOM_NORMAL'
    texture_F90B3 = bpy.data.textures.new(name='DepthDisplace', type='IMAGE', )
    list(bpy.context.view_layer.objects.active.modifiers)[Index].texture = texture_F90B3
    list(bpy.context.view_layer.objects.active.modifiers)[Index].strength = Strength
    texture_F90B3.extension = 'EXTEND' #LeiaInc LI1 modification: changed from CLIP to EXTEND to avoid wrapping of UV
    if nodetree['sna_usesepimages']:
        texture_F90B3.image = nodetree['sna_depthimage']
    else:
        texture_F90B3.image = nodetree['sna_image']
        list(bpy.context.view_layer.objects.active.modifiers)[Index].texture.crop_min_x = 0.5
    texture_F90B3.image.colorspace_settings.name = 'Raw' #LeiaInc LI1 modification: change from sRGB (default)_to Raw so that colorspace mapping does not skew depth map


def leia_deformsettings(Index): #LeiaInc LI1 - Add Simple Deform Modifier
    list(bpy.context.view_layer.objects.active.modifiers)[Index].origin = bpy.data.objects["Empty_DepthMapReference"]
    list(bpy.context.view_layer.objects.active.modifiers)[Index].deform_method = 'BEND'
    list(bpy.context.view_layer.objects.active.modifiers)[Index].deform_axis = 'Z'
    list(bpy.context.view_layer.objects.active.modifiers)[Index].angle = 0 #default to no curvature
    

def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.types.Scene.sna_camerasetup = bpy.props.BoolProperty(name='CameraSetup', description='', default=False)
    bpy.utils.register_class(SNA_AddonPreferences_45548)
    bpy.types.TOPBAR_MT_file_import.append(sna_add_to_topbar_mt_file_import_04409)
    bpy.utils.register_class(SNA_OT_Load_Image_Ae495)
    bpy.utils.register_class(SNA_OT_Load_Depth_Image_Ec8B8)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_camerasetup
    bpy.utils.unregister_class(SNA_AddonPreferences_45548)
    bpy.types.TOPBAR_MT_file_import.remove(sna_add_to_topbar_mt_file_import_04409)
    bpy.utils.unregister_class(SNA_OT_Load_Image_Ae495)
    bpy.utils.unregister_class(SNA_OT_Load_Depth_Image_Ec8B8)

