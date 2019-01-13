import bpy 
for img in bpy.data.images:
    if "Cher" in img.filepath:
        bpy.data.images.remove(img, do_unlink=True)