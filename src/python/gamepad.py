import sys

def init_gamepad(obj, gamepad):
    """
        PARAMETERS: obj: the game object this script is applied to
                    gamepad: the xbox controller
    """
    #Get the os:
    os = sys.platform[0:3] #win, dar, or lin
    
    #Joystick movement below this threshold will not be considered
    active_threshold = .25
    
    #Create a variable for each possible xbox controller input
    #Because the HOME button does not work in windows, I have omitted it.    
    #Also, windows treats left and right triggers as though they were one axis, they cancel eachother when both are pressed....
    
    #Left Joystick
    if 'L_Y' not in obj:
        obj['L_Y'] = 0.0
    if 'L_X' not in obj:
        obj['L_X'] = 0.0    
    #Right Joystick
    if 'R_Y' not in obj:
        obj['R_Y'] = 0.0
    if 'R_X' not in obj:
        obj['R_X'] = 0.0        
    #D_PAD
    if 'D_PAD_UP' not in obj:
        obj['D_PAD_UP'] = False
    if 'D_PAD_DOWN' not in obj:
        obj['D_PAD_DOWN'] = False
    if 'D_PAD_RIGHT' not in obj:
        obj['D_PAD_RIGHT'] = False
    if 'D_PAD_LEFT' not in obj:
        obj['D_PAD_LEFT'] = False
    #Triggers (These will be treated as buttons instead of axis)
    if 'L_TRIGGER' not in obj:
        obj['L_TRIGGER'] = False
    if 'R_TRIGGER' not in obj:
        obj['R_TRIGGER'] = False
    #Buttons
    if 'A_BUTTON' not in obj:
        obj['A_BUTTON'] = False
    if 'B_BUTTON' not in obj:
        obj['B_BUTTON'] = False
    if 'X_BUTTON' not in obj:
        obj['X_BUTTON'] = False
    if 'Y_BUTTON' not in obj:
        obj['Y_BUTTON'] = False
    if 'L_BUMPER' not in obj:
        obj['L_BUMPER'] = False
    if 'R_BUMPER' not in obj:
        obj['R_BUMPER'] = False
    if 'BACK_BUTTON' not in obj:
        obj['BACK_BUTTON'] = False
    if 'START_BUTTON' not in obj:
        obj['START_BUTTON'] = False
    if 'L_JS_BUTTON' not in obj:
        obj['L_JS_BUTTON'] = False
    if 'R_JS_BUTTON' not in obj:
        obj['R_JS_BUTTON'] = False
        
    #If running on Windows:
    if os == 'win':
        #Left joystick
        if abs(gamepad.axisValues[1]) > active_threshold:
            obj['L_Y'] = gamepad.axisValues[1]
        else: 
            obj['L_Y'] = 0
        if abs(gamepad.axisValues[0]) > active_threshold:
            obj['L_X'] = gamepad.axisValues[0]
        else:
             obj['L_X'] = 0
        #Right joystick
        if abs(gamepad.axisValues[3]) > active_threshold:
            obj['R_Y'] = gamepad.axisValues[3]
        else:
             obj['R_Y'] = 0
        if abs(gamepad.axisValues[4]) > active_threshold:
            obj['R_X'] = gamepad.axisValues[4]
        else:
             obj['R_X'] = 0
        #Triggers:
        if gamepad.axisValues[2] > active_threshold:
            obj['L_TRIGGER'] = True
        else:
             obj['L_TRIGGER'] = False
        if gamepad.axisValues[2] < -active_threshold:
            obj['R_TRIGGER'] = True
        else:
             obj['R_TRIGGER'] = False
        #D-Pad
        if gamepad.hatValues[0] == 1:
            obj['D_PAD_UP'] = True
        else:
             obj['D_PAD_UP'] = False
        if gamepad.hatValues[0] == 2:
            obj['D_PAD_RIGHT'] = True
        else:
             obj['D_PAD_RIGHT'] = False
        if gamepad.hatValues[0] == 8:
            obj['D_PAD_LEFT'] = True
        else:
             obj['D_PAD_LEFT'] = False
        if gamepad.hatValues[0] == 4:
            obj['D_PAD_DOWN'] = True
        else:
             obj['D_PAD_DOWN'] = False
        #Buttons
        if 0 in gamepad.activeButtons:
            obj['A_BUTTON'] = True
        else:
             obj['A_BUTTON'] = False
        if 1 in gamepad.activeButtons:
            obj['B_BUTTON'] = True
        else: 
            obj['B_BUTTON'] = False
        if 2 in gamepad.activeButtons:
            obj['X_BUTTON'] = True
        else:
            obj['X_BUTTON'] = False
        if 3 in gamepad.activeButtons:
            obj['Y_BUTTON'] = True
        else:
            obj['Y_BUTTON'] = False
        if 4 in gamepad.activeButtons:
            obj['L_BUMPER'] = True
        else:
            obj['L_BUMPER'] = False
        if 5 in gamepad.activeButtons:
            obj['R_BUMPER'] = True
        else:
            obj['R_BUMPER'] = False
        if 6 in gamepad.activeButtons:
            obj['BACK_BUTTON'] = True
        else:
            obj['BACK_BUTTON'] = False
        if 7 in gamepad.activeButtons:
            obj['START_BUTTON'] = True
        else:
            obj['START_BUTTON'] = False
        if 8 in gamepad.activeButtons:
            obj['L_JS_BUTTON'] = True
        else:
            obj['L_JS_BUTTON'] = False
        if 9 in gamepad.activeButtons:
            obj['R_JS_BUTTON'] = True
        else:
            obj['R_JS_BUTTON'] = False
    #If running on MAC
    elif os == 'dar':
        #Left joystick
        if abs(gamepad.axisValues[1]) > active_threshold:
            obj['L_Y'] = gamepad.axisValues[1]
        else:
             obj['L_Y'] = 0
        if abs(gamepad.axisValues[0]) > active_threshold:
            obj['L_X'] = gamepad.axisValues[0]
        else:
             obj['L_X'] = 0
        #Right joystick
        if abs(gamepad.axisValues[3]) > active_threshold:
            obj['R_Y'] = gamepad.axisValues[3]
        else:
             obj['R_Y'] = 0
        if abs(gamepad.axisValues[2]) > active_threshold:
            obj['R_X'] = gamepad.axisValues[2]
        else:
             obj['R_X'] = 0
        #Triggers
        if gamepad.axisValues[4] > active_threshold:
            obj['L_TRIGGER'] = True
        else:
            obj['L_TRIGGER'] = False
        if gamepad.axisValues[5] > active_threshold:
            obj['R_TRIGGER'] = True
        else:
            obj['R_TRIGGER'] = False
        #D-Pad
        if 0 in gamepad.activeButtons:
            obj['D_PAD_UP'] = True
        else:
            obj['D_PAD_UP'] = False
        if 1 in gamepad.activeButtons:
            obj['D_PAD_DOWN'] = False
        else:
            obj['D_PAD_DOWN'] = False
        if 2 in gamepad.activeButtons:
            obj['D_PAD_LEFT'] = True
        else:
            obj['D_PAD_LEFT'] = False
        if 3 in gamepad.activeButtons:
            obj['D_PAD_RIGHT'] = True
        else:
            obj['D_PAD_RIGHT'] = False
        #Buttons
        if 4 in gamepad.activeButtons:
            obj['START_BUTTON'] = True
        else:
            obj['START_BUTTON'] = False
        if 5 in gamepad.activeButtons:
            obj['BACK_BUTTON'] = True
        else:
            obj['BACK_BUTTON'] = False
        if 6 in gamepad.activeButtons:
            obj['L_JS_BUTTON'] = True
        else: 
            obj['L_JS_BUTTON'] = False
        if 7 in gamepad.activeButtons:
            obj['R_JS_BUTTON'] = True
        else:
            obj['R_JS_BUTTON'] = False
        if 8 in gamepad.activeButtons:
            obj['L_BUMPER'] = True
        else:
            obj['L_BUMPER'] = False
        if 9 in gamepad.activeButtons:
            obj['R_BUMPER'] = True
        else:
            obj['R_BUMPER'] = False
        #if 10 in xbox.activeButtons:
            #obj['HOME_BUTTON'] = True
        #else:
            #obj['HOME_BUTTON'] = False
        if 11 in gamepad.activeButtons:
            obj['A_BUTTON'] = True
        else:
            obj['A_BUTTON'] = False
        if 12 in gamepad.activeButtons:
            obj['B_BUTTON'] = True
        else:
            obj['B_BUTTON'] = False
        if 13 in gamepad.activeButtons:
            obj['X_BUTTON'] = True
        else: 
            obj['X_BUTTON'] = False
        if 14 in gamepad.activeButtons:
            obj['Y_BUTTON'] = True
        else:
            obj['Y_BUTTON'] = False
    #If running on Linux
    elif os == 'lin': 
            #Left joystick
        if abs(gamepad.axisValues[1]) > active_threshold:
            obj['L_Y'] = gamepad.axisValues[1]
        else: 
            obj['L_Y'] = 0
        if abs(gamepad.axisValues[0]) > active_threshold:
            obj['L_X'] = gamepad.axisValues[0]
        else:
             obj['L_X'] = 0
        #Right joystick
        if abs(gamepad.axisValues[3]) > active_threshold:
            obj['R_X'] = gamepad.axisValues[3]
        else:
             obj['R_X'] = 0
        if abs(gamepad.axisValues[4]) > active_threshold:
            obj['R_Y'] = gamepad.axisValues[4]
        else:
             obj['R_Y'] = 0
        #Triggers:
        if gamepad.axisValues[2] > active_threshold:
            obj['L_TRIGGER'] = True
        else:
             obj['L_TRIGGER'] = False
        if gamepad.axisValues[5] < active_threshold:
            obj['R_TRIGGER'] = True
        else:
             obj['R_TRIGGER'] = False
        #D-Pad
        if 11 in gamepad.activeButtons:
            obj['D_PAD_LEFT'] = True
        else:
             obj['D_PAD_LEFT'] = False
        if 12 in gamepad.activeButtons:
            obj['D_PAD_RIGHT'] = True
        else:
             obj['D_PAD_RIGHT'] = False
        if 13 in gamepad.activeButtons:
            obj['D_PAD_UP'] = True
        else:
             obj['D_PAD_UP'] = False
        if 14 in gamepad.hatValues:
            obj['D_PAD_DOWN'] = True
        else:
             obj['D_PAD_DOWN'] = False
        #Buttons
        if 0 in gamepad.activeButtons:
            obj['A_BUTTON'] = True
        else:
             obj['A_BUTTON'] = False
        if 1 in gamepad.activeButtons:
            obj['B_BUTTON'] = True
        else: 
            obj['B_BUTTON'] = False
        if 2 in gamepad.activeButtons:
            obj['X_BUTTON'] = True
        else:
            obj['X_BUTTON'] = False
        if 3 in gamepad.activeButtons:
            obj['Y_BUTTON'] = True
        else:
            obj['Y_BUTTON'] = False
        if 4 in gamepad.activeButtons:
            obj['L_BUMPER'] = True
        else:
            obj['L_BUMPER'] = False
        if 5 in gamepad.activeButtons:
            obj['R_BUMPER'] = True
        else:
            obj['R_BUMPER'] = False
        if 6 in gamepad.activeButtons:
            obj['BACK_BUTTON'] = True
        else:
            obj['BACK_BUTTON'] = False
        if 7 in gamepad.activeButtons:
            obj['START_BUTTON'] = True
        else:
            obj['START_BUTTON'] = False
        #if 8 in xbox.activeButtons:
        #    obj['HOME_BUTTON'] = True
        #else:
        #    obj['HOME_BUTTON'] = False
        if 9 in gamepad.activeButtons:
            obj['L_JS_BUTTON'] = True
        else:
            obj['L_JS_BUTTON'] = False
        if 10 in gamepad.activeButtons:
            obj['R_JS_BUTTON'] = True
        else:
            obj['R_JS_BUTTON'] = False
        
        
        
#######################################################################

def button_tap(obj, key):
    """ obj = the object that the xbox controls
        xbox = the gamepad
        key = the name of the button being pressed
    """      
    #Create object properties for XBOX Buttons status:
    #D_PAD
    if 'D_PAD_UP_status' not in obj:
        obj['D_PAD_UP_status'] = 'Off'
    if 'D_PAD_DOWN_status' not in obj:
        obj['D_PAD_DOWN_status'] = 'Off'
    if 'D_PAD_RIGHT_status' not in obj:
        obj['D_PAD_RIGHT_status'] = 'Off'
    if 'D_PAD_LEFT_status' not in obj:
        obj['D_PAD_LEFT_status'] = 'Off'
    #Triggers (These will be treated as buttons instead of axis)
    if 'L_TRIGGER_status' not in obj:
        obj['L_TRIGGER_status'] = 'Off'
    if 'R_TRIGGER_status' not in obj:
        obj['R_TRIGGER_status'] = 'Off'
    #Buttons
    if 'A_BUTTON_status' not in obj:
        obj['A_BUTTON_status'] = 'Off'
    if 'B_BUTTON_status' not in obj:
        obj['B_BUTTON_status'] = 'Off'
    if 'X_BUTTON_status' not in obj:
        obj['X_BUTTON_status'] = 'Off'
    if 'Y_BUTTON_status' not in obj:
        obj['Y_BUTTON_status'] = 'Off'
    if 'L_BUMPER_status' not in obj:
        obj['L_BUMPER_status'] = 'Off'
    if 'R_BUMPER_status' not in obj:
        obj['R_BUMPER_status'] = 'Off'
    if 'BACK_BUTTON_status' not in obj:
        obj['BACK_BUTTON_status'] = 'Off'
    if 'START_BUTTON_status' not in obj:
        obj['START_BUTTON_status'] = 'Off'
    if 'L_JS_BUTTON_status' not in obj:
        obj['L_JS_BUTTON_status'] = 'Off'
    if 'R_JS_BUTTON_status' not in obj:
        obj['R_JS_BUTTON_status'] = 'Off'
    
    #If button was off, but now active, switch it's status and return True
    if obj[key + '_status'] == 'Off' and obj[key] == True:
        obj[key + '_status'] = 'On'
        return True
    #If button was on, and is still active, return false
    elif obj[key + '_status'] == 'On' and obj[key] == True:
        return False
    #If button was on, and is not active anymore, switch it's status and return False
    elif obj[key + '_status'] == 'On' and obj[key] == False:
        obj[key + '_status'] = 'Off'
        return False
    elif obj[key + '_status'] == 'Off' and obj[key] == False:
        return False
        
#######################################################################          
    
    
            
        