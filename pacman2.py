# Term Project 3
# Melina Driscoll, msdrisco

import random
from tkinter import *

def init(data):
    data.startState = False
    data.instructionState = False
    data.gameState = True
    data.loseState = False
    data.winState = False
    data.margin = 10
    data.cellColors = drawBoard(data)
    data.cellCount = 0
    data.startCircles = [[data.width//2-20,data.height//6,data.width//2+20,
    data.height//6+40],[data.width//2-20,data.height-data.height//5,
    data.width//2+20,data.height-data.height//5+40]]
    data.direction1 = 5
    data.direction2 = -5
    data.startCircle = [data.width//2-30,data.height//2-30,data.width//2+30,
    data.height//2+30]
    data.startGhost = [data.startCircle[0]-80,data.startCircle[1],
    data.startCircle[2]-80,data.startCircle[3]]
    data.startLost = False
    data.timerDelay = 100
    data.coins = drawCoins(data)
    data.count = 0
    data.score = 0
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
    data.ghosts = [[26,30,"tomato"],[30,30,"deepskyblue"],[34,30,"magenta"]]
    data.directions = ["Right", "Left", "Up", "Down"]
    data.ghost1Direction = None
    data.ghost2Direction = None
    data.ghost3Direction = None
    data.switchRoles = False
    data.redCount = 0
    
def mousePressed(event, data):
    x = event.x
    y = event.y
    if data.instructionState:
        if 220 <= x <= 380:
            if 450 <= y <= 500:
                data.instructionState = False
                data.gameState = True
    if data.gameState:
        print(x,y)

def keyPressed(event, data):
    if data.startState:
        if event.keysym == "b":
            data.startState = False
            data.instructionState = True
    if data.gameState:
        #changes the direction of pac man based on the key the user presses
        if event.keysym == "Right":
            data.pacmanDirection = "Right"
            if validToMove(data):
                movePacman(data)
            if getCoins(data) == "regular":
                data.score += 1
            if getCoins(data) == "special":
                data.score += 5
                data.switchRoles = True
                print("right true")
                data.ghosts[0][2] = "red"
                data.ghosts[1][2] = "red"
                data.ghosts[2][2] = "red"
        if event.keysym == "Left":
            data.pacmanDirection = "Left"
            if validToMove(data):
                movePacman(data)
            if getCoins(data) == "regular":
                data.score += 1
            print(getCoins(data))
            if getCoins(data) == "special":
                data.score += 5
                data.switchRoles = True
                print("left true")
                data.ghosts[0][2] = "red"
                data.ghosts[1][2] = "red"
                data.ghosts[2][2] = "red"
        if event.keysym == "Up":
            data.pacmanDirection = "Up"
            if validToMove(data):
                movePacman(data)
            print(getCoins(data))
            if getCoins(data) == "regular":
                data.score += 1
            if getCoins(data) == "special":
                data.score += 5
                data.switchRoles = True
                print("up true")
                data.ghosts[0][2] = "red"
                data.ghosts[1][2] = "red"
                data.ghosts[2][2] = "red"
        if event.keysym == "Down":
            data.pacmanDirection = "Down"
            if validToMove(data):
                movePacman(data)
            if getCoins(data) == "regular":
                data.score += 1
            if getCoins(data) == "special":
                data.score += 5
                data.switchRoles = True
                print("down true")
                data.ghosts[0][2] = "red"
                data.ghosts[1][2] = "red"
                data.ghosts[2][2] = "red"
    if data.loseState or data.winState:
        if event.keysym == "p":
            init(data)
    
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
    if data.gameState:
        data.count += 1
        if len(data.coins) == 0:
            data.gameState = False
            data.winState = True
        #moves ghost one
        if data.count == 5:
            data.ghosts[0][1] = 26
        data.ghost1Direction = "Right"
        if (data.count >= 5):
            if validGhostMove(data,1):
                moveGhost(data,1)
            else:
                randomIndex = random.randint(0,len(data.directions)-1)
                data.ghost1Direction = data.directions[randomIndex]
                if validGhostMove(data,1):
                    moveGhost(data,1)
        #moves ghost two
        if data.count == 15:
            data.ghosts[1][1] = 26
        data.ghost2Direction = "Left"
        if (data.count >= 15):
            if validGhostMove(data,2):
                moveGhost(data,2)
            else:
                randomIndex = random.randint(0,len(data.directions)-1)
                data.ghost2Direction = data.directions[randomIndex]
                if validGhostMove(data,2):
                    moveGhost(data,2)
        #moves ghost three
        if data.count == 30:
            data.ghosts[2][1] = 26
        data.ghost3Direction = "Right"
        if (data.count >= 30):
            if validGhostMove(data,3):
                moveGhost(data,3)
            else:
                randomIndex = random.randint(0,len(data.directions)-1)
                data.ghost3Direction = data.directions[randomIndex]
                if validGhostMove(data,3):
                    moveGhost(data,3)
        if data.switchRoles:
            data.redCount += 1
            print(data.redCount)
            if data.redCount > 30 and data.redCount%2 == 0:
                data.ghosts[0][2] = "red"
                data.ghosts[1][2] = "red"
                data.ghosts[2][2] = "red"
            if data.redCount > 30 and data.redCount%2 != 0:
                data.ghosts[0][2] = "black"
                data.ghosts[1][2] = "black"
                data.ghosts[2][2] = "black"
        if data.redCount == 40:
            data.switchRoles = False
            data.ghosts[0][2] = "tomato"
            data.ghosts[1][2] = "deepskyblue"
            data.ghosts[2][2] = "magenta"
            data.redCount = 0
        checkCollisions(data)

def redrawAll(canvas, data):
    canvas.create_rectangle(data.margin,data.margin,data.width-data.margin,
    data.height-data.margin,fill="black")
    if data.startState:
        #draws title and instructions to begin
        canvas.create_text(data.width//2,data.height//3,
        text="Welcome to Pac-Man",fill="plum",font="Arial 50 bold")
        canvas.create_text(data.width//2,data.height//2+60,
        text="Press 'b' to begin",fill="deepskyblue",font="Arial 32 bold")
        for circle in data.startCircles:
            canvas.create_oval(circle[0],circle[1],circle[2],circle[3],
            fill="yellow")
    if data.instructionState:
        #draws instructions on how to place the game
        canvas.create_text(data.width//2,data.height//4,
        text="Use the arrow keys to move",font="Arial 28",fill="white")
        canvas.create_text(data.width//2,data.height//4+32,
        text="to collect the coins and avoid",font="Arial 28",fill="white")
        canvas.create_text(data.width//2,data.height//4+64,
        text="the ghosts.",font="Arial 28",fill="white")
        #draws example of pac man moving across the screen
        canvas.create_oval(data.startCircle[0],data.startCircle[1],
        data.startCircle[2],data.startCircle[3],fill="yellow")
        #draws ghost following pacman
        canvas.create_oval(data.startGhost[0],data.startGhost[1],
        data.startGhost[2],data.startGhost[3],fill="deepskyblue")
        if data.startLost:
            canvas.create_text(data.width//2,data.height//2+70,text="YOU LOST",
            font="Arial 34 bold", fill="plum")
        #draws the button to continue to the game
        canvas.create_rectangle(220,450,380,500,fill="white")
        canvas.create_text(data.width//2,475,text="Continue",font="Arial 28 bold",
        fill="black")
    if data.gameState:
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
        canvas.create_text(60,28,text=scoreText,fill="white",font="Arial 20")
        #draws pac man
        canvas.create_oval(data.pacmanLeftCol*10,data.pacmanTopRow*10,
        data.pacmanRightCol*10,data.pacmanBottomRow*10,fill="yellow")
        #draws ghosts
        for ghost in data.ghosts:
            canvas.create_oval(ghost[0]*10,ghost[1]*10,ghost[0]*10+30,
            ghost[1]*10+30,fill=ghost[2])
    if data.loseState:
        scoreText = "Score: %d" % (data.score)
        canvas.create_text(data.width//2,data.height//3+35,text="YOU LOST",
        font="Arial 40 bold",fill="plum")
        canvas.create_text(data.width//2,data.height//3+85,
        text=scoreText,font="Arial 30",fill="yellow")
        canvas.create_text(data.width//2,data.height//3+135,
        text="Press 'p' to play again",font="Arial 22",fill="plum")
    if data.winState:
        scoreText = "Score: %d" % (data.score)
        canvas.create_text(data.width//2,data.height//3+35,text="YOU WON",
        font="Arial 40 bold",fill="plum")
        canvas.create_text(data.width//2,data.height//3+85,
        text=scoreText,font="Arial 30",fill="yellow")
        canvas.create_text(data.width//2,data.height//3+135,
        text="Press 'p' to play again",font="Arial 22",fill="plum")
            
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
        
def drawBoard(data):
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
                result[y].append("blue")
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
          
def validToMove(data):
    #avoids pacman from running into any walls
    if data.pacmanDirection == "Right":
        data.pacmanRightCol += 2
        data.pacmanLeftCol += 2
        if 31 <= data.pacmanTopRow <= 34 and data.pacmanRightCol > 59:
            data.pacmanLeftCol = 2
            data.pacmanRightCol = 5
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
        if 31 <= data.pacmanTopRow <= 34 and data.pacmanLeftCol < 0:
            data.pacmanLeftCol = 55
            data.pacmanRightCol = 58
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
    #rightCol = data.ghosts[num-1][0]+3
    #leftCol = data.ghosts[num-1][0]
    #topRow = data.ghosts[num-1][1]
    #bottomRow = data.ghosts[num-1][1]+3
    #avoids the ghost from running into any walls
    if direction == "Right":
        data.ghosts[num-1][0] += 1
        if 31 <= data.ghosts[num-1][1] <= 34 and data.ghosts[num-1][0]+3 > 59:
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
        if data.pacmanLeftCol <= coin[0]//10 <= data.pacmanRightCol or \
        data.pacmanLeftCol <= (coin[0]+10)//10 <= data.pacmanRightCol:
            if data.pacmanTopRow <= coin[1]//10 <= data.pacmanBottomRow or \
            data.pacmanTopRow <= (coin[1]+10)//10 <= data.pacmanBottomRow:
                data.coins.remove(coin)
                if coin[4] == "red":
                    print("special")
                    return "special"
                else:
                    return "regular"
    return False
    
def checkCollisions(data):
    if data.switchRoles == False:
        for ghost in data.ghosts:
            if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
            ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
            (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
            ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                data.gameState = False
                data.loseState = True
    else:
        count = -1
        for ghost in data.ghosts:
            count += 1
            if count == 0:
                row = 26
                col = 30
                color = "tomato"
                if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                    data.score += 10
                    #data.ghosts[count][2] = color
                    data.ghosts[count][0] = row
                    data.ghosts[count][1] = col
            if count == 1:
                row = 30
                col = 30
                color = "deepskyblue"
                if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                    data.score += 10
                    #data.ghosts[count][2] = color
                    data.ghosts[count][0] = row
                    data.ghosts[count][1] = col
            if count == 2:
                row = 34
                col = 30
                color = "magenta"
                if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
                ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
                (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
                ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
                    data.score += 10
                    #data.ghosts[count][2] = color
                    data.ghosts[count][0] = row
                    data.ghosts[count][1] = col
            
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
    data.timerDelay = 500 # milliseconds
    root = Tk()
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
# Colab6 Main
################################################

def testAll():
    pass

def main():
    testAll()

if __name__ == '__main__':
    main()