# Term Project 3
# Melina Driscoll, msdrisco

import random
import math
import socket
from tkinter import *

def init(data):
    data.startState = True
    data.instructionState = False
    data.gameState = False
    data.game2State = False
    data.loseState = False
    data.winState = False
    data.timer = 200
    data.margin = 10
    data.cellColors = determineBoard(data)
    data.cellCount = 0
    data.startCircles = [[data.width//2-20,data.height//6,data.width//2+20,
    data.height//6+40],[data.width//2-20,data.height-data.height//5,
    data.width//2+20,data.height-data.height//5+40]]
    data.direction1 = 5
    data.direction2 = -5
    data.startCircle = [data.width//2-30,data.height//2-30,data.width//2+30,
    data.height//2+30]
    data.startGhost = [data.startCircle[0]-70,data.startCircle[1],
    data.startCircle[2]-70,data.startCircle[3]]
    data.startLost = False
    data.timerDelay = 100
    data.coins = drawCoins(data)
    data.count = 0
    data.score = 0
    data.lives = 3
    data.numRows = data.height//20
    data.numCols = data.width//20
    data.pacmanTopRow = 41
    data.pacmanLeftCol = 29
    data.pacmanBottomRow = 44
    data.pacmanRightCol = 32
    data.pacmanCenterX = data.pacmanLeftCol*10+15
    data.pacmanCenterY = data.pacmanTopRow*10+15
    data.pacman = [data.pacmanCenterX-15,data.pacmanCenterY-15,
    data.pacmanCenterX+15,data.pacmanCenterY+15]
    data.pacmanDirection = None
    data.ghosts = [[29,30,"tomato"],[27,33,"deepskyblue"],[31,33,"magenta"]]
    data.ghosts2 = [[25,31,"tomato"],[29,31,"deepskyblue"],[33,31,"magenta"],
    [25,35,"peru"],[29,35,"plum"],[33,35,"palegreen"]]
    data.directions = ["Right", "Left", "Up", "Down"]
    data.ghostRowReset = None
    data.ghostColReset = None
    data.ghost1Direction = None
    data.ghost2Direction = None
    data.ghost3Direction = None
    data.ghost4Direction = None
    data.ghost5Direction = None
    data.ghost6Direction = None
    data.switchRoles = False
    data.redCount = 0
    data.coinsSpecial = []
    data.normalGhosts = []
    
def mousePressed(event, data):
    x = event.x
    y = event.y
    #click on begin button to begin the game
    if data.startState:
        if 240 <= x <= 360:
            if 330 <= y <= 380:
                data.startState = False
                data.instructionState = True
    #click on continue button to begin the game
    if data.instructionState:
        if 220 <= x <= 380:
            if 450 <= y <= 500:
                data.instructionState = False
                data.coins = drawCoins(data)
                data.gameState = True

def keyPressed(event, data):
    if data.gameState or data.game2State:
        #changes the direction of pac man based on the key the user presses
        if event.keysym == "Right":
            data.pacmanDirection = "Right"
            #if pacman is valid to move right, move right
            if validToMove(data):
                movePacman(data)
            #if pacman runs into a regular coin
            if getCoins(data) == "regular":
                data.score += 1
            #if pacman runs into a special coin
            if getCoins(data) == "special":
                data.score += 5
                data.switchRoles = True
                count = 0
                #if hit red coin and on level one
                if data.gameState:
                    for ghost in data.ghosts:
                        if not(ghost in data.normalGhosts):
                            data.ghosts[count][2] = "red"
                        count += 1
                #if hit red coin and on level two
                if data.game2State:
                    for ghost in data.ghosts2:
                        if not(ghost in data.normalGhosts):
                            data.ghosts2[count][2] = "red"
                        count += 1
        if event.keysym == "Left":
            data.pacmanDirection = "Left"
            #if valid to move left, move pacman left
            if validToMove(data):
                movePacman(data)
            #if pacman runs into a regular coin
            if getCoins(data) == "regular":
                data.score += 1
            #if pacman runs into a special coin
            if getCoins(data) == "special" or len(data.coinsSpecial) != 0:
                data.score += 5
                data.switchRoles = True
                count = 0
                #if hit red coin and on level one, all ghosts turn red
                if data.gameState:
                    for ghost in data.ghosts:
                        if not(ghost in data.normalGhosts):
                            data.ghosts[count][2] = "red"
                        count += 1
                #if hit red coin and on level two, all ghosts turn red
                if data.game2State:
                    for ghost in data.ghosts2:
                        if not(ghost in data.normalGhosts):
                            data.ghosts2[count][2] = "red"
                        count += 1
        if event.keysym == "Up":
            data.pacmanDirection = "Up"
            #if pacman valid to move up, move pacman up
            if validToMove(data):
                movePacman(data)
            #if pacman runs into a regular coin
            if getCoins(data) == "regular":
                data.score += 1
            #if pacman runs into a special coin
            if getCoins(data) == "special" or len(data.coinsSpecial) != 0:
                data.score += 5
                data.switchRoles = True
                count = 0
                #if hit red coin and on level one, all ghosts turn red
                if data.gameState:
                    for ghost in data.ghosts:
                        if not(ghost in data.normalGhosts):
                            data.ghosts[count][2] = "red"
                        count += 1
                #if hit red coin and on level two, all ghosts turn red
                if data.game2State:
                    for ghost in data.ghosts2:
                        if not(ghost in data.normalGhosts):
                            data.ghosts2[count][2] = "red"
                        count += 1
        if event.keysym == "Down":
            data.pacmanDirection = "Down"
            #if pacman valid to move down, move pacman down
            if validToMove(data):
                movePacman(data)
            #if pacman runs into a regular coin
            if getCoins(data) == "regular":
                data.score += 1
            #if pacman runs into a special coin
            if getCoins(data) == "special":
                data.score += 5
                data.switchRoles = True
                count = 0
                #if hit red coin and on level one, all ghosts turn red
                if data.gameState:
                    for ghost in data.ghosts:
                        if not(ghost in data.normalGhosts):
                            data.ghosts[count][2] = "red"
                        count += 1
                #if hit red coin and on level two, all ghosts turn red
                if data.game2State:
                    for ghost in data.ghosts2:
                        if not(ghost in data.normalGhosts):
                            data.ghosts2[count][2] = "red"
                        count += 1
    if data.loseState or data.winState:
        #if user wants to play level one
        if event.keysym == "1":
            init(data)
            data.startState = False
            data.gameState = True
            data.cellColors = determineBoard(data)
            data.coins = drawCoins(data)
        #if user wants to play level two
        if event.keysym == "2":
            init(data)
            data.startState = False
            data.game2State = True           
            data.cellColors = determineBoard(data) 
            data.coins = drawCoins(data)
    
def timerFired(data):
    if data.startState:
        moveStartCircles(data)
    if data.instructionState and (data.startLost == False):
        #moves sample pac man left to right across the screen
        data.startCircle[0] += 4
        data.startCircle[2] += 4
        data.startGhost[0] += 5
        data.startGhost[2] += 5
        if data.startCircle[0] <= data.startGhost[2]:
            data.startLost = True
    if data.gameState or data.game2State:
        #decrease time left for user to play
        if data.count%4 == 0:
            data.timer -= 1
        if data.gameState:
            data.count += 1
            #if time has run out, player loses
            if data.timer == 0:
                data.gameState = False
                data.game2State = False
                data.winState = True
        if data.game2State:
            data.count += 1
            #if time runs out, player loses
            if data.timer == 100:
                data.gameState = False
                data.game2State = False
                data.winState = True
        #if user has eaten all of the coins, player wins
        if len(data.coins) == 0:
            data.gameState = False
            data.game2State = False
            data.winState = True
        if data.gameState:
            #moves ghost one
            if data.count == 5:
                data.ghosts[0][1] = 26
            #gets best direction for ghost one to move
            data.ghost1Direction = getBestDirection(data,1)
            valid = validGhostMove(data,1)
            if (data.count >= 5):
                if valid:
                    moveGhost(data,1)
                #if best direction is not valid, choose random direction
                if valid == False:
                    if data.count%5 == 0:
                        #data.ghost1Direction = getSecondDirection(data,1)
                        index = random.randint(0,len(data.directions)-1)
                        data.ghost1Direction = data.directions[index]
                        valid = validGhostMove(data,1)
                        if valid:
                            moveGhost(data,1)
            #moves ghost two
            if data.count == 25:
                data.ghosts[1][1] = 26
            #gets best direction for ghost two to move
            data.ghost2Direction = getBestDirection(data,2)
            if (data.count >= 25):
                valid = validGhostMove(data,2)
                if valid:
                    moveGhost(data,2)
                #if best direction is not valid, choose random direction
                if valid == False:
                    if data.count%5 == 0:
                        #data.ghost2Direction = getSecondDirection(data,2)
                        index = random.randint(0,len(data.directions)-1)
                        data.ghost2Direction = data.directions[index]
                        valid = validGhostMove(data,2)
                        if valid:
                            moveGhost(data,2)
            #moves ghost three
            if data.count == 35:
                data.ghosts[2][1] = 26
            #gets best direction for ghost three to move
            data.ghost3Direction = getBestDirection(data,3)
            if (data.count >= 35):
                valid = validGhostMove(data,3)
                if valid:
                    moveGhost(data,3)
                #if best direction is not valid, choose random direction
                if valid == False:
                    if data.count%5 == 0:
                        #data.ghost3Direction = getSecondDirection(data,3)
                        index = random.randint(0,len(data.directions)-1)
                        data.ghost3Direction = data.directions[index]
                        valid = validGhostMove(data,3)
                        if valid:
                            moveGhost(data,3)
        if data.game2State:
            #moves ghost one
            if data.count == 5:
                data.ghosts2[0][1] = 26
            #gets best direction for ghost one to move
            data.ghost1Direction = getBestDirection(data,1)
            if (data.count >= 5):
                if validGhostMove(data,1):
                    moveGhost(data,1)
                #if best direction is not valid, choose random direction
                if not(validGhostMove(data,1)):
                    if data.count%5 == 0:
                        index = random.randint(0,len(data.directions)-1)
                        data.ghost1Direction = data.directions[index]
                    if validGhostMove(data,1):
                        moveGhost(data,1)
            #moves ghost two
            if data.count == 15:
                data.ghosts2[1][1] = 26
            #gets best direction for ghost two to move
            data.ghost2Direction = getBestDirection(data,2)
            if (data.count >= 15):
                if validGhostMove(data,2):
                    moveGhost(data,2)
                #if best direction is not valid, choose random direction
                if not(validGhostMove(data,2)):
                    if data.count%5 == 0:
                        index = random.randint(0,len(data.directions)-1)
                        data.ghost2Direction = data.directions[index]
                    if validGhostMove(data,2):
                        moveGhost(data,2)
            #moves ghost three
            if data.count == 30:
                data.ghosts2[2][1] = 26
            #gets best direction for ghost three to move
            data.ghost3Direction = getBestDirection(data,3)
            if (data.count >= 30):
                if validGhostMove(data,3):
                    moveGhost(data,3)
                #if best direction is not valid, choose random direction
                if not(validGhostMove(data,3)):
                    if data.count%5 == 0:
                        index = random.randint(0,len(data.directions)-1)
                        data.ghost3Direction = data.directions[index]
                    if validGhostMove(data,3):
                        moveGhost(data,3)
            #moves ghost four
            if data.count == 35:
                data.ghosts2[3][1] = 26
            #gets best direction for ghost four to move
            data.ghost4Direction = getBestDirection(data,4)
            if (data.count >= 35):
                if validGhostMove(data,4):
                    moveGhost(data,4)
                #if best direction is not valid, choose random direction
                if not(validGhostMove(data,4)):
                    if data.count%5 == 0:
                        index = random.randint(0,len(data.directions)-1)
                        data.ghost4Direction = data.directions[index]
                    if validGhostMove(data,4):
                        moveGhost(data,4)
            #moves ghost five
            if data.count == 45:
                data.ghosts2[4][1] = 26
            #gets best direction for ghost five to move
            data.ghost5Direction = getBestDirection(data,5)
            if (data.count >= 45):
                if validGhostMove(data,5):
                    moveGhost(data,5)
                #if best direction is not valid, choose random direction
                if not(validGhostMove(data,5)):
                    if data.count%5 == 0:
                        index = random.randint(0,len(data.directions)-1)
                        data.ghost5Direction = data.directions[index]
                    if validGhostMove(data,5):
                        moveGhost(data,5)
            #moves ghost six
            if data.count == 50:
                data.ghosts2[5][1] = 26
            #gets best direction for ghost six to move
            data.ghost6Direction = getBestDirection(data,6)
            if (data.count >= 50):
                if validGhostMove(data,6):
                    moveGhost(data,6)
                #if best direction is not valid, choose random direction
                if not(validGhostMove(data,6)):
                    if data.count%5 == 0:
                        index = random.randint(0,len(data.directions)-1)
                        data.ghost6Direction = data.directions[index]
                    if validGhostMove(data,6):
                        moveGhost(data,6)
        #if player has hit a special coin, receieves a power up to get more
        #points for colliding with the ghosts
        if data.switchRoles:
            data.redCount += 1
            for ghost in data.ghosts:
                if not(ghost in data.normalGhosts):
                    #ghosts flash when the power up is about to end
                    if data.redCount > 30 and data.redCount%2 == 0:
                        data.ghosts[0][2] = "red"
                        data.ghosts[1][2] = "red"
                        data.ghosts[2][2] = "red"
                    if data.redCount > 30 and data.redCount%2 != 0:
                        data.ghosts[0][2] = "white"
                        data.ghosts[1][2] = "white"
                        data.ghosts[2][2] = "white"
        #when powerup has ended, return game to normal
        if data.redCount == 40:
            data.coinsSpecial = []
            data.normalGhosts = []
            data.switchRoles = False
            data.ghosts[0][2] = "tomato"
            data.ghosts[1][2] = "deepskyblue"
            data.ghosts[2][2] = "magenta"
            data.ghosts2[0][2] = "tomato"
            data.ghosts2[1][2] = "deepskyblue"
            data.ghosts2[2][2] = "magenta"
            data.ghosts2[3][2] = "peru"
            data.ghosts2[4][2] = "plum"
            data.ghosts2[5][2] = "palegreen"
            data.redCount = 0
        #check collisions between pacman and each ghost
        checkCollisions(data)
        
def redrawAll(canvas, data):
    canvas.create_rectangle(data.margin,data.margin,data.width-data.margin,
    data.height-data.margin,fill="black")
    if data.startState:
        #draws title and instructions to begin
        canvas.create_text(data.width//2,data.height//3,
        text="Welcome to Pac-Man",fill="plum",font="Arial 50 bold")
        canvas.create_rectangle(data.width//2-60,data.height//2+30,
        data.width//2+60,data.height//2+70,fill="white")
        canvas.create_text(data.width//2,data.height//2+50,
        text="Begin",fill="black",font="Arial 32 bold")
        for circle in data.startCircles:
            canvas.create_oval(circle[0],circle[1],circle[2],circle[3],
            fill="yellow")
    if data.instructionState:
        #draws instructions on how to place the game
        canvas.create_text(data.width//2,data.height//4-60,
        text="Use the arrow keys to move",font="Arial 28",fill="white")
        canvas.create_text(data.width//2,data.height//4-28,
        text="to collect the coins and avoid",font="Arial 28",fill="white")
        canvas.create_text(data.width//2,data.height//4+4,
        text="the ghosts.",font="Arial 28",fill="white")
        canvas.create_text(data.width//2,data.height//4+40,
        text="The red coins are power-ups and ",font="Arial 24",fill="white")
        canvas.create_text(data.width//2,data.height//4+65,
        text="allow Pac-Man to capture the ghosts.",font="Arial 24",
        fill="white")
        #draws example of pac man moving across the screen
        canvas.create_oval(data.startCircle[0],data.startCircle[1],
        data.startCircle[2],data.startCircle[3],fill="yellow")
        canvas.create_polygon(data.startCircle[2],data.startCircle[1],
        data.startCircle[2]-30,data.startCircle[1]+30,data.startCircle[2],
        data.startCircle[3],fill="black")
        #draws ghost following pacman
        canvas.create_oval(data.startGhost[0],data.startGhost[1],
        data.startGhost[2],data.startGhost[3],fill="deepskyblue")
        canvas.create_oval(data.startGhost[0]+16,data.startGhost[1]+16,
        data.startGhost[0]+22,data.startGhost[1]+22,fill="black")
        canvas.create_oval(data.startGhost[0]+44,data.startGhost[1]+16,
        data.startGhost[0]+38,data.startGhost[1]+22,fill="black")
        canvas.create_rectangle(data.startGhost[0]+15,data.startGhost[1]+38,
        data.startGhost[0]+45,data.startGhost[1]+41,fill="black")
        if data.startLost:
            canvas.create_text(data.width//2,data.height//2+70,text="YOU LOST",
            font="Arial 34 bold", fill="plum")
        #draws the button to continue to the game
        canvas.create_rectangle(220,450,380,500,fill="white")
        canvas.create_text(data.width//2,475,text="Continue",font="Arial 28 bold",
        fill="black")
    if data.gameState or data.game2State:
        #draws board
        for x in range(0,data.height,10):
            for y in range(0,data.width,10):
                if data.cellCount < 3600:
                    #draws each cell blue or black
                    color = data.cellColors[y//10][x//10]
                    canvas.create_rectangle(x+10,y+10,x+20,y+20,
                    fill=color,outline=color)
                    data.cellCount += 1
                if data.cellCount == 3600:
                    data.cellCount = 0
        #draws coins
        for coin in data.coins:
            canvas.create_oval(coin[0],coin[1],coin[2],coin[3],fill=coin[4])
        #draws the score
        scoreText = "Score: %d" % (data.score)
        canvas.create_text(63,28,text=scoreText,fill="white",font="Arial 20")
        #draws the lives remaining
        livesText = "Lives: %s" % (data.lives)
        canvas.create_text(300,28,text=livesText,fill="white",font="Arial 20")
        if data.gameState:
            #draws the time remaining
            timerText = "Time left: %d" % (data.timer)
            canvas.create_text(530,28,text=timerText,fill="white",
            font="Arial 20")
        if data.game2State:
            #draws the time remaining
            timerText = "Time left: %d" % (data.timer-100)
            canvas.create_text(530,28,text=timerText,fill="white",
            font="Arial 20")
        #draws pac man
        canvas.create_oval(data.pacmanLeftCol*10,data.pacmanTopRow*10,
        data.pacmanRightCol*10,data.pacmanBottomRow*10,fill="yellow")
        if data.pacmanDirection == "Right" or data.pacmanDirection == None:
            canvas.create_polygon(data.pacmanRightCol*10, data.pacmanTopRow*10,
            data.pacmanRightCol*10,data.pacmanBottomRow*10,
            data.pacmanRightCol*10-15,data.pacmanTopRow*10+15,fill="black")
        if data.pacmanDirection == "Left":
            canvas.create_polygon(data.pacmanLeftCol*10, data.pacmanTopRow*10,
            data.pacmanLeftCol*10,data.pacmanBottomRow*10,
            data.pacmanLeftCol*10+15,data.pacmanTopRow*10+15,fill="black")
        if data.pacmanDirection == "Up":
            canvas.create_polygon(data.pacmanLeftCol*10, data.pacmanTopRow*10,
            data.pacmanRightCol*10-15,data.pacmanBottomRow*10-15,
            data.pacmanRightCol*10,data.pacmanTopRow*10,fill="black")
        if data.pacmanDirection == "Down":
            canvas.create_polygon(data.pacmanLeftCol*10, data.pacmanBottomRow*10,
            data.pacmanLeftCol*10+15,data.pacmanBottomRow*10-15,
            data.pacmanRightCol*10,data.pacmanBottomRow*10,fill="black")
        #draws ghosts
        if data.gameState:
            for ghost in data.ghosts:
                canvas.create_oval(ghost[0]*10,ghost[1]*10,ghost[0]*10+30,
                ghost[1]*10+30,fill=ghost[2])
                canvas.create_oval(ghost[0]*10+8,ghost[1]*10+8,ghost[0]*10+11,
                ghost[1]*10+10,fill="black")
                canvas.create_oval(ghost[0]*10+18,ghost[1]*10+8,ghost[0]*10+21,
                ghost[1]*10+10,fill="black")
                canvas.create_oval(ghost[0]*10+10,ghost[1]*10+18,ghost[0]*10+20,
                ghost[1]*10+20,fill="black")
        if data.game2State:
            for ghost in data.ghosts2:
                canvas.create_oval(ghost[0]*10,ghost[1]*10,ghost[0]*10+30,
                ghost[1]*10+30,fill=ghost[2])
                canvas.create_oval(ghost[0]*10+8,ghost[1]*10+8,ghost[0]*10+11,
                ghost[1]*10+10,fill="black")
                canvas.create_oval(ghost[0]*10+18,ghost[1]*10+8,ghost[0]*10+21,
                ghost[1]*10+10,fill="black")
                canvas.create_oval(ghost[0]*10+10,ghost[1]*10+18,ghost[0]*10+20,
                ghost[1]*10+20,fill="black")
    if data.loseState:
        scoreText = "Score: %d" % (data.score)
        canvas.create_text(data.width//2,data.height//3+35,text="YOU LOST",
        font="Arial 40 bold",fill="plum")
        canvas.create_text(data.width//2,data.height//3+85,
        text=scoreText,font="Arial 30",fill="yellow")
        canvas.create_text(data.width//2,data.height//3+135,
        text="Press '1' to play level 1",font="Arial 22",fill="plum")
        canvas.create_text(data.width//2,data.height//3+165,
        text="Press '2' to play level 2",font="Arial 22",fill="plum")
    if data.winState:
        scoreText = "Score: %d" % (data.score)
        canvas.create_text(data.width//2,data.height//3+35,text="YOU WON",
        font="Arial 40 bold",fill="plum")
        canvas.create_text(data.width//2,data.height//3+85,
        text=scoreText,font="Arial 30",fill="yellow")
        canvas.create_text(data.width//2,data.height//3+135,
        text="Press '1' to play level 1",font="Arial 22",fill="plum")
        canvas.create_text(data.width//2,data.height//3+165,
        text="Press '2' to play level 2",font="Arial 22",fill="plum")
            
def moveStartCircles(data):
    #on start screen, move circles across the screen
    data.startCircles[0][0] += data.direction1
    data.startCircles[0][2] += data.direction1
    data.startCircles[1][0] += data.direction2
    data.startCircles[1][2] += data.direction2
    if data.startCircles[0][0] <= data.margin:
        data.direction1 = 5
    if data.startCircles[0][2] >= data.width-data.margin:
        data.direction1 = -5
    if data.startCircles[1][0] <= data.margin:
        data.direction2 = 5
    if data.startCircles[1][2] >= data.width-data.margin:
        data.direction2 = -5

def determineBoard(data):
    if data.game2State == True:
        return drawBoard2(data)
    else:
        return drawBoard1(data)
        
def drawBoard1(data):
    result = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
    [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
    [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
    [],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for x in range(0,data.height,10):
        for y in range(0,60):
            #top
            if (10 <= x <= 570 and 10 <= y*10 <= 20):
                result[y].append("blue")
            #top left box
            elif (80 <= x <= 140 and 80 <= y*10 <= 140):
                result[y].append("blue")
            #top middle left box
            elif (200 <= x <= 230 and 80 <= y*10 <= 220):
                result[y].append("blue")
            #top middle middle box
            elif (290 <= x <= 290 and 80 <= y*10 <= 220):
                result[y].append("blue")
            #top middle right box
            elif (350 <= x <= 380 and 80 <= y*10 <= 220):
                result[y].append("blue")
            #top middle box
            elif (140 <= x <= 440 and 200 <= y*10 <= 230):
                result[y].append("blue")
            #top right box
            elif (440 <= x <= 500 and 80 <= y*10 <= 140):
                result[y].append("blue")
            #ghost home
            elif (260 <= x <= 330 and 290 <= y*10 <= 350):
                result[y].append("cornflowerblue")
            #topmiddle left box
            elif (140 <= x <= 200 and 290 <= y*10 <= 350):
                result[y].append("blue")
            #topmiddle right box
            elif (380 <= x <= 450 and 290 <= y*10 <= 350):
                result[y].append("blue")
            #middle left box
            elif (170 <= x <= 260 and 440 <= y*10 <= 470):
                result[y].append("blue")
            #middle right box
            elif (320 <= x <= 410 and 440 <= y*10 <= 470):
                result[y].append("blue")
            #bottom left box
            elif (80 <= x <= 140 and 470 <= y*10 <= 500):
                result[y].append("blue")
            #small bottom left box
            elif (140 <= x <= 200 and 500 <= y*10 <= 500):
                result[y].append("blue")
            #bottom right box
            elif (440 <= x <= 500 and 470 <= y*10 <= 500):
                result[y].append("blue")
            #small bottom right box
            elif (380 <= x <= 440 and 500 <= y*10 <= 500):
                result[y].append("blue")
            #bottom middle box
            elif (260 <= x <= 320 and 500 <= y*10 <= 500):
                result[y].append("blue")
            #top right outline
            elif (560 <= x <= 570 and 20 <= y*10 <= 200):
                result[y].append("blue")
            elif (500 <= x <= 570 and 200 <= y*10 <= 210):
                result[y].append("blue")
            elif (500 <= x <= 510 and 200 <= y*10 <= 290):
                result[y].append("blue")
            elif (500 <= x <= 600 and 280 <= y*10 <= 290):
                result[y].append("blue")
            #bottom right outline
            elif (500 <= x <= 600 and 350 <= y*10 <= 360):
                result[y].append("blue")
            elif (500 <= x <= 510 and 350 <= y*10 <= 410):
                result[y].append("blue")
            elif (500 <= x <= 560 and 400 <= y*10 <= 410):
                result[y].append("blue")
            elif (560 <= x <= 570 and 400 <= y*10 <= 570):
                result[y].append("blue")
            #bottom
            elif (10 <= x <= 560 and 560 <= y*10 <= 570):
                result[y].append("blue")
            #bottom left outline
            elif (10 <= x <= 20 and 400 <= y*10 <= 570):
                result[y].append("blue")
            elif (10 <= x <= 80 and 400 <= y*10 <= 410):
                result[y].append("blue")
            elif (70 <= x <= 80 and 350 <= y*10 <= 410):
                result[y].append("blue")
            elif (0 <= x <= 80 and 350 <= y*10 <= 360):
                result[y].append("blue")
            #top left outline
            elif (0 <= x <= 80 and 280 <= y*10 <= 290):
                result[y].append("blue")
            elif (70 <= x <= 80 and 200 <= y*10 <= 290):
                result[y].append("blue")
            elif (10 <= x <= 80 and 200 <= y*10 <= 210):
                result[y].append("blue")
            elif (10 <= x <= 20 and 20 <= y*10 <= 210):
                result[y].append("blue")
            else:
                result[y].append("black")
    return result
    
def drawBoard2(data):
    result = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
    [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
    [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
    [],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for x in range(0,data.height,10):
        for y in range(0,60):
            #top
            if (10 <= x <= 570 and 10 <= y*10 <= 20):
                result[y].append("blue")
            #top left box
            elif (80 <= x <= 140 and 80 <= y*10 <= 140):
                result[y].append("blue")
            #top middle left box
            elif (200 <= x <= 230 and 80 <= y*10 <= 220):
                result[y].append("blue")
            #top middle middle box
            elif (290 <= x <= 290 and 80 <= y*10 <= 220):
                result[y].append("blue")
            #top middle right box
            elif (350 <= x <= 380 and 80 <= y*10 <= 220):
                result[y].append("blue")
            #top middle box
            elif (140 <= x <= 440 and 200 <= y*10 <= 230):
                result[y].append("blue")
            #top right box
            elif (440 <= x <= 570 and 20 <= y*10 <= 140):
                result[y].append("blue")
            #ghost home
            elif (220 <= x <= 360 and 290 <= y*10 <= 380):
                result[y].append("cornflowerblue")
            #topmiddle left box
            elif (140 <= x <= 200 and 290 <= y*10 <= 380):
                result[y].append("blue")
            #topmiddle right box
            elif (380 <= x <= 450 and 290 <= y*10 <= 380):
                result[y].append("blue")
            #middle left box
            elif (170 <= x <= 300 and 440 <= y*10 <= 470):
                result[y].append("blue")
            #middle right box
            elif (300 <= x <= 410 and 440 <= y*10 <= 470):
                result[y].append("blue")
            #bottom left box
            elif (80 <= x <= 140 and 470 <= y*10 <= 500):
                result[y].append("blue")
            #small bottom left box
            elif (140 <= x <= 200 and 500 <= y*10 <= 500):
                result[y].append("blue")
            #bottom right box
            elif (440 <= x <= 500 and 470 <= y*10 <= 500):
                result[y].append("blue")
            #small bottom right box
            elif (380 <= x <= 440 and 500 <= y*10 <= 500):
                result[y].append("blue")
            #bottom middle box
            elif (260 <= x <= 320 and 500 <= y*10 <= 500):
                result[y].append("blue")
            #top right outline
            elif (560 <= x <= 570 and 20 <= y*10 <= 200):
                result[y].append("blue")
            elif (500 <= x <= 570 and 200 <= y*10 <= 210):
                result[y].append("blue")
            elif (500 <= x <= 510 and 200 <= y*10 <= 290):
                result[y].append("blue")
            elif (500 <= x <= 600 and 280 <= y*10 <= 290):
                result[y].append("blue")
            #bottom right outline
            elif (500 <= x <= 600 and 350 <= y*10 <= 360):
                result[y].append("blue")
            elif (500 <= x <= 510 and 350 <= y*10 <= 410):
                result[y].append("blue")
            elif (500 <= x <= 560 and 400 <= y*10 <= 410):
                result[y].append("blue")
            elif (560 <= x <= 570 and 400 <= y*10 <= 570):
                result[y].append("blue")
            #bottom
            elif (10 <= x <= 560 and 560 <= y*10 <= 570):
                result[y].append("blue")
            #bottom left outline
            elif (10 <= x <= 20 and 400 <= y*10 <= 570):
                result[y].append("blue")
            elif (10 <= x <= 80 and 400 <= y*10 <= 410):
                result[y].append("blue")
            elif (70 <= x <= 80 and 350 <= y*10 <= 410):
                result[y].append("blue")
            elif (0 <= x <= 80 and 350 <= y*10 <= 360):
                result[y].append("blue")
            #top left outline
            elif (0 <= x <= 80 and 280 <= y*10 <= 290):
                result[y].append("blue")
            elif (70 <= x <= 80 and 200 <= y*10 <= 290):
                result[y].append("blue")
            elif (10 <= x <= 80 and 200 <= y*10 <= 210):
                result[y].append("blue")
            elif (10 <= x <= 20 and 20 <= y*10 <= 210):
                result[y].append("blue")
            else:
                result[y].append("black")
    return result
    
def validToMove(data):
    #avoids pacman from running into any walls
    if data.pacmanDirection == "Right":
        data.pacmanRightCol += 2
        data.pacmanLeftCol += 2
        #if pacman is going through the tunnel
        if 31 <= data.pacmanTopRow <= 34 and data.pacmanRightCol > 59:
            data.pacmanLeftCol = 2
            data.pacmanRightCol = 5
        elif 50 <= data.pacmanTopRow <= 51 and \
        (38 < data.pacmanRightCol > 51 or 9 < data.pacmanRightCol > 21 or \
        27 < data.pacmanRightCol > 33):
            data.pacmanRightCol -= 2
            data.pacmanLeftCol -= 2
            return False
        elif 7 <= data.pacmanTopRow <= 21 and 25 <= data.pacmanRightCol < 35:
            data.pacmanRightCol -= 2
            data.pacmanLeftCol -= 2
            return False
        else:
            #if the cell to the right is black, is valid to move
            row = data.pacmanTopRow-1
            col = data.pacmanRightCol-1
            row2 = data.pacmanBottomRow-1
            if data.cellColors[row][col]=="black" and \
            data.cellColors[row2][col] == "black":
                return True
            else:
                data.pacmanRightCol -= 2
                data.pacmanLeftCol -= 2
                return False
    elif data.pacmanDirection == "Left":
        data.pacmanRightCol -= 2
        data.pacmanLeftCol -= 2
        #if pacman is going through the tunnel
        if 31 <= data.pacmanTopRow <= 34 and data.pacmanLeftCol < 0:
            data.pacmanLeftCol = 55
            data.pacmanRightCol = 58
        elif 50 <= data.pacmanTopRow <= 51 and \
        (38 < data.pacmanLeftCol > 51 or 9 < data.pacmanRightCol > 22 or \
        27 < data.pacmanRightCol > 34):
            data.pacmanRightCol += 2
            data.pacmanLeftCol += 2
            return False
        else:
            #if the cell to the left is black, is valid to move
            row = data.pacmanTopRow-1
            col = data.pacmanLeftCol-1
            row2 = data.pacmanBottomRow-1
            if data.cellColors[row][col]=="black" and \
            data.cellColors[row2][col]=="black":
                return True
            else:
                data.pacmanRightCol += 2
                data.pacmanLeftCol += 2
                return False
    elif data.pacmanDirection == "Up":
        data.pacmanTopRow -= 2
        data.pacmanBottomRow -= 2
        #if the cell above is black, is valid to move
        row = data.pacmanTopRow-1
        col = data.pacmanLeftCol-1
        col2 = data.pacmanRightCol-1
        if data.cellColors[row][col]=="black" and \
        data.cellColors[row][col2] == "black":
            return True
        else:
            data.pacmanTopRow += 2
            data.pacmanBottomRow += 2
            return False
    elif data.pacmanDirection == "Down":
        data.pacmanTopRow += 2
        data.pacmanBottomRow += 2
        if 49 < data.pacmanBottomRow <= 52 and 28 < data.pacmanLeftCol < 33:
            data.pacmanTopRow -= 2
            data.pacmanBottomRow -= 2
            return False
        elif 6 <= data.pacmanTopRow <= 21 and 29 <= data.pacmanLeftCol < 31:
            data.pacmanTopRow -= 2
            data.pacmanBottomRow -= 2
            return False
        #if the cell below is black, is valid to move
        row = data.pacmanBottomRow-1
        col = data.pacmanLeftCol-1
        col2 = data.pacmanRightCol-1
        if data.cellColors[row][col]=="black" and \
        data.cellColors[row][col2]=="black":
            return True
        else:
            data.pacmanTopRow -= 2
            data.pacmanBottomRow -= 2
            return False
    else:
        return True
        
def validGhostMove(data,num):
    if num == 1:
        direction = data.ghost1Direction
    if num == 2:
        direction = data.ghost2Direction
    if num == 3:
        direction = data.ghost3Direction
    if num == 4:
        direction = data.ghost4Direction
    if num == 5:
        direction = data.ghost5Direction
    if num == 6:
        direction = data.ghost6Direction
    #avoids the ghost from running into any walls
    if data.gameState:
        if direction == "Right":
            data.ghosts[num-1][0] += 1
            if ghostsCollide(data,num):
                data.ghosts[num-1][0] -= 1
                return False
            if ghostsCollide(data,num) == None:
                if 31 <= data.ghosts[num-1][1] <= 34 and \
                data.ghosts[num-1][0]+3 > 59:
                    data.ghosts[num-1][0] = 0
                else:
                    #if the cell to the right is black, is valid to move
                    row = data.ghosts[num-1][1]-1
                    col = data.ghosts[num-1][0]+2
                    row2 = data.ghosts[num-1][1]+2
                    if data.cellColors[row][col]=="black" and \
                    data.cellColors[row2][col] == "black":
                        return True
                    else:
                        data.ghosts[num-1][0] -= 1
                        return False
        elif direction == "Left":
            data.ghosts[num-1][0] -= 1
            if ghostsCollide(data,num):
                data.ghosts[num-1][0] += 1
                return False
            if ghostsCollide(data,num) == None:
                if 31 <= data.ghosts[num-1][1] <= 34 and data.ghosts[num-1][0] < 0:
                    data.ghosts[num-1][0] = 56
                else:
                    #if the cell to the left is black, is valid to move
                    row = data.ghosts[num-1][1]-1
                    col = data.ghosts[num-1][0]-1
                    row2 = data.ghosts[num-1][1]+2
                    if data.cellColors[row][col]=="black" and \
                    data.cellColors[row2][col]=="black":
                        return True
                    else:
                        data.ghosts[num-1][0] += 1
                        return False
        elif direction == "Up":
            data.ghosts[num-1][1] -= 1
            if ghostsCollide(data,num):
                data.ghosts[num-1][1] += 1
                return False
            if ghostsCollide(data,num) == None:
                #if the cell above is black, is valid to move
                row = data.ghosts[num-1][1]-1
                col = data.ghosts[num-1][0]-1
                col2 = data.ghosts[num-1][0]+2
                if data.cellColors[row][col]=="black" and \
                data.cellColors[row][col2]=="black":
                    return True
                else:
                    data.ghosts[num-1][1] += 1
                    return False
        elif direction == "Down":
            data.ghosts[num-1][1] += 1
            if ghostsCollide(data,num):
                data.ghosts[num-1][1] -= 1
                return False
            if ghostsCollide(data,num) == None:
                #if the cell below is black, is valid to move
                row = data.ghosts[num-1][1]+2
                col = data.ghosts[num-1][0]-1
                col2 = data.ghosts[num-1][0]+2
                if data.cellColors[row][col]=="black" and \
                data.cellColors[row][col2] == "black":
                    return True
                else:
                    data.ghosts[num-1][1] -= 1
                    return False
        else:
            return True
    if data.game2State:
        if direction == "Right":
            data.ghosts2[num-1][0] += 1
            if ghostsCollide(data,num):
                data.ghosts2[num-1][0] -= 1
                return False
            if ghostsCollide(data,num) == None:
                if 31 <= data.ghosts2[num-1][1] <= 34 and \
                data.ghosts2[num-1][0]+3 > 59:
                    data.ghosts2[num-1][0] = 0
                else:
                    #if the cell to the right is black, is valid to move
                    row = data.ghosts2[num-1][1]-1
                    col = data.ghosts2[num-1][0]+2
                    row2 = data.ghosts2[num-1][1]+2
                    if data.cellColors[row][col]=="black" and \
                    data.cellColors[row2][col] == "black":
                        return True
                    else:
                        data.ghosts2[num-1][0] -= 1
                        return False
        elif direction == "Left":
            data.ghosts2[num-1][0] -= 1
            if ghostsCollide(data,num):
                data.ghosts2[num-1][0] += 1
                return False
            if ghostsCollide(data,num) == None:
                if 31 <= data.ghosts2[num-1][1] <= 34 and \
                data.ghosts2[num-1][0] < 0:
                    data.ghosts2[num-1][0] = 56
                else:
                    #if the cell to the left is black, is valid to move
                    row = data.ghosts2[num-1][1]-1
                    col = data.ghosts2[num-1][0]-1
                    row2 = data.ghosts2[num-1][1]+2
                    if data.cellColors[row][col]=="black" and \
                    data.cellColors[row2][col]=="black":
                        return True
                    else:
                        data.ghosts2[num-1][0] += 1
                        return False
        elif direction == "Up":
            data.ghosts2[num-1][1] -= 1
            if ghostsCollide(data,num):
                data.ghosts2[num-1][1] += 1
                return False
            if ghostsCollide(data,num) == None:
                #if the cell above is black, is valid to move
                row = data.ghosts2[num-1][1]-1
                col = data.ghosts2[num-1][0]-1
                col2 = data.ghosts2[num-1][0]+2
                if data.cellColors[row][col]=="black" and \
                data.cellColors[row][col2]=="black":
                    return True
                else:
                    data.ghosts2[num-1][1] += 1
                    return False
        elif direction == "Down":
            data.ghosts2[num-1][1] += 1
            if ghostsCollide(data,num):
                data.ghosts2[num-1][1] -= 1
                return False
            if ghostsCollide(data,num) == None:
                #if the cell below is black, is valid to move
                row = data.ghosts2[num-1][1]+2
                col = data.ghosts2[num-1][0]-1
                col2 = data.ghosts2[num-1][0]+2
                if data.cellColors[row][col]=="black" and \
                data.cellColors[row][col2] == "black":
                    return True
                else:
                    data.ghosts2[num-1][1] -= 1
                    return False
        else:
            return True
                
def movePacman(data):
    if data.pacmanDirection == "Right":
        data.pacmanLeftCol += 1
        data.pacmanRightCol += 1
        if data.pacmanTopRow == 32 and data.pacmanRightCol > 59:
            data.pacmanLeftCol = 0
            data.pacmanRightCol = 3
    if data.pacmanDirection == "Left":
        data.pacmanLeftCol -= 1
        data.pacmanRightCol -= 1
        if data.pacmanTopRow == 32 and data.pacmanLeftCol < 0:
            data.pacmanLeftCol = 56
            data.pacmanRightCol = 59
    if data.pacmanDirection == "Up":
        data.pacmanTopRow -= 1
        data.pacmanBottomRow -= 1
    if data.pacmanDirection == "Down":
        data.pacmanTopRow += 1
        data.pacmanBottomRow += 1
        
def moveGhost(data,num):
    if data.gameState:
        if data.count%50 == 0:
            if num == 1:
                direction = data.ghost1Direction
            if num == 2:
                direction = data.ghost2Direction
            if num == 3:
                direction = data.ghost3Direction
            #rightCol = data.ghosts[num-1][0]+3
            #leftCol = data.ghosts[num-1][0]
            #topRow = data.ghosts[num-1][1]
            #bottomRow = data.ghosts[num-1][1]+3
            if direction == "Right":
                data.ghosts[num-1][0] += 1
                if data.ghosts[num-1][1] == 32 and data.ghosts[num-1][0]+3 > 59:
                    data.ghosts[num-1][0] = 0
            if direction == "Left":
                data.ghosts[num-1][0] -= 1
                if data.ghosts[num-1][1] == 32 and data.ghosts[num-1][0] < 0:
                    data.ghosts[num-1][0] = 56
            if direction == "Up":
                data.ghosts[num-1][1] -= 1
            if direction == "Down":
                data.ghosts[num-1][1] += 1
    if data.game2State:
        if data.count%50 == 0:
            if num == 1:
                direction = data.ghost1Direction
            if num == 2:
                direction = data.ghost2Direction
            if num == 3:
                direction = data.ghost3Direction
            if num == 4:
                direction = data.ghost4Direction
            if num == 5:
                direction = data.ghost5Direction
            if num == 6:
                direction = data.ghost6Direction
            #rightCol = data.ghosts[num-1][0]+3
            #leftCol = data.ghosts[num-1][0]
            #topRow = data.ghosts[num-1][1]
            #bottomRow = data.ghosts[num-1][1]+3
            if direction == "Right":
                data.ghosts2[num-1][0] += 2
                if data.ghosts2[num-1][1] == 32 and data.ghosts2[num-1][0]+3 > 59:
                    data.ghosts2[num-1][0] = 0
            if direction == "Left":
                data.ghosts2[num-1][0] -= 2
                if data.ghosts2[num-1][1] == 32 and data.ghosts2[num-1][0] < 0:
                    data.ghosts2[num-1][0] = 56
            if direction == "Up":
                data.ghosts2[num-1][1] -= 2
            if direction == "Down":
                data.ghosts2[num-1][1] += 2
        
def drawCoins(data):
    results = []
    for x in range(0,60):
        for y in range(0,60):
            if data.cellColors[y-1][x-1] == "black" and x%3 == 0 and y%3==0:
                if not((x*10 < 50 or x*10 > 560) and \
                ((300 > y*10 or y*10 > 340)) or \
                (y*10 < 50 or y*10 > 560) or \
                ((x*10 > 480 or x*10 < 120) and \
                (190 < y*10 < 300 or 340 < y*10 < 410))):
                    if x*10 > 10:
                        results.append([x*10,y*10,x*10+10,y*10+10,"pink"])
    
    #create power up coins
    results[2][4]="red"
    results[2][0]-=3
    results[2][2]+=3
    results[2][1]-=3
    results[2][3]+=3
    #this power up coin is only in level one
    if data.gameState:
        results[120][4]="red"
        results[120][0]-=3
        results[120][2]+=3
        results[120][1]-=3
        results[120][3]+=3
    results[50][4]="red"
    results[50][0]-=3
    results[50][2]+=3
    results[50][1]-=3
    results[50][3]+=3
    results[67][4]="red"
    results[67][0]-=3
    results[67][2]+=3
    results[67][1]-=3
    results[67][3]+=3
    results[90][4]="red"
    results[90][0]-=3
    results[90][2]+=3
    results[90][1]-=3
    results[90][3]+=3
    results[9][4]="red"
    results[9][0]-=3
    results[9][2]+=3
    results[9][1]-=3
    results[9][3]+=3
    return results
        
def getCoins(data):
    for coin in data.coins:
        leftcol = coin[0]//10
        rightcol = (coin[0]+10)//10
        toprow = coin[1]//10
        bottomrow = (coin[1]+10)//10
        if data.pacmanLeftCol <= leftcol <= data.pacmanRightCol or \
        data.pacmanLeftCol <= rightcol <= data.pacmanRightCol:
            if data.pacmanTopRow <= toprow <= data.pacmanBottomRow or \
            data.pacmanTopRow <= bottomrow <= data.pacmanBottomRow:
                data.coins.remove(coin)
                if coin[4] == "red":
                    data.coinsSpecial.append(coin)
                    return "special"
                else:
                    return "regular"
    
def checkCollisions(data):
    if data.gameState:
        if data.switchRoles == False:
            count = -1
            for ghost in data.ghosts:
                count += 1
                if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                    if count == 0:
                        data.ghostRowReset = 29
                        data.ghostColReset = 30
                    if count == 1:
                        data.ghostRowReset = 27
                        data.ghostColReset = 33
                    if count == 2:
                        data.ghostRowReset = 31
                        data.ghostColReset = 33
                    data.ghosts[count][0] = data.ghostRowReset
                    data.ghosts[count][1] = data.ghostColReset
                    data.lives -= 1
                    if data.lives == 0:
                        data.gameState = False
                        data.loseState = True
        if data.switchRoles:
            count = -1
            for ghost in data.ghosts:
                count += 1
                if count == 0:
                    row = 29
                    col = 30
                    color = "tomato"
                    if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                    ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                    (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                    ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                        if not(ghost in data.normalGhosts):
                            data.score += 10
                            data.normalGhosts.append(ghost)
                            data.ghosts[count][2] = color
                            data.ghosts[count][0] = row
                            data.ghosts[count][1] = col
                        else:
                            data.ghosts[count][0] = row
                            data.ghosts[count][1] = col
                            data.lives -= 1
                            if data.lives == 0:
                                data.gameState = False
                                data.loseState = True
                if count == 1:
                    row = 27
                    col = 33
                    color = "deepskyblue"
                    if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                    ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                    (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                    ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                        if not(ghost in data.normalGhosts):
                            data.score += 10
                            data.normalGhosts.append(ghost)
                            data.ghosts[count][2] = color
                            data.ghosts[count][0] = row
                            data.ghosts[count][1] = col
                        else:
                            data.ghosts[count][0] = row
                            data.ghosts[count][1] = col
                            data.lives -= 1
                            if data.lives == 0:
                                data.gameState = False
                                data.loseState = True
                if count == 2:
                    row = 31
                    col = 33
                    color = "magenta"
                    if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                    ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                    (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                    ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                        if not(ghost in data.normalGhosts):
                            data.score += 10
                            data.normalGhosts.append(ghost)
                            data.ghosts[count][2] = color
                            data.ghosts[count][0] = row
                            data.ghosts[count][1] = col
                        else:
                            data.ghosts[count][0] = row
                            data.ghosts[count][1] = col
                            data.lives -= 1
                            if data.lives == 0:
                                data.gameState = False
                                data.loseState = True
    if data.game2State:
        if data.switchRoles == False:
            count = -1
            for ghost in data.ghosts2:
                count += 1
                if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                    if count == 0:
                        data.ghosts2[count][0] = 27
                        data.ghosts2[count][1] = 29
                    if count == 1:
                        data.ghosts2[count][0] = 27
                        data.ghosts2[count][1] = 32
                    if count == 2:
                        data.ghosts2[count][0] = 27
                        data.ghosts2[count][1] = 35
                    if count == 3:
                        data.ghosts2[count][0] = 31
                        data.ghosts2[count][1] = 29
                    if count == 4:
                        data.ghosts2[count][0] = 31
                        data.ghosts2[count][1] = 32
                    if count == 5:
                        data.ghosts2[count][0] = 31
                        data.ghosts2[count][1] = 35
                    data.lives -= 1
                    if data.lives == 0:
                        data.game2State = False
                        data.loseState = True
        if data.switchRoles:
            count = -1
            for ghost in data.ghosts2:
                count += 1
                if count == 0:
                    row = 27
                    col = 29
                    color = "tomato"
                    if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                    ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                    (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                    ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                        if not(ghost in data.normalGhosts):
                            data.score += 10
                            data.normalGhosts.append(ghost)
                            data.ghosts2[count][2] = color
                            data.ghosts2[count][0] = row
                            data.ghosts2[count][1] = col
                        else:
                            data.ghosts2[count][0] = row
                            data.ghosts2[count][1] = col
                            data.lives -= 1
                            if data.lives == 0:
                                data.game2State = False
                                data.loseState = True
                if count == 1:
                    row = 27
                    col = 32
                    color = "deepskyblue"
                    if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                    ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                    (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                    ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                        if not(ghost in data.normalGhosts):
                            data.score += 10
                            data.normalGhosts.append(ghost)
                            data.ghosts2[count][2] = color
                            data.ghosts2[count][0] = row
                            data.ghosts2[count][1] = col
                        else:
                            data.ghosts2[count][0] = row
                            data.ghosts2[count][1] = col
                            data.lives -= 1
                            if data.lives == 0:
                                data.game2State = False
                                data.loseState = True
                if count == 2:
                    row = 27
                    col = 35
                    color = "magenta"
                    if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                    ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                    (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                    ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                        if not(ghost in data.normalGhosts):
                            data.score += 10
                            data.normalGhosts.append(ghost)
                            data.ghosts2[count][2] = color
                            data.ghosts2[count][0] = row
                            data.ghosts2[count][1] = col
                        else:
                            data.ghosts2[count][0] = row
                            data.ghosts2[count][1] = col
                            data.lives -= 1
                            if data.lives == 0:
                                data.game2State = False
                                data.loseState = True
                if count == 3:
                    row = 31
                    col = 29
                    color = "peru"
                    if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                    ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                    (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                    ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                        if not(ghost in data.normalGhosts):
                            data.score += 10
                            data.normalGhosts.append(ghost)
                            data.ghosts2[count][2] = color
                            data.ghosts2[count][0] = row
                            data.ghosts2[count][1] = col
                        else:
                            data.ghosts2[count][0] = row
                            data.ghosts2[count][1] = col
                            data.lives -= 1
                            if data.lives == 0:
                                data.game2State = False
                                data.loseState = True
                if count == 4:
                    row = 31
                    col = 32
                    color = "plum"
                    if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                    ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                    (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                    ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                        if not(ghost in data.normalGhosts):
                            data.score += 10
                            data.normalGhosts.append(ghost)
                            data.ghosts2[count][2] = color
                            data.ghosts2[count][0] = row
                            data.ghosts2[count][1] = col
                        else:
                            data.ghosts2[count][0] = row
                            data.ghosts2[count][1] = col
                            data.lives -= 1
                            if data.lives == 0:
                                data.game2State = False
                                data.loseState = True
                if count == 5:
                    row = 31
                    col = 35
                    color = "palegreen"
                    if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                    ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                    (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                    ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                        if not(ghost in data.normalGhosts):
                            data.score += 10
                            data.normalGhosts.append(ghost)
                            data.ghosts2[count][2] = color
                            data.ghosts2[count][0] = row
                            data.ghosts2[count][1] = col
                        else:
                            data.ghosts2[count][0] = row
                            data.ghosts2[count][1] = col
                            data.lives -= 1
                            if data.lives == 0:
                                data.game2State = False
                                data.loseState = True
                    
def getBestDirection(data,ghost):
    bestDistance = 10000
    bestDirection = None
    if data.gameState:
        if ghost == 1:
            direction = data.ghost1Direction
        if ghost == 2:
            direction = data.ghost2Direction
        if ghost == 3:
            direction = data.ghost3Direction
        for direction in data.directions:
            if direction == "Left":
                data.ghosts[ghost-1][0] -= 2
                distanceCols = math.fabs(data.pacmanLeftCol - \
                data.ghosts[ghost-1][0])
                distanceRows = math.fabs(data.pacmanTopRow - \
                data.ghosts[ghost-1][1])
                distance = distanceCols + distanceRows
                data.ghosts[ghost-1][0] += 2
                if distance < bestDistance:
                    bestDistance = distance
                    bestDirection = "Left"
                data.ghosts[ghost-1][0] += 2
            if direction == "Right":
                data.ghosts[ghost-1][0] += 2
                distanceCols = math.fabs(data.pacmanLeftCol - \
                data.ghosts[ghost-1][0])
                distanceRows = math.fabs(data.pacmanTopRow - \
                data.ghosts[ghost-1][1])
                distance = distanceCols + distanceRows
                data.ghosts[ghost-1][0] -= 2
                if distance < bestDistance:
                    bestDistance = distance
                    bestDirection = "Right"
                data.ghosts[ghost-1][0] -= 2
            if direction == "Up":
                data.ghosts[ghost-1][1] -= 2
                distanceCols = math.fabs(data.pacmanLeftCol - \
                data.ghosts[ghost-1][0])
                distanceRows = math.fabs(data.pacmanTopRow - \
                data.ghosts[ghost-1][1])
                distance = distanceCols + distanceRows
                data.ghosts[ghost-1][1] += 2
                if distance < bestDistance:
                    if direction == "Left":
                        data.ghosts[num-1][0] -= 2
                    if direction == "Right":
                        data.ghosts[num-1][0] += 2
                    bestDistance = distance
                    bestDirection = "Up"
                data.ghosts[ghost-1][1] += 2
            if direction == "Down":
                data.ghosts[ghost-1][1] += 2
                distanceCols = math.fabs(data.pacmanLeftCol - \
                data.ghosts[ghost-1][0])
                distanceRows = math.fabs(data.pacmanTopRow - \
                data.ghosts[ghost-1][1])
                distance = distanceCols + distanceRows
                data.ghosts[ghost-1][1] -= 2
                if distance < bestDistance:
                    if direction == "Left":
                        data.ghosts[num-1][0] -= 2
                    if direction == "Right":
                        data.ghosts[num-1][0] += 2
                    bestDistance = distance
                    bestDirection = "Down"
                data.ghosts[ghost-1][1] -= 2
        return bestDirection
    if data.game2State:
        if ghost == 1:
            direction = data.ghost1Direction
        if ghost == 2:
            direction = data.ghost2Direction
        if ghost == 3:
            direction = data.ghost3Direction
        if ghost == 4:
            direction = data.ghost4Direction
        if ghost == 5:
            direction = data.ghost5Direction
        if ghost == 6:
            direction = data.ghost6Direction
        for direction in data.directions:
            if direction == "Left":
                data.ghosts2[ghost-1][0] -= 2
                distanceCols = math.fabs(data.pacmanLeftCol - \
                data.ghosts2[ghost-1][0])
                distanceRows = math.fabs(data.pacmanTopRow - \
                data.ghosts2[ghost-1][1])
                distance = distanceCols + distanceRows
                data.ghosts2[ghost-1][0] += 2
                if distance < bestDistance:
                    bestDistance = distance
                    bestDirection = "Left"
            if direction == "Right":
                data.ghosts2[ghost-1][0] += 2
                distanceCols = math.fabs(data.pacmanLeftCol - \
                data.ghosts2[ghost-1][0])
                distanceRows = math.fabs(data.pacmanTopRow - \
                data.ghosts2[ghost-1][1])
                distance = distanceCols + distanceRows
                data.ghosts2[ghost-1][0] -= 2
                if distance < bestDistance:
                    bestDistance = distance
                    bestDirection = "Right"
            if direction == "Up":
                data.ghosts2[ghost-1][1] -= 2
                distanceCols = math.fabs(data.pacmanLeftCol - \
                data.ghosts2[ghost-1][0])
                distanceRows = math.fabs(data.pacmanTopRow - \
                data.ghosts2[ghost-1][1])
                distance = distanceCols + distanceRows
                data.ghosts2[ghost-1][1] += 2
                if distance < bestDistance:
                    if direction == "Left":
                        data.ghosts2[num-1][0] -= 2
                    if direction == "Right":
                        data.ghosts2[num-1][0] += 2
                    bestDistance = distance
                    bestDirection = "Up"
            if direction == "Down":
                data.ghosts2[ghost-1][1] += 2
                distanceCols = math.fabs(data.pacmanLeftCol - \
                data.ghosts2[ghost-1][0])
                distanceRows = math.fabs(data.pacmanTopRow - \
                data.ghosts2[ghost-1][1])
                distance = distanceCols + distanceRows
                data.ghosts2[ghost-1][1] -= 2
                if distance < bestDistance:
                    if direction == "Left":
                        data.ghosts2[num-1][0] -= 2
                    if direction == "Right":
                        data.ghosts2[num-1][0] += 2
                    bestDistance = distance
                    bestDirection = "Down"
        return bestDirection
    
def ghostsCollide(data,num):
    if data.gameState:
        if num == 1:
            if data.ghosts[1][0] <= data.ghosts[0][0] <= data.ghosts[1][0]+3 \
            and data.ghosts[1][1] <= data.ghosts[0][1] <= data.ghosts[1][1]+3:
                return True
            if data.ghosts[2][0] <= data.ghosts[0][0] <= data.ghosts[2][0]+3 \
            and data.ghosts[2][1] <= data.ghosts[0][1] <= data.ghosts[2][1]+3:
                return True
        if num == 2:
            if data.ghosts[0][0] <= data.ghosts[1][0] <= data.ghosts[0][0]+3 \
            and data.ghosts[0][1] <= data.ghosts[1][1] <= data.ghosts[0][1]+3:
                return True
            if data.ghosts[2][0] <= data.ghosts[1][0] <= data.ghosts[2][0]+3 \
            and data.ghosts[2][1] <= data.ghosts[1][1] <= data.ghosts[2][1]+3:
                return True
        if num == 3:
            if data.ghosts[0][0] <= data.ghosts[2][0] <= data.ghosts[0][0]+3 \
            and data.ghosts[0][1] <= data.ghosts[2][1] <= data.ghosts[0][1]+3:
                return True
            if data.ghosts[1][0] <= data.ghosts[2][0] <= data.ghosts[1][0]+3 \
            and data.ghosts[1][1] <= data.ghosts[2][1] <= data.ghosts[1][1]+3:
                return True
    if data.game2State:
        if num == 1:
            if data.ghosts2[1][0] <= data.ghosts2[0][0] <= data.ghosts2[1][0]+3 \
            and data.ghosts2[1][1] <= data.ghosts2[0][1] <= data.ghosts2[1][1]+3:
                return True
            if data.ghosts2[2][0] <= data.ghosts2[0][0] <= data.ghosts2[2][0]+3 \
            and data.ghosts2[2][1] <= data.ghosts2[0][1] <= data.ghosts2[2][1]+3:
                return True
            if data.ghosts2[3][0] <= data.ghosts2[0][0] <= data.ghosts2[3][0]+3 \
            and data.ghosts2[3][1] <= data.ghosts2[0][1] <= data.ghosts2[3][1]+3:
                return True
            if data.ghosts2[4][0] <= data.ghosts2[0][0] <= data.ghosts2[4][0]+3 \
            and data.ghosts2[4][1] <= data.ghosts2[0][1] <= data.ghosts2[4][1]+3:
                return True
            if data.ghosts2[5][0] <= data.ghosts2[0][0] <= data.ghosts2[5][0]+3 \
            and data.ghosts2[5][1] <= data.ghosts2[0][1] <= data.ghosts2[5][1]+3:
                return True
        if num == 2:
            if data.ghosts2[0][0] <= data.ghosts2[1][0] <= data.ghosts2[0][0]+3 \
            and data.ghosts2[0][1] <= data.ghosts2[1][1] <= data.ghosts2[0][1]+3:
                return True
            if data.ghosts2[2][0] <= data.ghosts2[1][0] <= data.ghosts2[2][0]+3 \
            and data.ghosts2[2][1] <= data.ghosts2[1][1] <= data.ghosts2[2][1]+3:
                return True
            if data.ghosts2[3][0] <= data.ghosts2[1][0] <= data.ghosts2[3][0]+3 \
            and data.ghosts2[3][1] <= data.ghosts2[1][1] <= data.ghosts2[3][1]+3:
                return True
            if data.ghosts2[4][0] <= data.ghosts2[1][0] <= data.ghosts2[4][0]+3 \
            and data.ghosts2[4][1] <= data.ghosts2[1][1] <= data.ghosts2[4][1]+3:
                return True
            if data.ghosts2[5][0] <= data.ghosts2[1][0] <= data.ghosts2[5][0]+3 \
            and data.ghosts2[5][1] <= data.ghosts2[1][1] <= data.ghosts2[5][1]+3:
                return True
        if num == 3:
            if data.ghosts2[1][0] <= data.ghosts2[2][0] <= data.ghosts2[1][0]+3 \
            and data.ghosts2[1][1] <= data.ghosts2[2][1] <= data.ghosts2[1][1]+3:
                return True
            if data.ghosts2[0][0] <= data.ghosts2[2][0] <= data.ghosts2[0][0]+3 \
            and data.ghosts2[0][1] <= data.ghosts2[2][1] <= data.ghosts2[0][1]+3:
                return True
            if data.ghosts2[3][0] <= data.ghosts2[2][0] <= data.ghosts2[3][0]+3 \
            and data.ghosts2[3][1] <= data.ghosts2[2][1] <= data.ghosts2[3][1]+3:
                return True
            if data.ghosts2[4][0] <= data.ghosts2[2][0] <= data.ghosts2[4][0]+3 \
            and data.ghosts2[4][1] <= data.ghosts2[2][1] <= data.ghosts2[4][1]+3:
                return True
            if data.ghosts2[5][0] <= data.ghosts2[2][0] <= data.ghosts2[5][0]+3 \
            and data.ghosts2[5][1] <= data.ghosts2[2][1] <= data.ghosts2[5][1]+3:
                return True
        if num == 4:
            if data.ghosts2[1][0] <= data.ghosts2[3][0] <= data.ghosts2[1][0]+3 \
            and data.ghosts2[1][1] <= data.ghosts2[3][1] <= data.ghosts2[1][1]+3:
                return True
            if data.ghosts2[2][0] <= data.ghosts2[3][0] <= data.ghosts2[2][0]+3 \
            and data.ghosts2[2][1] <= data.ghosts2[3][1] <= data.ghosts2[2][1]+3:
                return True
            if data.ghosts2[0][0] <= data.ghosts2[3][0] <= data.ghosts2[0][0]+3 \
            and data.ghosts2[0][1] <= data.ghosts2[3][1] <= data.ghosts2[0][1]+3:
                return True
            if data.ghosts2[4][0] <= data.ghosts2[3][0] <= data.ghosts2[4][0]+3 \
            and data.ghosts2[4][1] <= data.ghosts2[3][1] <= data.ghosts2[4][1]+3:
                return True
            if data.ghosts2[5][0] <= data.ghosts2[3][0] <= data.ghosts2[5][0]+3 \
            and data.ghosts2[5][1] <= data.ghosts2[3][1] <= data.ghosts2[5][1]+3:
                return True
        if num == 5:
            if data.ghosts2[1][0] <= data.ghosts2[4][0] <= data.ghosts2[1][0]+3 \
            and data.ghosts2[1][1] <= data.ghosts2[4][1] <= data.ghosts2[1][1]+3:
                return True
            if data.ghosts2[2][0] <= data.ghosts2[4][0] <= data.ghosts2[2][0]+3 \
            and data.ghosts2[2][1] <= data.ghosts2[4][1] <= data.ghosts2[2][1]+3:
                return True
            if data.ghosts2[3][0] <= data.ghosts2[4][0] <= data.ghosts2[3][0]+3 \
            and data.ghosts2[3][1] <= data.ghosts2[4][1] <= data.ghosts2[3][1]+3:
                return True
            if data.ghosts2[0][0] <= data.ghosts2[4][0] <= data.ghosts2[0][0]+3 \
            and data.ghosts2[0][1] <= data.ghosts2[4][1] <= data.ghosts2[0][1]+3:
                return True
            if data.ghosts2[5][0] <= data.ghosts2[4][0] <= data.ghosts2[5][0]+3 \
            and data.ghosts2[5][1] <= data.ghosts2[4][1] <= data.ghosts2[5][1]+3:
                return True
        if num == 6:
            if data.ghosts2[1][0] <= data.ghosts2[5][0] <= data.ghosts2[1][0]+3 \
            and data.ghosts2[1][1] <= data.ghosts2[5][1] <= data.ghosts2[1][1]+3:
                return True
            if data.ghosts2[2][0] <= data.ghosts2[5][0] <= data.ghosts2[2][0]+3 \
            and data.ghosts2[2][1] <= data.ghosts2[5][1] <= data.ghosts2[2][1]+3:
                return True
            if data.ghosts2[3][0] <= data.ghosts2[5][0] <= data.ghosts2[3][0]+3 \
            and data.ghosts2[3][1] <= data.ghosts2[5][1] <= data.ghosts2[3][1]+3:
                return True
            if data.ghosts2[4][0] <= data.ghosts2[5][0] <= data.ghosts2[4][0]+3 \
            and data.ghosts2[4][1] <= data.ghosts2[5][1] <= data.ghosts2[4][1]+3:
                return True
            if data.ghosts2[0][0] <= data.ghosts2[5][0] <= data.ghosts2[0][0]+3 \
            and data.ghosts2[0][1] <= data.ghosts2[5][1] <= data.ghosts2[0][1]+3:
                return True
            
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Toplevel()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)

#################################################
# Term Project Main
################################################

def testAll():
    pass

def main():
    testAll()

if __name__ == '__main__':
    main()