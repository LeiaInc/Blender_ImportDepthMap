# Blender_ImportDepthMap
Blender Add-On to import Depth Maps and create 3D displacement models from them

Refer to https://www.immersity.ai/tutorial/importing-depth-maps-from-immersityai-to-blender for tutorial on how to use.

# Overview
The code is based on the original work from Elin (https://github.com/Ladypoly). The original code is referenced here:
We modified this code to make some minor adjustments and to add Field of View functionality. Note that version 1.1.1 from Ladypoly was used as the basis for these modifications. This resulted in the Add-On used in the tutorial. We provide here an explanation of the basic operation of the 3rd party Add-On as well as the modifications that were performed by the Immersity AI team and why these were performed. For this section a rudimentary understanding of Blender is assumed.

# Features of this basic functionality
User provides file location to RGB image
User provides file location to Monochrome Depth Map
A Plane object is created
The RGB image is mapped to the plane object as Base Color
The RBG image is again mapped to the plane object as Emission so that the rendering is not light source dependent (in other words has it’s own “glow”). This avoids unevenness in brightness and avoids introducing unwanted shadows in the final rendering.
The Depth Map is placed into a Texture. In the modified code the following changes have been applied:
- The image is mapped using the extend method to avoid the depth map UV from wrapping around the plane as this causes edge artifacts
- The image colorspace is changed from sRGB to Raw so that color corrections don’t impact depth.
The Plane is subdivided into a mesh (with as many divisions as possible given processing power and memory). The original Blender Add-On goes to 6 levels of subdivision. The modified version has this increased to 8.
The Plane is curved using a Deform Modifier to correct for Camera Field of View distortions. The modifier is anchored to a empty object to provide a point of reference. This makes orienting the deformations easier. Both the modifier and the empty object are additions to the original code.
The plane is displaced using a Displacement Modifier with reference to the Depth Map Texture.
Rendering can be performed with the faster Eevee Render Engine as we are not concerned with light/material interaction, we are merely re-rendering an existing image from different viewpoints. As such we don’t really want to introduce unwanted artifacts from a more complex rendering engine
Note that the Add-On has other functionality that is not covered in this tutorial:
Importing of Panoramas
Automatic camera rig setup

A big shout out to Elin for making the original code available through GNU licensing.
