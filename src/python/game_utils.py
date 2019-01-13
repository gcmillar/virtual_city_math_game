import bge
import mathutils
import math

def track_to(obj, target, offset, damping, axis):
    """ Adjusts object's localOrientation until it points at target object
        along 1 axis the other two axis are made to be 0.
        Parameters: KX_GameObject, Target's Name (String), Offset (Degrees),
        Damp amount (Degrees), Axis (int: 0, 1, or 2)
    """
    #Get target's x distance from obj
    targetX = target.worldPosition[0] - obj.worldPosition[0]
    #Get target's y distance from obj
    targetY = target.worldPosition[1] - obj.worldPosition[1]
    #Get target's y distance from obj
    targetZ = target.worldPosition[2]
    if axis == 0:
        #Calculate the goal X angle
        goal = math.atan2(targetZ, targetY)
        #Make a string version of axis
        axis_string = 'X'
    elif axis == 1:
        #Calculate the goal Y angle
        goal = math.atan2(targetX, targetZ)
        #Make a string version of axis
        axis_string = 'Y'
    elif axis == 2:
        #Calculate the goal Z angle
        goal = math.atan2(targetY, targetX)
        #Make a string version of axis
        axis_string = 'Z'
    #adjust goal angle for offset
    goal -= math.pi/2 + math.radians(offset)
    #Set obj's orientation to equal goal_angle
    current = obj.localOrientation.to_euler('XYZ')[axis]
    #convert damping to radians
    increment = math.radians(damping)
    #Rotation list
    rotation_list = [0, 0, 0]
    #if current + 2pi is closer to goal_angle, do it
    if (abs((current + (2 * math.pi)) - goal) < abs(current - goal)):
        current += (2 * math.pi)
    #if current - 2pi is closer to goal_angle, do it
    elif (abs((current - (2 * math.pi)) - goal) < abs(current - goal)):
        current -= (2 * math.pi)

    #add to current orientation until it is aligned with goal
    if (current < goal) and ((current + increment) < goal):
        obj.localOrientation = mathutils.Matrix.Rotation((current + increment), 3, axis_string)
    elif (current > goal) and ((current - increment) > goal):
        obj.localOrientation = mathutils.Matrix.Rotation((current-increment), 3, axis_string)
    else:
        obj.localOrientation = mathutils.Matrix.Rotation(goal, 3, axis_string)

#######################################################################

def gradual_set_position(obj, vector, increment):
    """ Gradually sets the obj's position to the given vector
        by adding/subtracting increment (float) every logic tick
    """
    for i in range(0, 3):
        #if we're less than the goal and + increment doesn't put us over, do it
        if (obj.worldPosition[i] < vector[i]) and (obj.worldPosition[i] + increment[i]) < vector[i]:
            obj.worldPosition[i] += increment[i]
        #if we're greater than the goal and - increment doesn't put us under, do it
        elif (obj.worldPosition[i] > vector[i]) and (obj.worldPosition[i] - increment[i]) > vector[i]:
            obj.worldPosition[i] -= increment[i]
        #if neither of the above cases are True, then we must be in range to set equal
        else:
            obj.worldPosition[i] = vector[i]

#######################################################################

def gradual_set_orientation(obj, transform_matrix, offset, increment, axis):
    """ Gradually sets the orientation of the obj to the orientation in the transform matrix
        obj = the object whose orientation you want to change
        transform_matrix = the transform matrix that is the target orientation
        offset (list of degrees [x, y, z]) = the amount you would like to offset the end orientation
        increment (list of degrees [x, y, z]) = the speed at which each angle will change
        axis (list of boolean [x, y, z]) = the axis that will be changed
    """
    #Get the object's current orientation as a euler
    obj_rot = obj.worldTransform.decompose()[1].to_euler('XYZ')
    former_rot = obj.worldTransform.decompose()[1].to_euler('XYZ')
    #Get the goal orientation as a euler
    goal_rot = transform_matrix.decompose()[1].to_euler('XYZ')

    for i in range(0, 3):
        #Change increment and offset to radians
        increment[i] = math.radians(increment[i])
        offset[i] = math.radians(offset[i])

        #if + 2pi is closer to goal angle, do it
        if (abs((obj_rot[i] + (2 * math.pi)) - goal_rot[i]) < abs(obj_rot[i] - goal_rot[i])):
            obj_rot[i] += (2 * math.pi)
        #if - 2pi is closer to goal_angle, do it
        elif (abs((obj_rot[i] - (2 * math.pi)) - goal_rot[i]) < abs(obj_rot[i] - goal_rot[i])):
            obj_rot[i] -= (2 * math.pi)

        #+/- to current orientation to get it closer to goal
        if (obj_rot[i] < goal_rot[i]) and ((obj_rot[i] + increment[i]) < goal_rot[i]):
            obj_rot[i] += increment[i] + offset[i]
        elif (obj_rot[i] > goal_rot[i]) and ((obj_rot[i] - increment[i]) > goal_rot[i]):
            obj_rot[i] -= increment[i] + offset[i]
        else:
            obj_rot[i] = goal_rot[i] + offset[i]
        #Only affectuate an orientation change along the desire axis
        if axis[i] == False:
            obj_rot[i] = former_rot[i]

    obj.localOrientation = obj_rot
