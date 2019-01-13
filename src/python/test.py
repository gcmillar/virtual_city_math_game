import bge
import game_utils
import math
import gamepad


def main(controller, camera, camera_test, scene, test_obj_dic):

    originalColor = 1.0, 1.0, 1.0
    correctColor = 0.0, 1.0, 0
    wrongColor = 1.0, 0, 0

    obj = controller.owner
    testObjName = obj['ACTIVE'].name.lstrip("popup_")
    testObj = obj['ACTIVE']
    gridObj = scene.objects["grid_"+ testObjName]
    testObj = scene.objects[testObjName]
    transparentPlane = scene.objects["PLANE"]
    ratio = test_obj_dic[testObjName]
    # test_color(controller, camera, cam_control, cam_plane, front_face)
    # change_scale(controller, camera)

    if obj['view_mode'] == 'TEST':
        camera_set(camera_test, testObj, scene)
        test_background (gridObj, testObj, transparentPlane, scene)
        test_scale(testObj, obj, ratio, correctColor, wrongColor)

    if obj['view_mode'] == 'THIRD_PERSON':
        hide_assets(gridObj,testObj, transparentPlane, scene)



#######################################################################


#######################################################################
def test_scale(test_obj, obj, ratio, correctColor, wrongColor):

    if obj["L_TRIGGER"] or obj["R_TRIGGER"] :
        obj["TEST_MODE"] = "On"

    if obj['R_Y'] > .40 and obj['R_X'] == 0:
        test_obj.localScale.x +=.05
    #push left on left joystick (and up or down)
    elif obj['R_Y'] < -.40 and obj['R_X'] == 0:
        test_obj.localScale.x -=.05
    #push up and only up
    if obj['L_Y'] < -.40 and obj['L_X'] == 0:
        test_obj.localScale.y +=.05
    #push down and only down
    if obj['L_Y'] > .4 and obj['L_X'] == 0:
        test_obj.localScale.y -=.05

    proportion =  test_obj.localScale.y/test_obj.localScale.x

    if obj["TEST_MODE"] == "On":

        if round(proportion,1) < ratio + 0.2 and round(proportion,1) > ratio - 0.2:
            test_obj.meshes[0].materials[0].diffuseColor = correctColor
        else:
            test_obj.meshes[0].materials[0].diffuseColor = wrongColor

    return proportion


def hide_assets(gridObj, testObj, transparentPlane, scene):

    gridObj.visible = False
    testObj.visible = False
    transparentPlane.visible = False
    for obj in scene.objects:
         if "popup_test" in obj.name:
             obj.visible = True

def camera_set(camera_test, testObj, scene):

    camera_test.position.x = testObj.position.x
    camera_test.position.y = testObj.position.y
    scene.active_camera = camera_test



def test_background(gridObj,testObj, transparentPlane, scene):

    testObj.position.z = 5
    gridObj.position.z = 4.5
    transparentPlane.position.z = 5

    gridObj.visible = True
    testObj.visible = True
    transparentPlane.visible = True

    for obj in scene.objects:
         if "popup_test" in obj.name:
             obj.visible = False
