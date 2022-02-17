from pywinauto.application import Application
import pyautogui
import time

# cv2.cvtColor takes a numpy ndarray as an argument
import numpy as nm
import pytesseract

# importing OpenCV
import cv2
from PIL import ImageGrab

"""this function grabs 3D Mark Results and valid state from the results page via OCR

needs to send the scores to order database
"""
def ScoretoString():
    # Path of tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    #while(True):

    # ImageGrab-To capture the screen image in a loop.
    # Bbox used to capture a specific area.
    #The bounding box is a (left_x, top_y, right_x, bottom_y) tuple
    overallcap = ImageGrab.grab(bbox =(334, 357, 550, 437))
    graphicsscorecap = ImageGrab.grab(bbox =(700, 230, 860, 290))
    cpuscorecap = ImageGrab.grab(bbox =(700, 320, 860, 385))
    #validcap = ImageGrab.grab(bbox =(435, 240, 575, 295))
    #bad cpu score should trigger maintainence notification as this is within our control

    # Converted the image to monochrome for it to be easily
    # read by the OCR and obtained the output String.
    overall = pytesseract.image_to_string(
            cv2.cvtColor(nm.array(overallcap), cv2.COLOR_BGR2GRAY),
            lang ='eng')
    graphicsscore = pytesseract.image_to_string(
            cv2.cvtColor(nm.array(graphicsscorecap), cv2.COLOR_BGR2GRAY),
            lang ='eng')
    cpuscore = pytesseract.image_to_string(
            cv2.cvtColor(nm.array(cpuscorecap), cv2.COLOR_BGR2GRAY),
            lang ='eng')
    #validscore = pytesseract.image_to_string(
            #cv2.cvtColor(nm.array(validcap), cv2.COLOR_BGR2GRAY),
            #lang ='eng')

    #processing the strings for output to csv
    numlist = ["0","1","2","3","4","5","6","7","8","9"]
    markscores = []

    rawlist1 = []
    for i in overall:
        rawlist1.append(i)
    resultlist1 = []
    for element in rawlist1:
        if element in numlist:
            resultlist1.append(element)
    overallstring = ''
    overallstring = overallstring.join(resultlist1)
    markscores.append("overall = " + overallstring + ',')

    rawlist2 = []
    for i in graphicsscore:
        rawlist2.append(i)
    resultlist2 = []
    for element in rawlist2:
        if element in numlist:
            resultlist2.append(element)
    graphicsstring = ''
    graphicsstring = graphicsstring.join(resultlist2)
    markscores.append("graphics = " + graphicsstring + ',')

    rawlist3 = []
    for i in cpuscore:
        rawlist3.append(i)
    resultlist3 = []
    for element in rawlist3:
        if element in numlist:
            resultlist3.append(element)
    cpustring = ''
    cpustring = cpustring.join(resultlist3)
    markscores.append("cpu = " + cpustring + ',')


    #(left_x, top_y, right_x, bottom_y)
    #color matching green or red (valid or invalid)
    validationstring = ''
    validationcap = pyautogui.screenshot(region=(433,215,463,245))
    #getting pixel color at location
    #accounting for slight variation in color with uncertainties ufloat = +/-
    #print(validationcap.getpixel((660, 474)))
    colors = validationcap.getpixel((445, 226))
    if 235 <= colors[0] <= 260 and 235 <= colors[1] <= 260 and 235 <= colors[2] <= 260:
        validationstring = "valid"
    elif 102 <= colors[0] <= 132 and 22 <= colors[1] <= 52 and 17 <= colors[2] <= 47:
        validationstring = "invalid"

    #else:
        #prompt authenticator and ask if valid or invalid
        #then store response in same variable to add to list

    markscores.append("valid = " + validationstring)


    fh = open("3DMarkPlaceholder.txt","w")
    for score in markscores:
        fh.write(score)
    fh.close()

    return
#need to enforce 1080p display settings before everything else

"""start with driver uninstallation and then reinstallation
preserve state between reboots by modifying a text file or something and
then reading it here to determine state via logic statement"""

#auto is 800,538
#fan button is 594,538 -- drag to 793,538
#apply button is 770,570
#minimize is 980,260
#pyautogui.click(x=moveToX, y=moveToY, clicks=num_of_clicks, interval=secs_between_clicks, button='left')

#Start MSI Afterburner (anaconda prompt needs to be in admin mode)
#Set gpu fan speed to 100%
#Minimize application

#MSIdir = r'C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe'
#this is a bit weird -- may need to start app twice
#app = Application().start(MSIdir)
#app = Application().start(MSIdir)
#time.sleep(1)
#pyautogui.click(x=800, y=538)
#pyautogui.moveTo(594, 538, duration = 0.05)
#pyautogui.dragTo(800, 538, duration = 0.5, button = 'left')
#pyautogui.click(x=770, y=570)
#pyautogui.click(x=980, y=260)

#lookup is 1100,320
#sensors is 880,295
#Log to file is 787,738
#File name is 1000,883
#save to file is 1660,950
#need to enter file name which then connects to cloud application

#Open GPU-Z for a second time
#click sensors and then log to file
#delete whatevers there and type in file name given by order number from database
#save to database
#don't touch and open Steam (should move GPU-Z to the background)

#Zdir = r'C:\Users\Benjamin\Desktop\Automate\GPU-Z\GPU-Z.exe'
#zapp = Application().start(Zdir)
#time.sleep(5)
#pyautogui.click(x = 880, y = 295)
#pyautogui.click(x = 787, y = 738)
#time.sleep(0.25)
#pyautogui.click(x = 1000, y = 883)
#for i in range(50):
#  pyautogui.keyDown('backspace')
#pyautogui.write('placeholderlog') #needs cloud file name integration
#pyautogui.click(x = 1660, y = 950)


#Markdir = r'C:\Program Files\UL\3DMark\3DMark.exe'
#markapp = Application().start(Markdir)
#time.sleep(25)
#waiting for 3DMark to load completely idk how to detect this (maybe loop until detects image)
#set preferences to not include demo
#pyautogui.click(x = 1265, y = 165)
#time.sleep(0.5)
#pyautogui.click(x = 950, y = 880)
#time.sleep(0.5)
#pyautogui.click(x = 1470, y = 440)
#time.sleep(250)

#ScoretoString()


#chrome needs to be primed to open in full screen (ie. be in full screen before last close)\

#closing 3DMark
#time.sleep(0.5)
#pyautogui.click(x = 1630, y = 115)


DDUdir = r'C:\Users\Benjamin\Desktop\Automate\DDU v18.0.3.8\Display Driver Uninstaller.exe'
DDUapp = Application(backend = "uia").start(DDUdir)
time.sleep(4)
print(DDUapp.windows())

#need to make sure that DDU has already started first and preferences have been set (in advanced options, select block windows from automatically installing drivers)


#Position Inspector
"""while True:
    print(pyautogui.position())
    time.sleep(0.25)"""
