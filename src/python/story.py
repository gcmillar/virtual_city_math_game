import bge
import game_utils
import math
import gamepad
import json
import aud


def get_slide_data(slidePath):
    with open(slidePath) as f:
        data = json.load(f)
    return data

def get_grid_coords(obj, index):

    mesh = obj.meshes[0]
    #for index in range(mesh.getVertexArrayLength(0)):
    #vec_verts = map(lambda v: own.worldTransform * v.XYZ, _getVerts(own))
    v = mesh.getVertex(0, index)
    vec_verts = obj.worldTransform * v.XYZ
    return vec_verts.xyz
    # textObj =  listObj[index]
    # _movetext(textObj,index,vec_verts)


def main(controller, camera, camera_story, camera_test, scene, test_obj_dic, slidePath):

    obj = controller.owner

    if obj['STORY_MODE'] == 'TEST' :

        testObj = obj['Test_object']
        correctColor = obj['Correct_color']
        wrongColor = obj['Wrong_color']
        ratio = obj['Test_ratio']

        if obj["TEST"] == "ACTIVE":
            test_scale(testObj, obj, ratio, correctColor, wrongColor)

    elif obj['STORY_MODE'] == 'NORMAL' :
        obj["TEST"] = "INACTIVE"
        obj["SOLVED"] = "No"



    if gamepad.button_tap(obj, 'X_BUTTON') and obj['STORY_MODE'] == 'TEST' :
        obj["TEST"] = "ACTIVE"

    if gamepad.button_tap(obj, 'D_PAD_RIGHT') or gamepad.button_tap(obj, 'D_PAD_LEFT'):

        slide_data = get_slide_data(slidePath)
        total_slide_number = len([slide for slide in slide_data if "slide_" in slide])

        if obj['D_PAD_RIGHT']:
            if obj['SLIDE'] < total_slide_number:
                obj['SLIDE'] += 1

                currentSlide = str(obj['SLIDE'])
                currentSlideData = slide_data["slide_" + currentSlide]
                clean_scene (scene)
                slide_set(obj, currentSlideData, camera_story, camera_test, scene)

        if obj['D_PAD_LEFT']:
            if obj['SLIDE'] > 1:
                obj['SLIDE'] -= 1
                currentSlide = str(obj['SLIDE'])
                currentSlideData = slide_data["slide_" + currentSlide]
                clean_scene (scene)
                slide_set(obj, currentSlideData, camera_story, camera_test, scene)

    if gamepad.button_tap(obj, 'B_BUTTON'):
        obj['SLIDE'] = 0
        obj['view_mode'] = 'THIRD_PERSON'
        scene.active_camera = camera
        clean_scene (scene)
    #   hide_assets(gridObj,testObj, transparentPlane, scene)



#######################################################################


#######################################################################
def slide_set(obj,slideData, camera_story, camera_test, scene):

    backdrop = scene.objects["plane_backdrop"]
    dialObj = scene.objects["Text_dialogue"]

    avatarList = [slideData[av] for av in slideData if "avatar" in av]
    dialogueList = [slideData[diag] for diag in slideData if "dialogue" in diag]
    camera = slideData["camera"]

    if "backdrop" in slideData :
        backdrop.visible = True
    else :
        backdrop.visible = False

    if slideData ["id"] == "TEST":

        testObjName = "test_" + slideData["test_object"]
        testObj = scene.objects[testObjName]
        gridObj = scene.objects["grid_"+ testObjName]
        transparentPlane = scene.objects["Transparent_plane"]

        obj['Test_object'] = testObj
        obj['Test_ratio'] = slideData["test_ratio"]

        # camera_test.position.x = testObj.position.x
        # camera_test.position.y = testObj.position.y

        camera_story.position = (camera["location"][0], camera["location"][1],camera["location"][2])
        xyz = camera_story.localOrientation.to_euler()

        cam_rotation = camera["rotation"]
        xyz[0] = math.radians(cam_rotation[0])
        xyz[1] = math.radians(cam_rotation[1])
        xyz[2] = math.radians(cam_rotation[2])

        camera_story.localOrientation = xyz.to_matrix()
        scene.active_camera = camera_story

        load_test_env(gridObj, testObj, transparentPlane, scene)

        # scene.active_camera = camera_test

        obj['STORY_MODE'] = "TEST"

    elif slideData ["id"] == "STORY":

        obj['STORY_MODE'] = "NORMAL"
        camera_story.position = (camera["location"][0], camera["location"][1],camera["location"][2])
        xyz = camera_story.localOrientation.to_euler()

        cam_rotation = camera["rotation"]
        xyz[0] = math.radians(cam_rotation[0])
        xyz[1] = math.radians(cam_rotation[1])
        xyz[2] = math.radians(cam_rotation[2])

        camera_story.localOrientation = xyz.to_matrix()
        scene.active_camera = camera_story

    for avatar in avatarList:

        if avatar["status"] == "On":
            avatarObj = scene.objects[avatar["id"]]
            avatarObj.visible = True
            gridIndex = int(avatar["grid"])

            avatarObj.worldPosition =  get_grid_coords (backdrop, gridIndex)
            avatarObj.worldOrientation = backdrop.worldOrientation


    for dialogue in dialogueList :

        if dialogue["status"] == "On":

            if dialogue["id"] == "":
                dialBox = scene.objects["dialogue_box_default"]
            else:
                dialBox = scene.objects[dialogue["id"]]

            dialBox.visible = True
            gridIndex_box = int(dialogue["grid_box"])
            dialBox.worldPosition =  get_grid_coords (backdrop, gridIndex_box)

            gridIndex_text = int(dialogue["grid_text"])
            dialObj.worldPosition =  get_grid_coords (backdrop, gridIndex_text)
            dialObj.visible = True
            dialObj.resolution = 50

            if obj['STORY_MODE'] == "NORMAL":

                if dialogue["text"]:
                    dialObj.text = dialogue["text"]
                else :
                    dialObj.text = "No text available"

            elif obj['STORY_MODE'] == "TEST":

               # obj["prompt_Dialogue"] = dialogue
               #
               if obj['SOLVED'] == "Yes":
                    dialObj.text = dialogue["text_solved"]
                    print ("got here")
               else:
                    dialObj.text = dialogue["text"]
                    print ("got here_2")

    device = aud.device()
    sound = aud.Factory.file("Q:\\My Drive\\Projects_manuscripts\\Math_game_project\\london.wav")
    sound = sound.pitch(1)
    device.play(sound)

def test_scale(test_obj, obj, ratio, correctColor, wrongColor):


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

    if round(proportion,1) < ratio + 0.2 and round(proportion,1) > ratio - 0.2:
        test_obj.meshes[0].materials[0].diffuseColor = correctColor
        obj['SOLVED'] = "Yes"
    else:
        test_obj.meshes[0].materials[0].diffuseColor = wrongColor
        obj['SOLVED'] = "No"

    return proportion

def load_test_env(gridObj,testObj, transparentPlane, scene):

    testObj.position.z = 5
    gridObj.position.z = 4.5
    transparentPlane.position.z = 5

    gridObj.visible = True
    testObj.visible = True
    transparentPlane.visible = True


def clean_scene (scene):
    assets = ["grid_", "backdrop", "avatar_", "dialogue_", "Transparent_plane", "test_", "Text_dialogue" ]
    for obj in scene.objects:
        for item in assets:
            if item in obj.name:
                obj.visible = False


def camera_set(camera, location, scene):
    camera.position.x = location
    scene.active_camera = camera
