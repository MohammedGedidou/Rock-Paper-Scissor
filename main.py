import random
import pygame 
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import os



#import random

#Kamera zugriff hinzufügen

"""cv2.VideoCapture(1) für die externe webkamera
cv2.VideoCapture(1) für den integrirte kamera
cv2V.ideoCapture(0) for the web cam in the Laptop 
and cv2.VideoCapture(1) for the extern webcam"""


Capture = cv2.VideoCapture(0)
Capture.set(3, 640)
Capture.set(4, 480)

"""Capture2 = cv2.VideoCapture(0)#cv2.VideoCapture(1) für die externe webkamera-----------cv2.VideoCapture(0) für den integrirte kamera
Capture2.set(3, 640)
Capture2.set(4, 480)"""
pygame.init()
pygame.mixer.music.load("Resources/gamemusik.mp3")
pygame.mixer.music.set_volume(0.5)      



detector = HandDetector(maxHands=1) # maximale hände die getrackt werden können am bildschirm


timer = 0
stateResult = False
startGame = False
scores =  [0,0]
pygame.mixer.music.play(-1)


ROCK = 1
PAPER = 2
SCISSORS = 3

#hintergrund adden
while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = Capture.read()
    

    # hintergrund scalieren
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Handfinden
    hands, img = detector.findHands(imgScaled)

    

    if startGame and not stateResult:
       
    

        timer = time.time() - initialTime
        cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

        if timer > 3:
            stateResult = True
            timer = 0

            
            if len(hands) == 0:
                Playermove = 0
            else:
                hand = hands[0]
                fingers = detector.fingersUp(hand)
                if fingers == [0, 0, 0, 0, 0]:
                    Playermove = 1
                elif fingers == [1, 1, 1, 1, 1]:
                    Playermove = 2
                elif fingers == [0, 1, 1, 0, 0]:
                    Playermove = 3
                else:
                    Playermove = 0

                
                  

                
                

            Computermove = random.randint(1, 3)
            img_path = os.path.join('Resources', f'{Computermove}.png')

            if os.path.exists(img_path):
                imgAI = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            else:
                raise FileNotFoundError(f"Image not found: {img_path}")

            imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))



                
            # Spiel Ergebniss fälle
           

            def determine_winner(Playermove, Computermove):
                if (Playermove == ROCK and Computermove == SCISSORS) or \
                (Playermove == PAPER and Computermove== ROCK) or \
                (Playermove == SCISSORS and Computermove == PAPER):
                    return 1 # Player wins
                elif (Playermove == ROCK and Computermove == PAPER) or \
                    (Playermove == PAPER and Computermove == SCISSORS) or \
                    (Playermove == SCISSORS and Computermove == ROCK):
                    return 0 # Computer wins
                else:
                    return -1 

            def update_scores(scores, winner):
                if winner == 0:
                    scores[0] += 1 # Player wins
                elif winner == 1:
                    scores[1] += 1 # Computer wins

           

            winner = determine_winner(Playermove, Computermove)
            update_scores(scores, winner)
    

    # Kamera auf dem hintergrund befestigen
    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

         # zeige spieler handzeichen
        if Playermove == 1:
            cv2.putText(imgBG, "Stein", (860, 310), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 6)
        elif Playermove == 2:
            cv2.putText(imgBG, "Papier", (860, 310), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 6)
        elif Playermove == 3:
            cv2.putText(imgBG, "Schere", (860, 310), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 6)


    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.imshow("BG", imgBG)
    

    
    

    key = cv2.waitKey(50)
    if key & 0xFF == 32: # start Programm with space
        startGame = True

        initialTime = time.time()
        stateResult = False
#um das programm zu schließen
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    elif key & 0xFF == 27:
        break        
