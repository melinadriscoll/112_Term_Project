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
    data.score = -2
    data.numRows = data.height//20
    data.numCols = data.width//20
    data.pacmanTopRow = 41
    data.pacmanLeftCol = 30
    data.pacmanBottomRow = 44
    data.pacmanRightCol = 33
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
    
def mousePressed(event, data):
    x = event.x
    y = event.y
    if data.instructionState:
        if 220 <= x <= 380:
            if 450 <= y <= 500:
                data.instructionState = False
                data.gameState = True

def keyPressed(event, data):
    if data.startState:
        if event.keysym == "b":
            data.startState = False
            data.instructionState = True
    if data.gameState:
        #changes the direction of pac man based on the key the user presses
        if event.keysym == "Right":
            data.pacmanDirection = "Right"
        if event.keysym == "Left":
            data.pacmanDirection = "Left"
        if event.keysym == "Up":
            data.pacmanDirection = "Up"
        if event.keysym == "Down":
            data.pacmanDirection = "Down"
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
        if validToMove(data):
            movePacman(data)
            if getCoins(data):
                data.score += 1
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
        #top left barrier
        canvas.create_rectangle(110,110,200,158,fill="black",outline="blue")
        #top middle barrier
        canvas.create_rectangle(290,110,340,230,fill="black",outline="blue")
        canvas.create_rectangle(200,230,438,260,fill="black",outline="blue")
        #top right barrier
        canvas.create_rectangle(420,110,518,170,fill="black",outline="blue")
        #middle left barrier
        canvas.create_rectangle(180,410,290,460,fill="black",outline="blue")
        #middle right barrier
        canvas.create_rectangle(340,410,440,460,fill="black",outline="blue")
        #bottom left barrier
        canvas.create_rectangle(110,470,178,520,fill="black",outline="blue")
        canvas.create_rectangle(178,510,230,530,fill="black",outline="blue")
        #bottom right barrier
        canvas.create_rectangle(400,510,450,530,fill="black",outline="blue")
        canvas.create_rectangle(450,470,520,520,fill="black",outline="blue")
        #bottom middle barrier
        canvas.create_rectangle(280,510,350,530,fill="black",outline="blue")
        #draws where the ghosts stay
        canvas.create_rectangle(260,288,380,350,fill="black",outline="red")
        #draws coins
        for coin in data.coins:
            canvas.create_oval(coin[0],coin[1],coin[2],coin[3],fill="pink")
        #draws the score
        scoreText = "Score: %d" % (data.score)
        canvas.create_text(60,25,text=scoreText,fill="white",font="Arial 25")
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
            if (40 <= x <= 560 and 40 <= y*10 <= 50):
                result[y].append("blue")
            elif (100 <= x <= 180 and 100 <= y*10 <= 140):
                result[y].append("blue")
            elif (280 <= x <= 320 and 100 <= y*10 <= 220):
                result[y].append("blue")
            elif (190 <= x <= 420 and 220 <= y*10 <= 230):
                result[y].append("blue")
            elif (410 <= x <= 500 and 100 <= y*10 <= 150):
                result[y].append("blue")
            elif (250 <= x <= 360 and 290 <= y*10 <= 330):
                result[y].append("blue")
            elif (170 <= x <= 270 and 400 <= y*10 <= 440):
                result[y].append("blue")
            elif (330 <= x <= 420 and 400 <= y*10 <= 440):
                result[y].append("blue")
            elif (100 <= x <= 160 and 460 <= y*10 <= 500):
                result[y].append("blue")
            elif (170 <= x <= 210 and 500 <= y*10 <= 510):
                result[y].append("blue")
            elif (440 <= x <= 500 and 460 <= y*10 <= 500):
                result[y].append("blue")
            elif (390 <= x <= 430 and 500 <= y*10 <= 510):
                result[y].append("blue")
            elif (270 <= x <= 330 and 500 <= y*10 <= 510):
                result[y].append("blue")
            elif (550 <= x <= 560 and 40 <= y*10 <= 200):
                result[y].append("blue")
            elif (480 <= x <= 560 and 200 <= y*10 <= 210):
                result[y].append("blue")
            elif (470 <= x <= 480 and 200 <= y*10 <= 290):
                result[y].append("blue")
            elif (480 <= x <= 600 and 280 <= y*10 <= 290):
                result[y].append("blue")
            elif (480 <= x <= 600 and 350 <= y*10 <= 360):
                result[y].append("blue")
            elif (470 <= x <= 480 and 350 <= y*10 <= 410):
                result[y].append("blue")
            elif (480 <= x <= 560 and 400 <= y*10 <= 410):
                result[y].append("blue")
            elif (560 <= x <= 570 and 400 <= y*10 <= 570):
                result[y].append("blue")
            elif (40 <= x <= 560 and 560 <= y*10 <= 570):
                result[y].append("blue")
            elif (30 <= x <= 40 and 400 <= y*10 <= 570):
                result[y].append("blue")
            elif (40 <= x <= 120 and 400 <= y*10 <= 410):
                result[y].append("blue")
            elif (110 <= x <= 120 and 350 <= y*10 <= 410):
                result[y].append("blue")
            elif (0 <= x <= 120 and 350 <= y*10 <= 360):
                result[y].append("blue")
            elif (0 <= x <= 120 and 280 <= y*10 <= 290):
                result[y].append("blue")
            elif (110 <= x <= 120 and 200 <= y*10 <= 290):
                result[y].append("blue")
            elif (30 <= x <= 120 and 200 <= y*10 <= 210):
                result[y].append("blue")
            elif (30 <= x <= 40 and 40 <= y*10 <= 200):
                result[y].append("blue")
            else:
                result[y].append("black")
    return result
          
def validToMove(data):
    #avoids pacman from running into any walls
    if data.pacmanDirection == "Right":
        data.pacmanRightCol += 1
        data.pacmanLeftCol += 1
        if 31 <= data.pacmanTopRow <= 33 and data.pacmanRightCol > 59:
            data.pacmanLeftCol = 0
            data.pacmanRightCol = 3
        else:
            #if the cell to the right is black, is valid to move
            row = data.pacmanTopRow-1
            col = data.pacmanRightCol-1
            row2 = data.pacmanBottomRow-1
            if data.cellColors[row][col]=="black" and \
            data.cellColors[row2][col] == "black":
                return True
            else:
                data.pacmanRightCol -= 1
                data.pacmanLeftCol -= 1
                return False
    elif data.pacmanDirection == "Left":
        data.pacmanRightCol -= 1
        data.pacmanLeftCol -= 1
        if 31 <= data.pacmanTopRow <= 33 and data.pacmanLeftCol < 0:
            data.pacmanLeftCol = 56
            data.pacmanRightCol = 59
        else:
            #if the cell to the left is black, is valid to move
            row = data.pacmanTopRow-1
            col = data.pacmanLeftCol-1
            row2 = data.pacmanBottomRow-1
            if data.cellColors[row][col]=="black" and \
            data.cellColors[row2][col]=="black":
                return True
            else:
                data.pacmanRightCol += 1
                data.pacmanLeftCol += 1
                return False
    elif data.pacmanDirection == "Up":
        data.pacmanTopRow -= 1
        data.pacmanBottomRow -= 1
        #if the cell above is black, is valid to move
        row = data.pacmanTopRow-1
        col = data.pacmanLeftCol-1
        col2 = data.pacmanRightCol-1
        if data.cellColors[row][col]=="black" and \
        data.cellColors[row][col2] == "black":
            return True
        else:
            data.pacmanTopRow += 1
            data.pacmanBottomRow += 1
            return False
    elif data.pacmanDirection == "Down":
        data.pacmanTopRow += 1
        data.pacmanBottomRow += 1
        #if the cell below is black, is valid to move
        row = data.pacmanBottomRow-1
        col = data.pacmanLeftCol-1
        col2 = data.pacmanRightCol-1
        if data.cellColors[row][col]=="black" and \
        data.cellColors[row][col2]=="black":
            return True
        else:
            data.pacmanTopRow -= 1
            data.pacmanBottomRow -= 1
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
        if 31 <= data.ghosts[num-1][1] <= 33 and data.ghosts[num-1][0]+3 > 59:
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
        if 31 <= data.ghosts[num-1][1] <= 33 and data.ghosts[num-1][0] < 0:
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
                        results.append([x*10,y*10,x*10+10,y*10+10])
    return results
        
def getCoins(data):
    for coin in data.coins:
        if data.pacmanLeftCol <= coin[0]//10 <= data.pacmanRightCol:
            if data.pacmanTopRow <= coin[1]//10 <= data.pacmanBottomRow:
                data.coins.remove(coin)
                return True
    return False
    
def checkCollisions(data):
    for ghost in data.ghosts:
        if (ghost[0] <= data.pacmanLeftCol+1 <= ghost[0]+3 or \
        ghost[0] <= data.pacmanRightCol-1 <= ghost[0]+3) and \
        (ghost[1] <= data.pacmanTopRow+1 <= ghost[1]+3 or \
        ghost[1] <= data.pacmanBottomRow-1 <= ghost[1]+3):
            data.gameState = False
            data.loseState = True
            
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