import random

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
#import random

#Kamera zugriff hinzufügen

"""cv2.VideoCapture(1) für die externe webkamera
cv2.VideoCapture(0) für den integrirte kamera
cv2V.ideoCapture(0) for the web cam in the Laptop 
and cv2.VideoCapture(1) for the extern webcam"""


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

"""cap2 = cv2.VideoCapture(0)#cv2.VideoCapture(1) für die externe webkamera-----------cv2.VideoCapture(0) für den integrirte kamera
cap2.set(3, 640)
cap2.set(4, 480)"""




detector = HandDetector(maxHands=1) # maximale hände die getrackt werden können am bildschirm


timer = 0
stateResult = False
startGame = False
scores =  [0,0]
#closeGame = False

#hintergrund adden
while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()
    

    # hintergrund scalieren
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = cv2.flip(imgScaled[:, 80:480],1)

    # Handfinden
    hands, img = detector.findHands(imgScaled)
    

    if startGame and stateResult is False:

        timer = time.time() - initialTime
        cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

        if timer > 3:
            stateResult = True
            timer = 0

            if hands:
                '''if hands[0]['type'] == 'Right':
                    hand = hands[0]
                elif len(hands) > 1 and hands[1]['type'] == 'Right':
                    hand = hands[1]
                else:
                    stateResult = False
                    continue
                    hand = hands[0]'''
                hand = hands[0]
                fingers = detector.fingersUp(hand)
                if fingers == [0, 0, 0, 0, 0]:
                    playerMove = 1
                elif fingers == [1, 1, 1, 1, 1]:
                    playerMove = 2
                elif fingers == [0, 1, 1, 0, 0]:
                    playerMove = 3
                else:
                    playerMove = 0
                
                  

                randomNumber = random.randint(1, 3)
                imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))



                # player gewinnt

                if (playerMove == 1 and randomNumber == 3) or \
                        (playerMove == 2 and randomNumber == 1) or \
                        (playerMove == 3 and randomNumber == 2):
                    scores[1] += 1

                # AI gewinnt
                if (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                        (playerMove == 2 and randomNumber == 3):
                    scores[0] += 1

    # randomNumber = random.randint(1, 3)
    # imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)

    # Kamera auf dem hintergrund befestigen
    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

         # zeige spieler handzeichen
        if playerMove == 1:
            cv2.putText(imgBG, "Stein", (860, 310), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 6)
        elif playerMove == 2:
            cv2.putText(imgBG, "Papier", (860, 310), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 6)
        elif playerMove == 3:
            cv2.putText(imgBG, "Schere", (860, 310), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 6)

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    # cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    

    
    

    key = cv2.waitKey(50)
    if key & 0xFF == 32: # start Programm with space
        startGame = True

        initialTime = time.time()
        stateResult = False
#um das programm zu schließen
    elif key & 0xFF == 27:
        break







