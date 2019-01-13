import bge
import game_utils
import math
import gamepad

def main(controller, cam_control, camera, cam_plane, front_face):
    obj = controller.owner
    fp_cam_set(controller, camera, cam_control, cam_plane, front_face)
    fp_movement(controller, camera)
    obj.localLinearVelocity = jump(controller)

####################################################################### 

def fp_movement(controller, camera):
    """ Move the camera and the object depending on thumbstick_layout setting
    """
    obj = controller.owner
    
    #Defines witch axis control, STRAFE, FORWARD/BACK, LOOK UP/DOWN, TURN
    if obj['thumbstick_layout'] == 'DEFAULT':
        thumb = [obj['L_X'], obj['L_Y'], obj['R_Y'], obj['R_X']]
    elif obj['thumbstick_layout'] == 'LEGACY':
        thumb = [obj['R_X'], obj['L_Y'], obj['R_Y'], obj['L_X']]
    elif obj['thumbstick_layout'] == 'SOUTHPAW':
        thumb = [obj['R_X'], obj['R_Y'], obj['L_Y'], obj['L_X']]
    elif obj['thumbstick_layout'] == 'LEGACYSOUTHPAW':
        thumb = [obj['L_X'], obj['R_Y'], obj['L_Y'], obj['R_X']]
        
    turn_speed = .03
    #Strafe Left/Right
    if thumb[1] == 0:
        obj.localLinearVelocity.x = thumb[0] * obj['running']
    #Forward/Back Movement
    if thumb[0] == 0:
        obj.localLinearVelocity.y = thumb[1] * -obj['running']
    #Diagonal Movement
    if thumb[1] != 0 and thumb[0] != 0:
        obj.localLinearVelocity.x = thumb[0] * obj['running'] * (1/math.sqrt(2))
        obj.localLinearVelocity.y = thumb[1] * -obj['running'] * (1/math.sqrt(2))       
    #Look Up/Down
    camera.applyRotation(((thumb[2] * -turn_speed * obj['look_invert']), 0, 0), True)
    #Rotate Left/Right Movement
    obj.applyRotation((0, 0, (thumb[3] * -turn_speed)), True)

#######################################################################


def fp_cam_set(controller, camera, cam_control, cam_plane, front_face):
    """ Places camera at the front_face empty and adjusts orientation to match front_face.
        Parent's the camera to the front_face 
        deactivates camera's track_to actuator
        activates cam_rotate's find_front actuator
        sets obj['fp_mode'] to off when L_bumper is tapped.
    """ 
    obj = controller.owner
    
    if obj['cam_set'] == 'Off':
        obj = controller.owner
        #how fast the camera gets to it's new position/orientation. Lower is faster.
        set_speed = 5
        lower_limit = .15 #When camera is this close, it will jump to front_face's position
        
        cam_plane.setParent(cam_control, True, True)
        #Deactivate the camera actuator
        controller.deactivate(controller.actuators['plane_locked_cam'])
        #Activate the find_front actuator, so that when we come out of fp_mode, we are facing front
        controller.activate(controller.actuators['find_front'])
        
        #Set the camera's position and orientation to the front_face empty...gradually
        if camera.parent != front_face:
            #Set the orient and loc increment to be relative to the camera's orientation offset from front face (makes the swap very smooth.)
            orient_increment = [0, 0, 0]
            loc_increment = [0, 0, 0]
            for i in range(0, 3):
                orient_increment[i] = math.degrees(abs(camera.worldOrientation.to_euler('XYZ')[i] - front_face.worldOrientation.to_euler('XYZ')[i]))/set_speed
                loc_increment[i] = abs(camera.worldPosition[i] - front_face.worldPosition[i])/set_speed          
            #unparent the camera from the cam_control and switch off it's track_to actuator
            controller.deactivate(controller.actuators['find_cam_control'])
            game_utils.gradual_set_position(camera, front_face.worldPosition, loc_increment)
            game_utils.gradual_set_orientation(camera, front_face.worldTransform, [0, 0, 0], (orient_increment), [True, True, True])
            #When we're really close, parent the cam to the front_face
            if abs(camera.worldPosition[0] - front_face.worldPosition[0]) < lower_limit and abs(camera.worldPosition[1] - front_face.worldPosition[1]) < lower_limit and abs(camera.worldPosition[2] - front_face.worldPosition[2]) < lower_limit:
                camera.worldPosition = front_face.worldPosition
                camera.worldOrientation = front_face.worldOrientation
                camera.setParent(front_face, True, True)
                obj['cam_set'] = 'On'
                
#######################################################################

def jump(controller):
    obj = controller.owner
    linX, linY, linZ = obj.localLinearVelocity
    
    if controller.sensors['ground']:
        if gamepad.button_tap(obj, 'A_BUTTON'):
            linZ += obj['jump_force']
    return (linX, linY, linZ)
    