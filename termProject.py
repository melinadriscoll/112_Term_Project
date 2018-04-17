#################################################
# Term Project
#Melina Driscoll, msdrisco
#################################################

import random

from tkinter import *

def init(data):
    data.margin = 10
    data.movingBlocks = []
    data.stoppedBlocks = []
    data.count = 0
    data.timerDelay = 500
    data.startState = True
    data.gameState = False
    data.winState = False
    data.loseState = False
    data.randomBlocks = []
    data.starterSquareWidth = (2/3)*data.width
    data.starterSquareHeight = (1/4)*data.height
    data.starterx1 = data.width//2 - data.starterSquareWidth//2
    data.starterx2 = data.width//2 + data.starterSquareWidth//2
    data.startery1 = data.height//2 - data.starterSquareHeight//2
    data.startery2 = data.height//2 + data.starterSquareHeight//2
    data.currBlock = None
    data.score = 0
 
#randomly generates new blocks of different sizes at the top of the board
def createBlock(data):
    blockSizes = [40,50,75,90]
    index = random.randint(0,len(blockSizes)-1)
    size = blockSizes[index]
    randomXCoor = random.randint(data.margin, data.width-data.margin-size)
    data.xCoor1 = randomXCoor
    data.xCoor2 = randomXCoor + size
    data.yCoor1 = data.margin
    data.yCoor2 = data.margin + size
    #checks if the new block will overlap with any of the existing blocks on
    #the board
    valid = validNewBlock(data,[data.xCoor1,data.yCoor1,
        data.xCoor2,data.yCoor2])
    if valid:
        #if the new block will not overlap any other blocks, add it to list of
        #existing blocks
        data.movingBlocks.append([data.xCoor1,data.yCoor1,data.xCoor2,
        data.yCoor2,"peachpuff"])

def validNewBlock(data,blockCoors):
    for block in data.movingBlocks:
        if blockCoors[1] <= block[1] <= blockCoors[3]:
            return False
    return True

#generates random blocks on the start screen    
def randomBlocks(data):
    xCoors = random.randint(data.margin,data.width-data.margin)
    yCoors = random.randint(data.margin,data.height-data.margin)
    size = (1/10)*data.width
    x1 = xCoors
    x2 = xCoors + size
    y1 = yCoors
    y2 = yCoors + size
    #ensures the random blocks will not overlap with the centered white square
    if data.starterx1 < x1 < data.starterx2 and \
    data.startery1 < y1 < data.startery2:
        pass
    elif data.starterx1 < x2 < data.starterx2 and \
    data.startery1 < y1 < data.startery2:
        pass
    elif data.starterx1 < x1 < data.starterx2 and \
    data.startery1 < y2 < data.startery2:
        pass
    elif data.starterx1 < x2 < data.starterx2 and \
    data.startery1 < y2 < data.startery2:
        pass  
    elif (x2 > data.width - data.margin) or \
    (y2 > data.height - data.margin):
        pass
    else:
        data.randomBlocks.append([x1,y1,x2,y2])

def mousePressed(event, data):
    if data.gameState:
        x = event.x
        y = event.y
        for block in data.movingBlocks:
            #if user clicks on a block
            if block[0] <= x <= block[2] and block[1] <= y <= block[3]:
                #if there is no other block already clicked, the block clicked
                #becomes selected
                if data.currBlock == None:
                    block[4] = "steelblue"
                    data.currBlock = block
                else:
                    #user can unclick a block
                    if data.currBlock == block:
                        block[4] = "peachpuff"
                        data.currBlock = None
                    else:
                        pass

def keyPressed(event, data):
    if data.startState:
        #user presses 'b' to begin the game
        if event.keysym == "b":
            data.startState = False
            data.gameState = True
            data.count = 0
    if data.gameState:
        #if the user has selected a block
        if data.currBlock != None:
            blockSize = data.currBlock[2] - data.currBlock[0]
            positionShift = 10
            #if the user presses the down arrow key, clicked block moves down
            if event.keysym == "Down":
                #moves block down, but ensures it does not leave the screen
                moveBlock(data,data.currBlock, positionShift)
            #if the user presses the left arrow key, clicked block moves left
            elif event.keysym == "Left":
                #makes sure block doesn't leave off the left of the screen
                if data.currBlock[0] - positionShift < data.margin:
                    data.currBlock[0] = data.margin
                    data.currBlock[2] = data.margin + blockSize
                elif isValidMove(data, data.currBlock):
                    data.currBlock[0] -= positionShift
                    data.currBlock[2] -= positionShift
            #if the user presses the right arrow key, clicked block moves right
            elif event.keysym == "Right":
                #makes sure block doesn't leave off the right of the screen
                if data.currBlock[2] + positionShift > data.width-data.margin:
                    data.currBlock[2] = data.width - data.margin
                    data.currBlock[0] = data.width - data.margin - blockSize
                elif isValidMove(data, data.currBlock):
                    data.currBlock[0] += positionShift
                    data.currBlock[2] += positionShift
    if data.winState or data.loseState:
        if event.keysym == "p":
            init()
    
def timerFired(data):
    if data.startState:
        #generates random blocks around the screen
        if data.count%2 == 0:
            randomBlocks(data)
        data.count += 1
    if data.gameState:
        #creates a new block at the top of the screen every 10 seconds
        if data.count%10 == 0:
            createBlock(data)
        #every second each moving block moves down on the screen
        if data.count > 0:
            for block in data.movingBlocks:
                moveBlock(data, block)
        data.count += 1
        
def moveBlock(data, block, positionShift = 10):
    blockSize = block[2] - block[0]
    block[1] += positionShift
    block[3] += positionShift
    #if the block has reached the bottom of the screen
    if block[3] >= data.height - data.margin:
        block[3] = data.height - data.margin
        block[1] = data.height - data.margin - blockSize
        #reset the clicked block to none if it reaches the bottom
        if data.currBlock == block:
            data.currBlock = None
        data.stoppedBlocks.append(block)
        data.score += 1
        data.movingBlocks.remove(block)
    else:
        #checks if the moving block has collided with a stopped block
        for stoppedBlock in data.stoppedBlocks:
            if block[3] == stoppedBlock[1]:
                if stoppedBlock[0] < block[0] < stoppedBlock[2] or \
                stoppedBlock[0] < block[2] < stoppedBlock[2]:
                    #sets block to be stopped above the other stopped block
                    block[1] = stoppedBlock[1] - blockSize
                    block[3] = stoppedBlock[1]
                    #reset the clicked block to none if it reaches a stopped
                    #block
                    if data.currBlock == block:
                        data.currBlock = None
                    data.stoppedBlocks.append(block)
                    data.score += 1
                    data.movingBlocks.remove(block)
                    continue
            elif block[3] > stoppedBlock[1]:
                if stoppedBlock[0] < block[0] < stoppedBlock[2] or \
                stoppedBlock[0] < block[2] < stoppedBlock[2]:
                    #sets block to be stopped above the other stopped block
                    block[1] = stoppedBlock[1] - blockSize
                    block[3] = stoppedBlock[1]
                    #reset the clicked block to none if it reaches a stopped
                    #block
                    if data.currBlock == block:
                        data.currBlock = None
                    data.stoppedBlocks.append(block)
                    data.score += 1
                    data.movingBlocks.remove(block)
            else:
                pass

#checks if the current block can move down the screen without colliding with 
# a stopped block
def isValidMove(data, block):
    for stopBlocks in data.stoppedBlocks:
        if stopBlocks[0] < block[0] < stopBlocks[2] or \
        stopBlocks[0] < block[2] < stopBlocks[2]:
            if stopBlocks[1] <= block[1] <= stopBlocks[3] or \
            stopBlocks[1] <= block[3] <= stopBlocks[3]:
                return False
    return True
    
def redrawAll(canvas, data):
    #draws background
    canvas.create_rectangle(data.margin, data.margin, data.width-data.margin,
    data.height - data.margin, fill="lightcyan")
    if data.startState:
        #draws centered white square and text with instructions
        canvas.create_rectangle(data.starterx1,data.startery1,data.starterx2,
        data.startery2,fill="white",outline="black")
        canvas.create_text(data.width//2,data.height//2,
        text="Press 'b' to begin",font="Arial 30 bold")
        #draws each randomly generated block
        for block in data.randomBlocks:
            canvas.create_rectangle(block[0],block[1],block[2],block[3],
            fill="peachpuff")
    if data.gameState:
        #draws each moving block
        for block in data.movingBlocks:
            canvas.create_rectangle(block[0],block[1],block[2],block[3],
            fill=block[4])
        #draws each stopped block
        for block in data.stoppedBlocks:
            canvas.create_rectangle(block[0],block[1],block[2],block[3],
            fill="cornsilk")
            if block[1] <= data.margin:
                data.gameState = False
                data.winState = True
        textSize = 22
        scoreText = "Score: %d" % (data.score)
        canvas.create_text(data.margin+textSize*2, data.margin+textSize,
        text=scoreText,font="Arial 18 bold", fill="indianred")
    if data.winState:
        canvas.create_text(data.width//2,data.height//2,text="YOU WIN!",
        font="Arial 30 bold", fill="red")
        winTextSize = 30
        scoreText = "Score: %s" % (data.score)
        canvas.create_text(data.width//2, data.height//2+winTextSize,
        text=scoreText, font="Arial 22 bold", fill="red")
        scoreTextSize = 22
        canvas.create_text(data.width//2,
        data.height//2+winTextSize+scoreTextSize,
        text="Press 'p' to play again!", font="Arial 18 bold",fill="black")
    if data.loseState:
        canvas.create_text(data.width//2,data.height//2,text="You lost.",
        font="Arial 30 bold", fill="red")
        winTextSize = 30
        scoreText = "Score: %s" % (data.score)
        canvas.create_text(data.width//2, data.height//2+winTextSize,
        text=scoreText, font="Arial 22 bold", fill="red")
        scoreTextSize = 22
        canvas.create_text(data.width//2,
        data.height//2+winTextSize+scoreTextSize,
        text="Press 'p' to play again!", font="Arial 18 bold",fill="black")

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