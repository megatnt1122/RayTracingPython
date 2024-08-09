#FIXED SPECULAR MOSTLY HAD TO NORMALIZE A BUNCH AKA VIEW PORT AND OTHERS

#ISSUE OF NOW MATH MAY BEW WRONG GETS STUCK ON SAME COLOR VALUE CFF2100

#Name:Austin Hampton
#CWID:10386361
#Date:12/21/2022
#Assignment:Assignment4 - Raytracing
#Description: This program generates 3 3d shapes: 2 cubes and 1 Cylinder
#                it then allows one to manipulate each shape using buttons
#
#PAINT THE BLUE SKY FIRST
import math
import copy
from tkinter import *
canvasWidth = 800 #400
canvasHeight = 600 #400
d = 400
Ip = .7
Ia = .3
lightSource = [500, 500, -500] #500 500 0
centerOfProjection = [0,0,-d] #Center of projection

#for rgb we use 3 combined colors RGB INSTEAD OF SPECULAR for each
#Driver for the traceray method


#this is the sphere class object it contains everything required for a sphere to work as well as all the reflectinos and tracing equations
class sphere:
    def __init__(self, centerpoint, radius, localColor, Kd, Ks, specIndex, localWeight, reflectWeight):
        self.centerpoint = centerpoint
        self.radius = radius
        self.localColor = localColor
        self.Kd = Kd
        self.Ks = Ks
        self.specIndex = specIndex
        self.localWeight = localWeight
        self.reflectedWeight = reflectWeight
        self.t = 999999
        self.intersectionPoint = []
        self.phongIntensity = 0
        self.reflect = [0,0,0]
    
    #returns reflected weight
    def reflectedWeight(self):
        return self.reflectWeight
    #Intersect function for sphere
    #return the intersection but also set t to something
    #IJK IS OUR RAY I THINK
    def intersect(self, startPoint,ray):
        intersectionPoint = []
        #PAGE 128 FOR INFO
        r = self.radius
        
        #first we need t
        #Center point is L M N
        l = self.centerpoint[0]
        m = self.centerpoint[1]
        n = self.centerpoint[2]
        
        #X1 Y1 Z1 IS STARTING POINT AKA CAMERA
        X1 = startPoint[0]
        Y1 = startPoint[1]
        Z1 = startPoint[2]
        
        #ray is our I J K
        i = ray[0]
        j = ray[1]
        k = ray[2]
        
        #setting a
        #a = I^2 + J^2 + K^2
        a = math.pow(i,2) + math.pow(j,2) + math.pow(k,2)
        
        #b = 𝟐 ∙ 𝒊 ∙ (𝑿𝟏 − 𝒍) + 𝟐 ∙ 𝒋 ∙ (𝒀𝟏 − 𝒎) + 𝟐 ∙ 𝒌 ∙ (𝒁𝟏 − 𝒏)
        b = 2 * i * (X1 - l) + 2 * j * (Y1 - m) + 2 * k * (Z1 - n)
        
        #c = 𝒍^2 + 𝒎^2 + 𝒏^2 + 𝑿𝟏^2 + 𝒀𝟏^2 + 𝒁𝟏^2 + 𝟐 ∙ (−𝒍 ∙ 𝑿𝟏 − 𝒎 ∙ 𝒀𝟏 − 𝒏 ∙ 𝒁𝟏) − 𝒓^2
        c = math.pow(l,2) + math.pow(m,2) + math.pow(n,2) + math.pow(X1,2) + math.pow(Y1,2) + math.pow(Z1,2) + 2 * (-l * X1 - m * Y1 - n * Z1) - math.pow(r,2)
        
        #discriminant = b^2 - 4 * a * c
        discriminant = math.pow(b,2) - 4 * a * c
        
        #if less than 0 then return 99999 and return intersectionPoint
        if(discriminant < 0):
            self.t = 99999
            return intersectionPoint
        
        #T numerator aka T Top  
        tTop = -b - (math.sqrt(math.pow(b, 2) - 4 * a * c))
        #T Denominator aka T Bottom
        tBottom = (2 * a)
        
        #If bottom is 0 then we must return intersection and say 99999 ELSE do normal equation
        if(tBottom==0):
            self.t = 99999
            return intersectionPoint
        else:
            t = tTop/tBottom
            
            X = X1 + i * t
            Y = Y1 + j * t
            Z = Z1 + k * t
        
            #Horizon
            if(Z<0 or Z>1500 or t < 0.001):
                self.t = 99999
                return intersectionPoint
            self.t = t
            #after we set our t we then get intersect points
            #setting intersect points
            X = X1 + i * t
            Y = Y1 + j * t
            Z = Z1 + k * t
            intersectionPoint.append(X)
            intersectionPoint.append(Y)
            intersectionPoint.append(Z)
            self.intersectionPoint = copy.deepcopy(intersectionPoint)
            self.setReflect(ray) #HAVE TO CALL THIS BEFORE PHONG
            self.setPhongIntensity()
            return intersectionPoint
    #used to set intersection point MAY BE UNNECESSARY IM TOO TIRED TO CHECK :D
    def setIntersectionPoint(self, intersectionPoint):
        self.intersectionPoint = intersectionPoint
    #Phong Intensity
    def setPhongIntensity(self):
        global centerOfProjection
        global Ia
        global Ip
        #########################################################################
        #SETTING Ia AND Ip DUNNO IF THEY ARE SUPPOSED TO BE SET SOMEWHEERES ELSE#
        #########################################################################
        Kd = self.Kd
        Ks = self.Ks
        L = computeUnitVector(self.intersectionPoint, lightSource)
        ambient = Ia * Kd
        SpecIndex = self.specIndex
        
        
        #MAY HAVE TO NORMALIZE THIS
        V = normalize(centerOfProjection)      
        
        
        
        nonNormal = []
        nonNormal.append(self.intersectionPoint[0]-self.centerpoint[0])
        nonNormal.append(self.intersectionPoint[1]-self.centerpoint[1])
        nonNormal.append(self.intersectionPoint[2]-self.centerpoint[2])
        N = normalize(nonNormal)    
        
        #N dot product L
        NdotL = N[0]*L[0] + N[1]*L[1] + N[2] * L[2]
        if NdotL < 0:NdotL = 0
        
        #calculating diffuse
        diffuse = Ip * Kd * NdotL
        
        #calculating reflections
        R = self.reflect # return vecor is normalized in reflect
        
        #R dot product V
        RdotV = R[0]*V[0] + R[1]*V[1] + R[2] * V[2]
        
        #if R dot product V  is less than 0 default to 0
        if RdotV < 0: RdotV = 0
        specular = Ip * Ks * RdotV**SpecIndex
        
        intensity = ambient + diffuse + specular
        self.phongIntensity = intensity
    
    #reflect
    def setReflect(self, ray):
        #SEE PAGE 133 FOR INFO
        global lightSource
        R = []
        
        nonNormal = []
        nonNormal.append(self.intersectionPoint[0]-self.centerpoint[0])
        nonNormal.append(self.intersectionPoint[1]-self.centerpoint[1])
        nonNormal.append(self.intersectionPoint[2]-self.centerpoint[2])
        N = normalize(nonNormal)       
        L = normalize(ray)
        twoCosPhi = 2 * (-N[0]*L[0]-N[1]*L[1]-N[2]*L[2])
        if twoCosPhi > 0:
            for i in range(3):
                R.append(N[i] + (L[i]/twoCosPhi))
        elif twoCosPhi == 0:
            for i in range(3):
                R.append(L[i])
        else:
            for i in range(3):
                R.append(-N[i]-(L[i]/twoCosPhi))     
        self.reflect = normalize(R)
    
    def localWeight(self):
        return self.localWeight
    
    def reflectedWeight(self):
        return self.reflectWeight
#CAP LETTERS ARE THE SURFACE NORMALS
#LOWERCASE LETTERS ARE anchor points
#X1 Y1 Z1 IS THE CENTER OF PROJECTION AKA CAMERA
#X2 Y2 Z2 = SCREEN REPRESENTATION 

#Checkerboard class used to define the checkerboard plane :D
class checkerboard:
    def __init__(self, normal, anchor, kd, ks, specIndex, localWeight, reflectWeight):
        self.normal = normal
        self.anchor = anchor
        self.kd = kd
        self.ks = ks
        self.specIndex = specIndex
        self.localWeight = localWeight
        self.reflectedWeight = reflectWeight
        self.intersectionPoint = []
        self.t = 999999
        #change these to actual stuff this is just a test
        self.phongIntensity = 0
        self.localColor = [0,0,0]
        #reflect TEST
        self.reflect = [1,1,1]  
    
    def intersectionPoint(self):
        return self.intersectionPoint
    
    def setIntersectionPoint(self, intersectionPoint):
        self.intersectionPoint = intersectionPoint

    #local Color its the [1, 0.5, 0.5] not the hexcode
        #Make it red
    def setLocalColor(self, intersectionPoint):
        if(intersectionPoint[0] >= 0):
            ColorFlag = 1
        else:
            ColorFlag = 0
        if(math.fmod(math.fabs(intersectionPoint[0]),200)>100):
            ColorFlag = not ColorFlag
        if(math.fmod(math.fabs(intersectionPoint[2]),200)>100):
            ColorFlag = not ColorFlag
        #COLOR RED
        if ColorFlag:
            color = [1,0,0]
        #COLOR WHITE
        else:
            color = [1,1,1]
        self.localColor = color
        
        
    #PAGE 133 FOR INFO
    def setT(self, t):
        self.t = t
    
    def getT(self):
        return self.t
    
    #return the intersection but also set t to something
    #IJK IS OUR RAY I THINK
    def intersect(self, startPoint,ray):
        intersectionPoint = []
        #PAGE 133 FOR INFO
        #first we need t
        #d = Aa + Bb + Cc
        A = self.normal[0]
        B = self.normal[1]
        C = self.normal[2]
        X1 = startPoint[0]
        Y1 = startPoint[1]
        Z1 = startPoint[2]
        a = self.anchor[0]
        b = self.anchor[1]
        c = self.anchor[2]
        #d = Aa + Bb + Cc
        D = A*a + B*b + C*c
        i = ray[0]
        j = ray[1]
        k = ray[2]
        
        tTop = -(A*X1 + B*Y1 + C*Z1 - D)
        tBottom = (A*i + B*j + C*k)
        
        #KEEP EYE ON THIS FUNCT MAY NEED TO BE == 0 DUNNO YET
        if(tBottom==0):
            self.t = 99999
            return intersectionPoint
        else:
            t = tTop/tBottom
            
            X = X1 + i * t
            Y = Y1 + j * t
            Z = Z1 + k * t
        
        #Horizon
            if(Z<0 or Z>1500 or t < 0.001):
                self.t = 99999
                return intersectionPoint
            self.t = t
            intersectionPoint.append(X)
            intersectionPoint.append(Y)
            intersectionPoint.append(Z)
            self.intersectionPoint = copy.deepcopy(intersectionPoint)
            self.setLocalColor(intersectionPoint)
            self.setReflect(ray) #HAVE TO CALL THIS BEFORE PHONG
            self.setPhongIntensity()   
            return intersectionPoint
    
    
    def normal(self):
        return self.normal
        
    def anchor(self):
        return self.anchor
    
    def kd(self):
        return self.kd
    
    def ks(self):
        return self.ks
    
    def specIndex(self):
        return self.specIndex
    
    def localWeight(self):
        return self.localWeight
    
    def reflectedWeight(self):
        return self.reflectWeight
 
    #Phong Intensity
    def setPhongIntensity(self):
        global centerOfProjection
        
        #########################################################################
        #SETTING Ia AND Ip DUNNO IF THEY ARE SUPPOSED TO BE SET SOMEWHEERES ELSE#
        #########################################################################
        global Ia
        global Ip
        Kd = self.kd
        Ks = self.ks
        L = computeUnitVector(self.intersectionPoint, lightSource)
        ambient = Ia * Kd
        SpecIndex = self.specIndex
        
        
        #MAY HAVE TO NORMALIZE THIS
        V = normalize(centerOfProjection)
        
        #surface normal
        N = normalize(self.normal)
        
        #N dot product L
        NdotL = N[0]*L[0] + N[1]*L[1] + N[2] * L[2]
        if NdotL < 0:NdotL = 0
        
        #calculating diffuse
        diffuse = Ip * Kd * NdotL
        
        #calculating reflections
        R = self.reflect # return vecor is normalized in reflect
        

        #R dot product V
        RdotV = R[0]*V[0] + R[1]*V[1] + R[2] * V[2]
        
        #if R dot product V  is less than 0 default to 0
        if RdotV < 0: RdotV = 0
        specular = Ip * Ks * RdotV**SpecIndex
        #print(specular)
        intensity = ambient + diffuse + specular
        self.phongIntensity = intensity
    
    #reflect
    def setReflect(self, ray):
        global lightSource
        R = []
        N = normalize(self.normal)
        L = normalize(ray)
        twoCosPhi = 2 * (-N[0]*L[0] - N[1]*L[1] - N[2]*L[2])
        if(twoCosPhi > 0):
            for i in range(3):
                 R.append(N[i] + ( L[i] / twoCosPhi ))
        elif(twoCosPhi == 0):
            for i in range(3):
                R.append(L[i])
        else:
            for i in range(3):
                R.append(-N[i] - ( L[i] / twoCosPhi ))
        self.reflect = normalize(R)
        
#defining the chekcerboard given: surface normal, anchor point, kd, ks, specIndex, weight local, weight for reflections0.5
board = checkerboard([0,1,0],[0,-300,0], 0.6,0.4, 8, 0.5, .5)
redSphere = sphere([300, -100, 300], 200, [1, 0.5, 0.5], 0.5, 0.5, 8, 0.5, 0.5)
greenSphere = sphere([-100, -200, 300], 100, [0.5, 1, 0.5], 0.5, 0.5, 8, 0.5, 0.5)
blueSphere = sphere([0,0,800], 300, [0.5, 0.5, 1], 0.5, 0.5, 8, 0.5, 0.5)

scene = [redSphere,greenSphere,blueSphere,board]



#method iterates over each pixel of the images, onerow of pixels at a time DRAWS EVERYTHING
def renderImage():
    global lightSource #MAY HAVe to normalize this maybe?
    global illuminationSaturationCounter
    global centerOfProjection
    global canvasHeight
    global canvasWidth
    illuminationSaturationCounter = 0
    
    top = round(canvasHeight/2)
    bottom = round(-canvasHeight/2)
    left = round(-canvasWidth/2)
    right = round(canvasWidth/2)
    
    for y in range(top, bottom, -1):
        for x in range(left, right):
            #RAY FROM THE CENTER OF PROJECTION TO THIS SPECIFIC PXIEL (this is sorta being our prospective projection)
            #RAY IS ALREADY BECOMING THE I J AND K USED FOR TRACING
            ray = computeUnitVector(centerOfProjection, [x,y,0])
            
            #color is the rgb values [R, G, B]
            color = traceRay(centerOfProjection, ray, 4)
            w.create_line(right+x, top-y, right+x+1, top-y, fill=RGBColorHexCode(color))
    overSat = illuminationSaturationCounter / (canvasWidth*canvasHeight) * 100
    print(illuminationSaturationCounter, " pixel color values were oversaturated: ", overSat, "%.")

#computes normal unit vector
def computeUnitVector(start, end):
    return normalize([end[0]-start[0], end[1]-start[1], end[2]-start[2]])

#spitting out the red green and blue color code
def RGBColorHexCode(color):
    #yes this is lazy but i had a lotta values being 1.00000000001 and got annoyed :D
    if(color[2] > 1): color[2]=1
    if(color[0] > 1): color[0]=1
    if(color[1] > 1): color[1]=1
    returnColor = triColorHexCode(color)
    return returnColor
    



##### CORE RAY TRACER FOR REFLECTED RAYS ONLY #####
#Traces a single ray, returning the color of the pixel as an [R, G, B] list, using a 0-1 scale
#FUNCTION IS TRACING A SINGLE RAY WITH CHANGING DEPTH I THINK
#our ray is the point on the screen AKA THE PIXEL AKA THE X2 Y2 Z2
def traceRay(startPoint, ray, depth):
    skyColor = [0.53, 0.81, 0.92]
    #return "black" when you reach the bottom of the recursive calls
    if depth == 0:
        return [0,0,0]
    #intersect the ray with all objects to determine nearestObject (if any)
    
    #T IS THE "BUFFER" IF THERE IS AN INTERSECTOIN THEN TMIN IS SET TO THAT POINT
    tMin = 999999 #initialize to t to a very large number
    for object in scene:        
        #objects intersect attribute is an empty array by default
        if(object.intersect(startPoint, ray) != []):
            if(object.t < tMin):
                #THIS IS SAYING IF INTERSECTION IS MET THEN SET TMIN TO THAT
                tMin = object.t
                #SET NEAREST OBJECT AT THIS T TO OBJECT
                nearestObject = object
    #intersect is empty aftert a second time for some reason
    #return skycolor if no intersection
    if tMin ==  999999:
        return skyColor
    
    #determine localColor and the weight for that color at the intersection point
    color = nearestObject.localColor
    intensity = nearestObject.phongIntensity
    #asks if object is in shadow if so lower the intensity
    if(inShadow(nearestObject, nearestObject.intersectionPoint)):
         intensity *= 0.25
    localColor = [color[0]*intensity*2, color[1]*intensity*2, color[2]*intensity*2]
    localWeight = nearestObject.localWeight
    
    #compute color returned from reflected ray
    reflectWeight = nearestObject.reflectedWeight
    reflectColor = traceRay(nearestObject.intersectionPoint, nearestObject.reflect, depth-1)
    
    #combine the local and reflected colors together using their respective weights
    #              R G B
    returnColor = [0,0,0]
    for i in range(3):
        returnColor[i] = localColor[i]*localWeight + reflectColor[i]*reflectWeight
    return returnColor

def inShadow(startObject, startPoint):
    ray = computeUnitVector(startPoint, lightSource)
    for object in scene:
        if startObject != object and object.intersect(startPoint, ray) != []: return 1
    return 0
#normalizes the vector
def normalize(vector):
    sumOfSquares = 0
    for i in range(len(vector)):
        sumOfSquares += vector[i]**2
    magnitude = math.sqrt(sumOfSquares)
    vect = []
    for i in range(len(vector)):
        vect.append(vector[i]/magnitude)
    return vect

#ambient =
#diffuse = 
#specular =
#THIS TAKES IN THE COLOR ARRAY [R, G, B] THEN 
def triColorHexCode(color):
    RColorCode = colorHexCode(color[0])
    GColorCode = colorHexCode(color[1])
    BColorCode = colorHexCode(color[2])
    
    #combined color codeR + combined color codeG + combined color codeB 
    colorString = "#" + RColorCode + GColorCode + BColorCode
    return colorString
#used to make the hexcode for the color
def colorHexCode(intensity):
    hexString = str(hex(round(255*intensity)))
    if(hexString[0] == "-"):
        print("illumination intensity setting to 0 due to negative intensity")
        trimmedHexString = "00"
    else:
        trimmedHexString = hexString[2:] #get rid of 0x at beginning of hex string
        #convert single digit hex strings to 2 digit hex strings
        if(len(trimmedHexString)==1):
            trimmedHexString = "0" + trimmedHexString
    return trimmedHexString

root = Tk()
outerframe = Frame(root)
outerframe.pack()
w = Canvas(outerframe, width=canvasWidth, height=canvasHeight)
renderImage()
#Put drawing objects here
w.pack()



#QUESTIONS TO ASK AND WHY
#when doing the local do the phong illumination model AKA ambient spec, diffuse
#the red or white on the checkerboard it should be a local components
#Ed Catmull 1972 HAND STUFF
#
#uc berklet blinn YOUTUBE LECTURE
#
#A
#What is RBG COLOR TAKING IN? specifically we want a list of 3 values one being r g b would we use our previous hexcode functions to convert it?
#
#Ask to explain the phong illumination model in further detail
#
#Ask to ensure that we are using projected projections to create everything
#Ask how does the checkerboard work with projected projections aka if we dont give it the location perameters
#Ask him to explain the code in more detail so you understand it
#Ask him to explain how the rays would work and shadows work
#Why does L = computing the unit vector
#In the notes you show us using a point light but in the assignment you want us using a lighting vector
#
#are we only using projected projection with plane?
#these may be dumb questions
#tmin wat is it simply
#should the plane act like a large polygon that we have specificed to change colors accordingly
#
#
#
#X1,Y1,Z1 = CENTER POINT OF PROJECTOIN VIEW POINT
#X2, Y2, Z2 = SCREEN LOCAITON
#z2 = 0