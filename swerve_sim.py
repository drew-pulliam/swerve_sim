import pygame
import math
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 
 
class TextPrint(object):
    """
    This is a simple class that will help us print to the screen
    It has nothing to do with the joysticks, just outputting the
    information.
    """
    def __init__(self):
        """ Constructor """
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pygame.font.Font(None, 20)
 
    def print(self, my_screen, text_string):
        """ Draw text onto the screen. """
        text_bitmap = self.font.render(text_string, True, BLACK)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height
 
    def reset(self):
        """ Reset text to the top of the screen. """
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15
 
    def indent(self):
        """ Indent the next line of text """
        self.x_pos += 10
 
    def unindent(self):
        """ Unindent the next line of text """
        self.x_pos -= 10
 
 
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [600, 600]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Initialize the joysticks
pygame.joystick.init()
 
# Get ready to print
textPrint = TextPrint()

def drawVector(startVec,x,y,color):
    global vectorMult
    end = startVec + pygame.math.Vector2(x*vectorMult,y*vectorMult)
    pygame.draw.line(screen, color, startVec, end)

def drawBox(fl,fr,bl,br):
    #inputs need to be vectors
    pygame.draw.line(screen, RED, fl, fr)
    pygame.draw.line(screen, BLACK, fr, br)
    pygame.draw.line(screen, BLACK, bl, br)
    pygame.draw.line(screen, BLACK, fl, bl)

def limitAng(ang):
    while ang < -180:
        ang += 360
    while ang > 180:
        ang -= 360
    return ang

robotWidth = 50
robotLength = 50

speed_scalar = 4
showVecAddition = False
move = True
robotCentric = False

if not move:
    showVecAddition = True
    robotCentric = False
    robotWidth = 200
    robotLength = 200

centerx = 250
centery = 300
vectorMult = robotWidth / 2
leftx = centerx - (robotWidth / 2)
rightx = centerx + (robotWidth / 2)
fronty = centery - (robotLength / 2)
backy = centery + (robotLength / 2)

flvec = pygame.math.Vector2(leftx,fronty)
frvec = pygame.math.Vector2(rightx,fronty)
blvec = pygame.math.Vector2(leftx,backy)
brvec = pygame.math.Vector2(rightx,backy)
robotCenter = pygame.math.Vector2(centerx,centery)

flang = limitAng(pygame.math.Vector2().angle_to(robotCenter-flvec))
frang = limitAng(flang + 90)
blang = limitAng(flang - 90)
brang = limitAng(flang - 180)

def rotateRobot(rot):
    global flvec, frvec, blvec, brvec, robotCenter, flang, frang, blang, brang, speed_scalar, move
    rotate = rot * speed_scalar
    flDelta = pygame.math.Vector2()
    flDelta.from_polar((rotate,flang-90))
    frDelta = pygame.math.Vector2()
    frDelta.from_polar((rotate,frang-90))
    blDelta = pygame.math.Vector2()
    blDelta.from_polar((rotate,blang-90))
    brDelta = pygame.math.Vector2()
    brDelta.from_polar((rotate,brang-90))

    if move:
        flvec += flDelta
        frvec += frDelta
        blvec += blDelta
        brvec += brDelta

        flang = limitAng(pygame.math.Vector2().angle_to(robotCenter-flvec))
        frang = limitAng(flang + 90)
        blang = limitAng(flang - 90)
        brang = limitAng(flang - 180)
        fudgeRobot()

def translateRobot(x,y):
    global flvec, frvec, blvec, brvec, robotCenter, speed_scalar, move
    if move:
        deltaX = x * speed_scalar
        deltaY = y * speed_scalar
        flvec += pygame.math.Vector2(deltaX,deltaY)
        frvec += pygame.math.Vector2(deltaX,deltaY)
        blvec += pygame.math.Vector2(deltaX,deltaY)
        brvec += pygame.math.Vector2(deltaX,deltaY)
        robotCenter += pygame.math.Vector2(deltaX,deltaY)

def fudgeRobot():
    global flvec, frvec, blvec, brvec, robotCenter, flang, frang, blang, brang, robotLength, robotWidth
    mag = math.sqrt((robotLength/2)*(robotLength/2)+(robotWidth/2)*(robotWidth/2))
    flDelta = pygame.math.Vector2()
    flDelta.from_polar((mag,flang))
    frDelta = pygame.math.Vector2()
    frDelta.from_polar((mag,frang))
    blDelta = pygame.math.Vector2()
    blDelta.from_polar((mag,blang))
    brDelta = pygame.math.Vector2()
    brDelta.from_polar((mag,brang))

    flvec = robotCenter - flDelta
    frvec = robotCenter - frDelta
    blvec = robotCenter - blDelta
    brvec = robotCenter - brDelta
    
    
 
# -------- Main Program Loop -----------
while not done:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
        # JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    if move:
        picture = pygame.image.load('C:/Users/ilive/Desktop/pyxinput/2019field.png')
        screen.blit(picture, (0,0))
 
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
 
    '''axes = joystick.get_numaxes()
    textPrint.print(screen, "Number of axes: {}".format(axes))
    textPrint.indent()
 
    for i in range(axes):
        axis = joystick.get_axis(i)
        textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis))
    textPrint.unindent()
    
    textPrint.print(screen,"flang: "+str(flang))
    textPrint.print(screen,"frang: "+str(frang))
    textPrint.print(screen,"blang: "+str(blang))
    textPrint.print(screen,"brang: "+str(brang))'''
    
    x = joystick.get_axis(0)
    y = joystick.get_axis(1)
    rotate = joystick.get_axis(4)
    deadband = 0.1

    #don't allow tanslation vector with magnitude > 1.0
    magnitude = math.sqrt(x * x + y * y)
    if magnitude > 1.0:
        x /= magnitude
        y /= magnitude
    magnitude = math.sqrt(x * x + y * y)    

    #textPrint.print(screen,"actualRobotWidth: "+str((flvec-frvec).magnitude()))
    #textPrint.print(screen,"mag: "+str(magnitude))

    if robotCentric:
        #rotate x and y into robot frame
        '''flRobotAng = limitAng(flang - 45)
        frRobotAng = limitAng(frang - 135)
        blRobotAng = limitAng(blang + 45)
        brRobotAng = limitAng(brang + 135)
        textPrint.print(screen, "flRobotAng: "+str(flRobotAng))
        textPrint.print(screen, "frRobotAng: "+str(frRobotAng))
        textPrint.print(screen, "blRobotAng: "+str(blRobotAng))
        textPrint.print(screen, "brRobotAng: "+str(brRobotAng))'''
        robotAng = limitAng(flang - 45)
        robotAng *= (math.pi / 180) #convert to radians
        newx = x * math.cos(robotAng) - y * math.sin(robotAng)
        newy = x * math.sin(robotAng) + y * math.cos(robotAng)
        x = newx
        y = newy
    

    
    if abs(rotate) > deadband:
        #out of deadband

        #find perpendicular angle to each module
        fl_ang = flang - 90
        fr_ang = frang - 90
        bl_ang = blang - 90
        br_ang = brang - 90

        #convert to radians
        fl_ang *= math.pi / 180
        fr_ang *= math.pi / 180
        bl_ang *= math.pi / 180
        br_ang *= math.pi / 180

        flx = rotate*math.cos(fl_ang)
        fly = rotate*math.sin(fl_ang)
        frx = rotate*math.cos(fr_ang)
        fry = rotate*math.sin(fr_ang)
        blx = rotate*math.cos(bl_ang)
        bly = rotate*math.sin(bl_ang)
        brx = rotate*math.cos(br_ang)
        bry = rotate*math.sin(br_ang)

    

    if magnitude > deadband:
        if abs(rotate) > deadband:
            #out of both deadbands
            mag1 = math.sqrt((flx+x)**2 + (fly+y)**2)
            mag2 = math.sqrt((frx+x)**2 + (fry+y)**2)
            mag3 = math.sqrt((blx+x)**2 + (bly+y)**2)
            mag4 = math.sqrt((brx+x)**2 + (bry+y)**2)

            mag = max(mag1,mag2,mag3,mag4)
            if mag == 0:
                mag = 1
            if mag < 1:
                mag = 1

            #rotate + translate
            FL = pygame.math.Vector2((flx+x)/mag,(fly+y)/mag)
            FR = pygame.math.Vector2((frx+x)/mag,(fry+y)/mag)
            BL = pygame.math.Vector2((blx+x)/mag,(bly+y)/mag)
            BR = pygame.math.Vector2((brx+x)/mag,(bry+y)/mag)
            translateRobot(x/mag,y/mag)
            rotateRobot(rotate/mag)
            textPrint.print(screen,"percent slow: "+str(1/mag))
            
            #resultant vectors
            drawVector(flvec,(flx+x)/mag,(fly+y)/mag,BLUE)
            drawVector(frvec,(frx+x)/mag,(fry+y)/mag,BLUE)
            drawVector(blvec,(blx+x)/mag,(bly+y)/mag,BLUE)
            drawVector(brvec,(brx+x)/mag,(bry+y)/mag,BLUE)
        else:
            #only translate
            translateRobot(x,y)
    else:
        if abs(rotate) > deadband:
            #only rotate
            rotateRobot(rotate)
            #fudgeRobot()

    if magnitude > deadband:
        #draw translation vectors
        if showVecAddition:
            #want to show vector addition
            drawVector(flvec,x,y,RED)
            drawVector(frvec,x,y,RED)
            drawVector(blvec,x,y,RED)
            drawVector(brvec,x,y,RED)
        elif abs(rotate) < deadband:
            #not rotating and don't want to show vector addition
            drawVector(flvec,x,y,BLUE)
            drawVector(frvec,x,y,BLUE)
            drawVector(blvec,x,y,BLUE)
            drawVector(brvec,x,y,BLUE)

    if abs(rotate) > deadband:
        #draw rotation vectors
        if showVecAddition:
            #want to show vector addition
            drawVector(flvec,flx,fly,GREEN)
            drawVector(frvec,frx,fry,GREEN)
            drawVector(blvec,blx,bly,GREEN)
            drawVector(brvec,brx,bry,GREEN)
        elif magnitude < deadband:
            #not translating and don't want to show vector addition
            drawVector(flvec,flx,fly,BLUE)
            drawVector(frvec,frx,fry,BLUE)
            drawVector(blvec,blx,bly,BLUE)
            drawVector(brvec,brx,bry,BLUE)

    drawBox(flvec,frvec,blvec,brvec)

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.update()
 
    # Limit to 60 frames per second
    clock.tick(40)
 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()