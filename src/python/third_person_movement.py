import bge
from bge import logic
import math
import mathutils
import gamepad
import game_utils

originalColor = 1.0, 1.0, 1.0
correctColor = 0.0, 1.0, 0
wrongColor = 1.0, 0, 0



scene = bge.logic.getCurrentScene()
cube = scene.objects["character_cube"]
# cont = bge.logic.getCurrentController()
# sens = cont.sensors['Delay']


def main(controller, cam_control, camera, cam_plane, popup_list):
    obj = controller.owner
    #Set cam_lock
    if 'cam_lock' not in obj:
        obj['cam_lock'] = 'On'

    cam_position_control(controller, cam_control, cam_plane, camera)
    #obj.localLinearVelocity = movement(controller, cam_control)
    active_obj = toggle(camera, controller, cam_control, cam_plane, popup_list)

    return active_obj



#######################################################################

def cam_parameters (camera, cam_plane,  cam_control, controller, height, min, max, targetLoc, camLoc):
    obj = controller.owner
    controller = bge.logic.getCurrentController()
    plane_locked_cam = controller.actuators['plane_locked_cam']
    # obj = controller.owner
    plane_locked_cam.height = height
    plane_locked_cam.min = min
    plane_locked_cam.max = max
    obj.worldPosition  = targetLoc
    cam_plane.worldPosition = camLoc
    cam_control.worldPosition = targetLoc

    trans_speed = [0, 0, 0]
    for i in range(0, 3):
        trans_speed[i] = abs(camera.worldPosition[i] - cam_plane.worldPosition[i])/5  #lower number = faster camera
        if trans_speed[i] < .1:
            trans_speed[i] = .1

    #game_utils.gradual_set_position(camera, cam_plane.worldPosition, trans_speed)
    camera.worldPosition = cam_plane.worldPosition
    camera.removeParent()

    controller.activate(controller.actuators['plane_locked_cam'])
    controller.activate(controller.actuators['find_cam_control'])
    cam_plane.setParent(cam_control, True, True)
    scene.active_camera = camera

def cam_position_control(controller, cam_control, cam_plane, camera):
    """ rotates the camera parent so that the camera revolves around character
        pulling left trigger aligns camera orientation to character orientation.
        camera position is the hit point of the cam_control raycast unless occluding
        object has 'not_affect_cam' property.
    """
    obj = controller.owner

    #Set the rotate speed
    rotate_speed = 4
    #Get the camera actuator attached to the cam_plane
    plane_locked_cam = controller.actuators['plane_locked_cam']
    #This increment will make it so that the further the cam is from the target the faster it will fly
    #initialize trans_speed
    trans_speed = [0, 0, 0]
    for i in range(0, 3):
        trans_speed[i] = abs(camera.worldPosition[i] - cam_plane.worldPosition[i])/5  #lower number = faster camera
        if trans_speed[i] < .1:
            trans_speed[i] = .1
    #Remove camera parent
    camera.removeParent()

    #Activate the camera's track_to actuator
    controller.activate(controller.actuators['find_cam_control'])
    #controller.activate(controller.actuators['plane_locked_cam'])


    ##### TURN CAM LOCK OFF ####
    if obj['R_Y'] or obj['R_X']:
        obj['cam_lock'] = 'Off'

    #### TURN CAM LOCK ON ####
    if  gamepad.button_tap(obj, 'L_TRIGGER') and (obj['cam_lock'] == 'Off'):
        obj['cam_lock'] = 'On'

    #### ROTATE CAM_CONTROL ####

    cam_control.localOrientation = cam_control.localOrientation * mathutils.Matrix.Rotation(math.radians(rotate_speed * obj['R_Y']), 3, 'Z')

    #### MOVE CAM_PLANE BACKWARDS/FORWARDS ####
    if cam_plane.localPosition[1] < -20 and obj['R_X'] < 0:
        cam_plane.localPosition[1] -= obj['R_X']/2
    elif cam_plane.localPosition[1] > -40 and obj['R_X'] > 0:
        cam_plane.localPosition[1] -= obj['R_X']/2
    if cam_plane.localPosition[2] > 1 and obj['R_X'] < 0:
        cam_plane.localPosition[2] += obj['R_X']/2
    elif cam_plane.localPosition[2] < 10 and obj['R_X'] > 0:
        cam_plane.localPosition[2] += obj['R_X']/2

    #### SET CAM_PLANE PARENT ####
    if obj['cam_lock'] == 'Off' or obj['L_TRIGGER']:
        controller.deactivate(plane_locked_cam)
        cam_plane.setParent(cam_control, True, True)

    #### REMOVE CAM_PLANE PARENT ####
    if obj['cam_lock'] == 'On' and obj['L_TRIGGER'] == False:
        controller.activate(plane_locked_cam)
        cam_plane.removeParent()

    #### CAM_CONTROL FIND FRONT ####
    # if obj['L_TRIGGER'] and obj['cam_lock'] == 'On':
    #     controller.actuators['find_front'].time = 3
    #     controller.activate(controller.actuators['find_front'])
    #     #When the cam_control is close to reaching alignment, slow it down
    #     if (abs(cam_control.localOrientation.to_euler('XYZ')[2] - obj.localOrientation.to_euler('XYZ')[2]) < .25):
    #         controller.actuators['find_front'].time = 10
    #         controller.activate(controller.actuators['find_front'])
    # else:
    #         controller.deactivate(controller.actuators['find_front'])
    #
    # #### CAM_COTNROL FIND CAMERA ####
    # if obj['cam_lock'] == 'On' and obj['L_TRIGGER'] == False:
    #     game_utils.track_to(cam_control, camera, 180, 5, 2)
    #
    #### CAMERA's POSITION ####
    if cam_control.rayCast(cam_plane)[0] != None and cam_control.rayCast(cam_plane)[0] != cam_plane:
        #Any object that has 'not_affect_cam' won't cause camera to jump
        if 'not_affect_cam' not in cam_control.rayCast(cam_plane)[0]:
            # #If cam_control's raycast hitpoint is closer to cam_control than camera, the camera should jump to that position instantly
            # if cam_control.getDistanceTo(cam_control.rayCast(cam_plane)[0]) < cam_control.getDistanceTo(camera):
            #     camera.worldPosition = cam_control.rayCast(cam_plane)[1]
            #     obj['cam_set'] = 'Off'
            # #When hitpoint is further away from cam_control than camera, the camera should gradually get to that position
            # else:
                game_utils.gradual_set_position(camera, cam_control.rayCast(cam_plane)[1], trans_speed)
        #If passing by an object with 'not_affect_cam' and in cam_lock_mode, camera should match position of cam_plane
        elif 'not_affect_cam' in cam_control.rayCast(cam_plane)[0]:
            game_utils.gradual_set_position(camera, cam_plane.worldPosition, trans_speed)
    #Moving back to the plane should be somewhat gradual
    elif cam_control.rayCast(cam_plane)[0] == cam_plane and obj['cam_set'] == 'Off':
        game_utils.gradual_set_position(camera, cam_plane.worldPosition, trans_speed)
    elif cam_control.rayCast(cam_plane)[0] == None and obj['cam_set'] == 'Off':
        game_utils.gradual_set_position(camera, cam_plane.worldPosition, trans_speed)
        if camera.worldPosition == cam_plane.worldPosition:
            obj['cam_set'] = 'On'
    if obj['cam_set'] == 'On':
        camera.worldPosition = cam_plane.worldPosition


#######################################################################
def movement(controller, cam_control):
    """ return y and x velocity components based on cam_controller z orientation
    """
    obj = controller.owner
    #Get the current movement
    linX, linY, linZ = obj.localLinearVelocity

    if controller.sensors['earth'].positive:
        if obj['L_TRIGGER']:
            strafe_speed = obj['running']/2

            #normalize the cam_control's z orientation to be from 0 to 2pi radians
            cam_control_orientation = cam_control.localOrientation.to_euler('XYZ')[2]
            if cam_control_orientation < 0:
                cam_control_orientation = cam_control_orientation + (2* math.pi)

            #The localLinearVelocity on each axis depends on the vector created by camera angle
            linX = math.sin(cam_control_orientation) * obj['running']/2 * obj['L_Y'] + math.cos(cam_control_orientation) * obj['running']/2 * obj['L_X']
            linY = math.cos(cam_control_orientation) * obj['running']/2 * -obj['L_Y'] + math.sin(cam_control_orientation) * obj['running']/2 * obj['L_X']
        else:
            running_threshold = .75
            if obj['view_mode'] == 'THIRD_PERSON':
                #if only pressing up or down
                if obj['L_Y'] != 0 and obj['L_X'] == 0:
                    linY = abs(obj['L_Y']) * obj['running']
                #if only pressing right or left
                elif obj['L_Y'] == 0 and obj['L_X'] != 0:
                    linY = abs(obj['L_X']) * obj['running']
                #if pressing both right and left, sum the vector componects
                elif obj['L_Y'] != 0 and obj['L_X'] != 0:
                    linY = (abs(obj['L_Y']) * obj['running'] * (1/(math.sqrt(2)))) + (abs(obj['L_X']) * obj['running'] * (1/(math.sqrt(2))))
                else:
                    linY = 0
            linX = 0

    return [linX, linY, linZ]

#
def toggle(camera, controller, cam_control, cam_plane, popup_list):

    obj = controller.owner
    index = obj['index']
    targetLoc = (popup_list[index].position.x, popup_list[index].position.y, 0)
    cameraLoc = (targetLoc[0]-10, targetLoc[1]-10, 20)

    if gamepad.button_tap(obj, 'A_BUTTON'):
        obj['ACTIVE'] = popup_list[index]
        if index == len(popup_list) - 1:
            obj['index'] = 0
        else:
            obj['index'] += 1

        cam_parameters(camera, cam_plane, cam_control, controller, 15, 25, 40, targetLoc, cameraLoc)

        return (obj['ACTIVE'])


#######################################################################

#######################################################################
