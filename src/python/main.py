import bge
import sys
path = bge.logic.expandPath("//")
pythonPath = sys.path.append(path + "/src/python")
configPath = path + "/src/config/config.json"
slidesPath = path + "/src/config/slides.json"


import mathutils
import math
import gamepad
import third_person_movement
import test
import json
import story


def main(controller):
    #get the objects associated with this script
    obj = controller.owner
    scene = bge.logic.getCurrentScene()
    cam_control = (bge.logic.getCurrentScene()).objects.get('cam_control')

    cam_plane = (bge.logic.getCurrentScene()).objects.get('cam_plane')
    camera = (bge.logic.getCurrentScene()).objects.get('Camera')
    camera_test = (bge.logic.getCurrentScene()).objects.get('Camera_test')
    camera_story = (bge.logic.getCurrentScene()).objects.get('Camera_story')
    front_face = (bge.logic.getCurrentScene()).objects.get('front_face')

    #get the xbox controller
    xbox = bge.logic.joysticks[0]
    #make the gamepad controls standard
    gamepad.init_gamepad(obj, xbox)
    #initialize object properties
    init_prop(obj)
    a = get_test_data (scene)

    popup_list = a[1]
    test_obj_dic = a[0]

    if obj['view_mode'] == 'THIRD_PERSON':
        third_person_movement.main(controller, cam_control, camera, cam_plane, popup_list)

    # if obj['view_mode'] == 'TEST':
    #     test.main(controller, camera, camera_test, scene, test_obj_dic)

    if obj['view_mode'] == 'STORY':
        story.main(controller, camera, camera_story, camera_test, scene, test_obj_dic, slidesPath)

    if gamepad.button_tap(obj, 'Y_BUTTON'):

        if obj['view_mode'] == 'THIRD_PERSON':
            obj['view_mode'] = 'STORY'

            # obj['cam_lock'] = 'On'
            # obj['cam_set'] = 'On'

    if gamepad.button_tap(obj, 'B_BUTTON') and obj['ACTIVE']:

        if obj['view_mode'] == 'THIRD_PERSON':
            obj['SLIDE'] = 0
            obj['view_mode'] = 'TEST'
            obj['cam_lock'] = 'On'
            obj['cam_set'] = 'On'


        elif obj['view_mode'] == 'TEST':

            targetLoc = (0, 0 ,0)
            camLoc = (-20,-30, 20)
            third_person_movement.cam_parameters(camera, cam_plane, cam_control, controller, 20, 40, 60, targetLoc, camLoc)
            obj['view_mode'] = 'THIRD_PERSON'
            test.main(controller, camera, camera_test, scene, test_obj_dic)
            obj['cam_lock'] = 'On'
            obj['TEST_MODE'] = "Off"
            # obj['cam_set'] = 'On'



##################-#####################################################


def get_test_data (scene):

    with open(configPath) as f:
        data = json.load(f)

    test_obj_dic = {"test_" + i["id"]: int(i["ratio"]) for i in data["testObjects"]}
    popup_list = [scene.objects[("popup_test_" + i["id"])] for i in data["testObjects"]]
    return test_obj_dic, popup_list

def init_prop(obj):
    """ Initialize a set of important variables
    """
    if 'Test_object' not in obj:
        obj['Test_object'] = "None"
    if 'Test_ratio' not in obj:
        obj['Test_ratio'] = 1
    if 'Correct_color' not in obj:
        obj['Correct_color'] = 0, 1.0, 0
    if 'Wrong_color' not in obj:
        obj['Wrong_color'] = 1.0, 0, 0
    if 'TEST' not in obj:
        obj["TEST"] = "INACTIVE"

    if 'Active_Dialogue' not in obj:
        obj['Active_Dialogue'] = {}

    if 'STORY_MODE' not in obj:
        obj['STORY_MODE'] = "NORMAL"

    if 'SOLVED' not in obj:
        obj['SOLVED'] = "No"

    if 'SLIDE' not in obj:
        obj['SLIDE'] = 0
    if 'ACTIVE' not in obj:
        obj['ACTIVE'] = None
    if 'TEST_MODE' not in obj:
        obj['TEST_MODE'] = "Off"
    #Set run speed
    if 'running' not in obj:
        obj['running'] = 20
    #Set jump force
    if 'jump_force' not in obj:
        obj['jump_force'] = 20
    #Toggles first person mode
    if 'view_mode' not in obj:
        obj['view_mode'] = 'THIRD_PERSON'
    #The fp thumbstick layout
    if 'thumbstick_layout' not in obj:
        obj['thumbstick_layout'] = 'DEFAULT' #can be DEFAULT, LEGACY, SOUTHPAW, or LEGACYSOUTHPAW
    #Look invert for fp_mode
    if 'look_invert' not in obj:
        #1 = not inverted, -1 = inverted
        obj['look_invert'] = 1
    #When Camera has reached its destined position
    if 'cam_set' not in obj:
        obj['cam_set'] = 'Off'
    if 'index' not in obj:
        obj['index'] = 0

#######################################################################
