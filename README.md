# Blender_ImportDepthMap

Blender Add-On to import Depth Maps and create 3D displacement models from them.

Refer to [this tutorial](https://www.immersity.ai/tutorial/importing-depth-maps-from-immersityai-to-blender) for instructions on how to use the add-on.

---

## Overview

This code is based on the original work by [Elin (Ladypoly)](https://github.com/Ladypoly). The original code is referenced here. 

We modified this code to make minor adjustments and add Field of View functionality. Version **1.1.1** from Ladypoly was used as the basis for these modifications. The modifications resulted in the add-on used in the tutorial. Below is an explanation of:
1. The basic operation of the third-party add-on.
2. The modifications performed by the Immersity AI team and the rationale behind them.

> **Note**: A basic understanding of Blender is assumed.

---

## Features of Basic Functionality

- **User Input**:
  - File location of the RGB image.
  - File location of the Monochrome Depth Map.

- **Output**:
  - A Plane object is created.
  - The RGB image is mapped to the plane object as:
    - Base Color.
    - Emission (to make rendering independent of light sources, giving the image a “glow” effect). This avoids uneven brightness and unwanted shadows in the final rendering.

- **Depth Map Handling**:
  - The Depth Map is placed into a Texture.
  - Modifications made to the original code:
    - The image is mapped using the **extend method** to prevent UV wrapping around the plane, which can cause edge artifacts.
    - The image color space is changed from **sRGB** to **Raw** to prevent color corrections from affecting depth.

- **Plane Modifications**:
  - The Plane is subdivided into a mesh:
    - Original add-on: 6 levels of subdivision.
    - Modified version: Increased to 8 levels.
  - The Plane is curved using a **Deform Modifier** to correct for Camera Field of View distortions:
    - Modifier is anchored to an empty object for easier orientation of deformations.
    - Both the modifier and the empty object are additions to the original code.
  - The Plane is displaced using a **Displacement Modifier** with reference to the Depth Map Texture.

- **Rendering**:
  - Rendering can be performed with the faster **Eevee Render Engine**, as light/material interaction is unnecessary. This avoids unwanted artifacts introduced by more complex rendering engines.

---

## Additional Functionality (Not Covered in the Tutorial)

- Importing of Panoramas.
- Automatic Camera Rig Setup.

---

## Acknowledgements

A big shoutout to **Elin (Ladypoly)** for making the original code available under the GNU licensing.

