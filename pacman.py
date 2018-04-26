# Term Project 3
# Melina Driscoll, msdrisco

import random
from tkinter import *

def init(data):
    data.startState = True
    data.instructionState = False
    data.gameState = False
    data.loseState = False
    data.winState = False
    data.margin = 10
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
    data.count = 0
    data.score = 0
    data.numRows = data.height//20
    data.numCols = data.width//20
    data.coins = drawCoins(data)
    data.pacman = [285,410,315,440]
    data.pacmanDirection = None
    data.ghosts = [[245,290,275,320,"red"],[285,290,315,320,"green"],
    [325,290,355,320,"orange"]]
    
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
            init()
    
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
        #print(validToMove(data))
        if validToMove(data):
            if data.count%4 == 0:
                movePacman(data)
                if getCoins(data):
                    data.score += 1
        data.count += 1

def redrawAll(canvas, data):
    canvas.create_rectangle(data.margin,data.margin,data.width-data.margin,
    data.height-data.margin,fill="black")
    if data.startState:
        #draws title and instructions to begin
        canvas.create_text(data.width//2,data.height//3,
        text="Welcome to Pac-Man",fill="plum",font="Arial 50 bold")
        canvas.create_text(data.width//2,data.height//2+60,
        text="Press 'b' to begin",fill="powderblue",font="Arial 32 bold")
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
        data.startGhost[2],data.startGhost[3],fill="red")
        if data.startLost:
            canvas.create_text(data.width//2,data.height//2+70,text="YOU LOST",
            font="Arial 34 bold", fill="plum")
        #draws the button to continue to the game
        canvas.create_rectangle(220,450,380,500,fill="white")
        canvas.create_text(data.width//2,475,text="Continue",font="Arial 28 bold",
        fill="black")
    if data.gameState:
        #draws the score
        scoreText = "Score: %d" % (data.score)
        canvas.create_text(50,25,text=scoreText,fill="white")
        #draws the outline of the board
        canvas.create_polygon(40,40,560,40,560,200,490,200,490,290,590,290,
        590,350,490,350,490,400,560,400,560,590,40,590,40,400,110,400,110,350,
        10,350,10,290,110,290,110,200,40,200,
        50,50,550,50,550,190,480,190,480,300,590,300,590,340,480,340,
        480,410,550,410,550,580,50,580,50,410,120,410,120,340,10,340,10,300,
        120,300,120,190,50,190,fill="black",outline="blue")
        canvas.create_rectangle(40,40,50,200,fill="black",outline="blue")
        #draws the coins
        drawCoins(data)
        for coin in data.coins:
            canvas.create_oval(coin[0],coin[1],coin[2],coin[3],fill="pink")
        #draws the inside barriers
        #top left barrier
        canvas.create_rectangle(95,100,160,155,fill="black",outline="blue")
        #top middle barrier
        canvas.create_polygon(270,100,330,100,330,200,415,200,415,235,
        185,235,185,200,270,200,fill="black",outline="blue")
        #top right barrier
        canvas.create_rectangle(505,100,440,155,fill="black",outline="blue")
        #middle left barrier
        canvas.create_rectangle(170,365,280,440,fill="black",outline="blue")
        #middle right barrier
        canvas.create_rectangle(430,365,320,440,fill="black",outline="blue")
        #bottom left barrier
        canvas.create_polygon(95,450,160,450,160,490,213,490,213,540,95,540,
        fill="black",outline="blue")
        #bottom middle barrier
        canvas.create_rectangle(265,490,335,540,fill="black",outline="blue")
        #bottom right barrier
        canvas.create_polygon(505,450,440,450,440,490,387,490,387,540,505,540,
        fill="black",outline="blue")
        #draws where the ghosts stay
        canvas.create_rectangle(240,280,360,330,fill="black",outline="blue")
        canvas.create_rectangle(280,270,320,280,fill="black",outline="blue")
        #draws pac man
        canvas.create_oval(data.pacman[0],data.pacman[1],data.pacman[2],
        data.pacman[3],fill="yellow")
        #draws ghosts
        for ghost in data.ghosts:
            canvas.create_oval(ghost[0],ghost[1],ghost[2],ghost[3],
            fill=ghost[4])
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
        
def drawCoins(data):
    #draws each coin on the board
    result = []
    for row in range(0,19):
        for col in range(0,15):
            coors = [row*25+70,col*35+70,row*25+80,col*35+80]
            if coors[0] < 130 and (190 < coors[1] < 410):
                pass
            elif coors[0] > 460 and (190 < coors[1] < 410):
                pass
            elif 285 <= coors[0] <= 315 and 410 <= coors[1] <= 440:
                pass
            else:
                result.append(coors)
    return result
          
def validToMove(data):
    x1 = data.pacman[0]
    y1 = data.pacman[1]
    x2 = data.pacman[2]
    y2 = data.pacman[3]
    #avoids pacman from running into any walls
    if data.pacmanDirection == "Right":
        if (95-15 < x1 < 160 and 100-15 < y1 < 155) or \
        (270-15 < x1 < 330 and 100-15 < y1 < 200) or \
        (180-15 < x1 < 415 and 200-15 < y1 < 235) or \
        (440-15 < x1 < 505 and 100-15 < y1 < 155) or \
        (x1 > 550-15 and 50 < y1 < 190-15) or \
        (x1 > 550-15 and 410 < y1 < 550-15) or \
        (240-15 < x1 < 360 and 280-15 < y1 < 330) or \
        (x1 > 480-15 and 190-15 < y1 < 300) or \
        (x1 > 480-15 and 340-15 < y1 < 410) or \
        (170-15 < x1 < 280 and 365-15 < y1 < 440) or \
        (320-15 < x1 < 430 and 365-15 < y1 < 440) or \
        (95-15 < x1 < 160 and 450-15 < y1 < 540) or \
        (160-15 < x1 < 213 and 490-15 < y1 < 540) or \
        (440-15 < x1 < 505 and 450-15 < y1 < 540) or \
        (387-15 < x1 < 440 and 490-15 < y1 < 540) or \
        (265-15 < x1 < 335 and 490-15 < y1 < 540):
            return False
    elif data.pacmanDirection == "Left":
        if (50 < y1 < 190-30) or (410 < y1 < 580-30):
            if x1-25 < 50:
                return False
        elif (190 < y1 < 300-30) or (340 < y1 < 410-30):
            if x1-25 < 120:
                return False
        else:
            return True
    elif data.pacmanDirection == "Up":
        if y1-35 <= 50:
            return False
        elif (10 <= x1 <= 120) or (480 <= x2 <= 590):
            if 190 <= y1-35 <= 410:
                return False
        else:
            return True
    elif data.pacmanDirection == "Down":
        if y2+35 >= 590:
            return False
        elif (10 < x1 < 120) or (480 < x2 < 590):
            if 190 <= y2+35 <= 410:
                return False
        else:
            return True
    else:
        return True
                
def movePacman(data):
    if data.pacmanDirection == "Right":
        data.pacman[0] += 25
        data.pacman[2] += 25
        if (50 < data.pacman[1] < 190-30) or (410 < data.pacman[1] < 580-30):
            if data.pacman[2] > 550:
                data.pacman[0] = 10
                data.pacman[2] = 40
        elif (190 < data.pacman[1] < 300-30) or (340 < data.pacman[1] < 410-30):
            if data.pacman[2] > 480:
                data.pacman[0] = 10
                data.pacman[2] = 40

    if data.pacmanDirection == "Left":
        data.pacman[0] -= 25
        data.pacman[2] -= 25
        if data.pacman[0] < 10:
            data.pacman[0] = 560
            data.pacman[2] = 590
    if data.pacmanDirection == "Up":
        data.pacman[1] -= 35
        data.pacman[3] -= 35
    if data.pacmanDirection == "Down":
        data.pacman[1] += 35
        data.pacman[3] += 35
        
def getCoins(data):
    for coin in data.coins:
        if data.pacman[0] <= coin[0] <= data.pacman[2]:
            if data.pacman[1] <= coin[1] <= data.pacman[3]:
                data.coins.remove(coin)
                return True
    return False
            
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