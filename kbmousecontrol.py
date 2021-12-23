import sys
import pyautogui
import time

MOVE_ARG = "m"
MOVE_REL_ARG = "mr"
DRAG_ARG = "d"
DRAG_REL_ARG = "dr"
LCLICK_ARG = "lc"
RCLICK_ARG = "rc"
DOUBLE_CLICK_ARG = "dc"
GET_POS_ARG = "getpos"
TYPE_ARG = "type"
COPY_ARG = "copy"
PASTE_ARG = "paste"
KEYDOWN_ARG = "keydown"
KEYUP_ARG = "keyup"
DELAY_ARG = "delay"

# Change these values to the region of the window
xMin = 100
xMax = 850
yMin = 100
yMax = 600

# This is some buffer room for the mouse
padding = 10

def key_down(*args):
    pyautogui.keyDown(str(args[0]))
    pass

def key_up(*args):
    pyautogui.keyUp(str(args[0]))
    pass

def copy_msg(*args):
    pyautogui.hotkey('ctrl', 'c')
    pass

def paste_msg(*args):
    pyautogui.hotkey('ctrl', 'v')
    pass

def type_msg(*args):
    msg = str(args[0])    
    
    if len(args) > 1:
        msg = " ".join(args)

    pyautogui.typewrite(msg, interval=0.05)
    pass

def double_click(*args):
    m.double_click(str(args[0]))
    pass

def rightclick():
    pyautogui.rightClick()
    pass

def leftclick():
    pyautogui.click()
    pass

def dragmouse(*args):
    newMouseLocation = (int(args[0]), int(args[1]))
    if(isPointOutOfBounds(newMouseLocation) is False): # if new pos isn't out of bounds move to new pos
        pyautogui.dragTo(newMouseLocation[0], newMouseLocation[1], duration=1)
    else:
        print("Cannot move mouse to position (" + str(newMouseLocation[0]) + ", " + str(newMouseLocation[1]) + ") - Out of bounds", file=sys.stderr)       
    
    #time.sleep(float(args[4]))
    #clampmouse()
    pass

def dragmouserel(*args):
    currentMousePos = pyautogui.position()
    newMouseLocation = (int(args[0]) + currentMousePos[0], int(args[1]) + currentMousePos[1])
    if(isPointOutOfBounds(newMouseLocation) is False):
        pyautogui.dragTo(int(args[0]), int(args[1]), duration=1)
    else:
        print("Cannot move mouse to position (" + str(newMouseLocation[0]) + ", " + str(newMouseLocation[1]) + ") - Out of bounds", file=sys.stderr)
    #time.sleep(float(args[2]))
    #clampmouse()
    pass

def movemouse(*args):
    newMouseLocation = (int(args[0]), int(args[1]))
    if(isPointOutOfBounds(newMouseLocation) is False): # if new pos isn't out of bounds move to new pos
        pyautogui.moveTo(newMouseLocation[0], newMouseLocation[1])
    else:
        print("Cannot move mouse to position (" + str(newMouseLocation[0]) + ", " + str(newMouseLocation[1]) + ") - Out of bounds", file=sys.stderr)
    
    #time.sleep(0)    
    #clampmouse()
    pass

def movemouserel(*args):
    currentMousePos = pyautogui.position()
    newMouseLocation = (int(args[0]) + currentMousePos[0], int(args[1]) + currentMousePos[1])
    if(isPointOutOfBounds(newMouseLocation) is False):
        pyautogui.moveTo(newMouseLocation[0], newMouseLocation[1])
    else:
        print("Cannot move mouse to position (" + str(newMouseLocation[0]) + ", " + str(newMouseLocation[1]) + ") - Out of bounds", file=sys.stderr)
    
    #time.sleep(0)    
    #clampmouse()
    pass

def execution_delay(*args):
    time.sleep(float(args[0]))

def getpos(*args):
    print(str(pyautogui.position()), file=sys.stderr)

def clampmouse():
    pos = pyautogui.position()
        
    curX = pos[0]
    curY = pos[1]

    if curX < xMin:
        pyautogui.moveTo(xMin + padding, curY)        
    elif curX > xMax:
        pyautogui.moveTo(xMax - padding, curY)

    curX = pyautogui.position()[0]

    if curY < yMin:
        pyautogui.moveTo(curX, yMin + padding)
    elif curY > yMax:
        pyautogui.moveTo(curX, yMax - padding)

def isPointInBox(box, point):
    left = box[0]
    top = box[1]
    width = box[2]
    height = box[3]

    isInHorizontalBounds = (point[0] >= left and point[0] < left + width)
    isInVerticalBounds = (point[1] >= top and point[1] < top + height)

    if(isInHorizontalBounds and isInVerticalBounds):
        return True
    else:
        return False

def isPointOutOfBounds(point):
    if(point[0] < 0 or point[1] < 0): # off left or above top screen edge
        return True

    screenSize = pyautogui.size()
    if(point[0] >= screenSize[0] or point[1] >= screenSize[1]): # off right or bottom screen edge
        return True

    for boundingBox in OutOfBoundsBoxes:
        pointTuple = (point[0], point[1])
        if(isPointInBox(boundingBox, pointTuple)):
            return True
    return False

# Map function to name
FuncMap = { 
    MOVE_ARG: movemouse,
    MOVE_REL_ARG: movemouserel,
    DRAG_ARG: dragmouse,
    DRAG_REL_ARG: dragmouserel,
    LCLICK_ARG: leftclick,
    RCLICK_ARG: rightclick,
    DOUBLE_CLICK_ARG: double_click,
    GET_POS_ARG: getpos,
    TYPE_ARG: type_msg,
    COPY_ARG: copy_msg,
    PASTE_ARG: paste_msg,
    KEYDOWN_ARG: key_down,
    KEYUP_ARG: key_up,
    DELAY_ARG: execution_delay 
}

# Map argument count to function
ArgCountMap = {
    MOVE_ARG: 2,
    MOVE_REL_ARG: 2,
    DRAG_ARG: 2,
    DRAG_REL_ARG: 2,
    LCLICK_ARG: 0,
    RCLICK_ARG: 0,
    DOUBLE_CLICK_ARG: 1,
    GET_POS_ARG: 0,
    TYPE_ARG: -1,
    COPY_ARG: 0,
    PASTE_ARG: 0,
    KEYDOWN_ARG: 1,
    KEYUP_ARG: 1,
    DELAY_ARG: 1
}

ArgTypeMap = {
    MOVE_ARG: "x y",
    MOVE_REL_ARG: "x y",
    DRAG_ARG: "x y",
    DRAG_REL_ARG: "x y",
    LCLICK_ARG: "",
    RCLICK_ARG: "",
    DOUBLE_CLICK_ARG: "mouse button (left or right)",
    GET_POS_ARG: "",
    TYPE_ARG: "",
    COPY_ARG: "",
    PASTE_ARG: "",
    KEYDOWN_ARG: "",
    KEYUP_ARG: "",
    DELAY_ARG: "time - seconds"
}

OutOfBoundsBoxes = [
    (0, 0, 1920, 100), # 100 pixel bar at the top of the screen
    (0, 0, 100, 1080), # 100 pixel bar down the left side of the screen
    (850, 0, 1070, 1080), # 1070 pixel bar down the right side of the screen
    (0, 600, 1920, 480) # 480 pixel bar across the bottom of the screen
]

def main():
    # Get all command line args
    input_args = sys.argv

    ## join the args into a string
    joined_args = " ".join(str(e) for e in input_args[1:])
    ## split into commands on ", "
    cmds = joined_args.split(", ")

    ##get a list of available commands
    availableCmds = ""
    for funcName in FuncMap:
        availableCmds += '"' + funcName + '", '
        availableCmds = availableCmds[:-2]

    for cmd in cmds:
        #split out the string cmd into a list
        args = cmd.split(" ")
        #remove the command itself for the number of arguments
        argCount = len(args) - 1

        mouseCmd = args[0]
        #check it is a valid command
        if mouseCmd in availableCmds:
            mouseCmdStr = '"' + mouseCmd + '"'
            try:
                # Get argument count from first argument
                reqArgs = ArgCountMap[mouseCmd]
                if reqArgs != -1 and (argCount < reqArgs or argCount > reqArgs):
                    print(mouseCmdStr + " requires " + str(reqArgs) + " arguments: " + '"' + ArgTypeMap[mouseCmd] + '"', file=sys.stderr)
                    sys.exit(1)
                
                func = FuncMap[mouseCmd]
                lst = args[1:]
                
                func(*lst)
            except KeyError:
                print("Invalid command: " + mouseCmdStr, file=sys.stderr) 
                sys.exit(2)
            except Exception as e:
                print("Error executing the " + mouseCmdStr + " mouse command: " + str(e), file=sys.stderr)
                sys.exit(1)
        else:
            print("No mouse command specified. Choose one of the following: " + availableCmds, file=sys.stderr)
            sys.exit(2)
    
if __name__ == "__main__":
    main()