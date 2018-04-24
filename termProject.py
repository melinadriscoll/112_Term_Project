#################################################
# Term Project
#Melina Driscoll, msdrisco
#################################################

import random

from tkinter import *

def init(data):
    data.margin = 10
    data.movingBlocks = []
    data.bottomBlocks = []
    data.stoppedBlocks = []
    data.count = 0
    data.timerDelay = 300
    data.startState = True
    data.startBlockState = False
    data.instructionBlockState = False
    data.gameBlockState = False
    data.winBlockState = False
    data.loseBlockState = False
    data.randomBlocks = []
    data.starterSquareWidth = (2/3)*data.width
    data.starterSquareHeight = (1/4)*data.height
    data.starterx1 = data.width//2 - data.starterSquareWidth//2
    data.starterx2 = data.width//2 + data.starterSquareWidth//2
    data.startery1 = data.height//2 - data.starterSquareHeight//2
    data.startery2 = data.height//2 + data.starterSquareHeight//2
    data.currBlock = None
    data.nowBlock = None
    data.score = 0
    data.startHangmanState = False
    data.gameHangmanState = False
    data.cities = ["Chicago","Boston","Austin","Miami","Denver","Seattle"]
    data.food = ["Goldfish","Cookie","Carrot","Apple","Pizza","Cheese"]
    data.pets = ["Dog","Cat","Goldfish","Parrot","Pig","Goat"]
    data.category = None
 
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
    x = event.x
    y = event.y
    if data.startState:
        #if user clicks on the Balancing Blocks, begin that game
        if data.margin+20 <= x <= data.margin+data.width//2-30:
            if data.height//2 <= y <= data.height//2+100:
                data.startState = False
                data.startBlockState = True
        #if user clicks on the Hangman, begin that game
        elif data.width-data.margin-data.width//2+30 <= x <= \
        data.width-data.margin-20:
            if data.height//2 <= y <= data.height//2+100:
                data.startState = False
                data.startHangmanState = True
    if data.instructionBlockState:
        #if the user clicks on the "Continue" button, continue to the game
        if (data.width//2 - data.buttonWidth//2 <= x <= \
        data.width//2 + data.buttonWidth//2):
            if (data.height-data.spaceAbove-data.buttonHeight <= y <= \
            data.height-data.spaceAbove):
                data.instructionBlockState = False
                data.gameBlockState = True
                data.count = 0
    if data.gameBlockState:
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
    if data.startHangmanState:
        if data.width//2-60 <= x <= data.width//2+60:
            if data.height//4-20 <= y <= data.height//4+20:
                data.category = data.cities
                data.startHangmanState = False
                data.gameHangmanState = True
            elif data.height//2-20 <= y <= data.height//2+20:
                data.category = data.food
                data.startHangmanState = False
                data.gameHangmanState = True
            elif data.height-data.height//4-20 <= y <= \
            data.height-data.height//4+20:
                data.category = data.pets
                data.startHangmanState = False
                data.gameHangmanState = True

def keyPressed(event, data):
    if data.startBlockState:
        #user presses 'b' to begin the game
        if event.keysym == "b":
            data.startBlockState = False
            data.instructionBlockState = True
            data.count = 0
    if data.gameBlockState:
        #if the user has selected a block
        if data.currBlock != None:
            blockSize = data.currBlock[2] - data.currBlock[0]
            data.positionShift = 10
            #if the user presses the down arrow key, clicked block moves down
            if event.keysym == "Down":
                #moves block down, but ensures it does not leave the screen
                moveBlock(data,data.currBlock, data.positionShift)
            #if the user presses the left arrow key, clicked block moves left
            elif event.keysym == "Left":
                data.currBlock[0] -= data.positionShift
                data.currBlock[2] -= data.positionShift
                #makes sure block doesn't leave off the left of the screen
                if data.currBlock[0] < data.margin:
                    data.currBlock[0] = data.margin
                    data.currBlock[2] = data.margin + blockSize
                elif not(isValidMove(data, data.currBlock)):
                    data.currBlock[0] += data.positionShift
                    data.currBlock[2] += data.positionShift
            #if the user presses the right arrow key, clicked block moves right
            elif event.keysym == "Right":
                data.currBlock[0] += data.positionShift
                data.currBlock[2] += data.positionShift
                #makes sure block doesn't leave off the right of the screen
                if data.currBlock[2] > data.width-data.margin:
                    data.currBlock[2] = data.width - data.margin
                    data.currBlock[0] = data.width - data.margin - blockSize
                elif not(isValidMove(data, data.currBlock)):
                    data.currBlock[0] -= data.positionShift
                    data.currBlock[2] -= data.positionShift
    if data.winBlockState or data.loseBlockState:
        if event.keysym == "p":
            init(data)
    
def timerFired(data):
    if data.startBlockState:
        #generates random blocks around the screen
        if data.count%2 == 0:
            randomBlocks(data)
        data.count += 1
    if data.gameBlockState:
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
        elif data.nowBlock == block:
            data.gameBlockState = False
            data.loseBlockState = True
        data.bottomBlocks.append(block)
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
                    data.nowBlock = block
                    if data.currBlock == block:
                        data.currBlock = None
                    if isBalanced(data, data.nowBlock, stoppedBlock):
                        block.append("lightsalmon")
                        data.stoppedBlocks.append(block)
                        data.score += 1
                        data.movingBlocks.remove(block)
                        continue
                    else:
                        data.nowBlock[4] = "red"
                        moveTippedBlock(data)
            elif block[3] > stoppedBlock[1]:
                if stoppedBlock[0] < block[0] < stoppedBlock[2] or \
                stoppedBlock[0] < block[2] < stoppedBlock[2]:
                    #sets block to be stopped above the other stopped block
                    block[1] = stoppedBlock[1] - blockSize
                    block[3] = stoppedBlock[1]
                    #reset the clicked block to none if it reaches a stopped
                    #block
                    data.nowBlock = block
                    if data.currBlock == block:
                        data.currBlock = None
                    if isBalanced(data, data.nowBlock, stoppedBlock):
                        block.append("lightsalmon")
                        data.stoppedBlocks.append(block)
                        data.score += 1
                        data.movingBlocks.remove(block)
                    else:
                        data.nowBlock[4] = "red"
                        moveTippedBlock(data)
            else:
                pass
        #checks if the moving block has collided with a bottom block
        for bottomBlock in data.bottomBlocks:
            if block[3] == bottomBlock[1]:
                if bottomBlock[0] < block[0] < bottomBlock[2] or \
                bottomBlock[0] < block[2] < bottomBlock[2]:
                    #sets block to be stopped above the bottom block
                    block[1] = bottomBlock[1] - blockSize
                    block[3] = bottomBlock[1]
                    #reset the clicked block to none if it reaches a bottom
                    #block
                    data.nowBlock = block
                    if data.currBlock == block:
                        data.currBlock = None
                    if isBalanced(data, data.nowBlock, bottomBlock):
                        block.append("lightsalmon")
                        data.stoppedBlocks.append(block)
                        data.score += 1
                        data.movingBlocks.remove(block)
                        continue
                    else:
                        data.nowBlock[4] = "red"
                        moveTippedBlock(data)
            elif block[3] > bottomBlock[1]:
                if bottomBlock[0] < block[0] < bottomBlock[2] or \
                bottomBlock[0] < block[2] < bottomBlock[2]:
                    #sets block to be stopped above the bottom block
                    block[1] = bottomBlock[1] - blockSize
                    block[3] = bottomBlock[1]
                    #reset the clicked block to none if it reaches a bottom
                    #block
                    data.nowBlock = block
                    if data.currBlock == block:
                        data.currBlock = None
                    if isBalanced(data, data.nowBlock, bottomBlock):
                        block.append("lightsalmon")
                        data.stoppedBlocks.append(block)
                        data.score += 1
                        data.movingBlocks.remove(block)
                        continue
                    else:
                        data.nowBlock[4] = "red"
                        moveTippedBlock(data)
            else:
                pass
                
def moveTippedBlock(data):
    if data.nowBlock[5] == "right":
        data.nowBlock[0] += data.positionShift
        data.nowBlock[2] += data.positionShift
        data.nowBlock[1] += data.positionShift
        data.nowBlock[3] += data.positionShift
        if data.nowBlock[3] >= data.height - data.margin:
            data.gameBlockState = False
            data.loseBlockState = True
    elif data.nowBlock[5] == "left":
        data.nowBlock[0] -= data.positionShift
        data.nowBlock[2] -= data.positionShift
        data.nowBlock[1] += data.positionShift
        data.nowBlock[3] += data.positionShift
        if data.nowBlock[3] >= data.height - data.margin:
            data.gameBlockState = False
            data.loseBlockState = True

#checks if the current block can move down the screen without colliding with 
# a stopped block
def isValidMove(data, block):
    for stopBlocks in data.stoppedBlocks:
        if stopBlocks[0] <= block[0] <= stopBlocks[2] or \
        stopBlocks[0] <= block[2] <= stopBlocks[2]:
            if stopBlocks[1] <= block[1] <= stopBlocks[3] or \
            stopBlocks[1] <= block[3] <= stopBlocks[3]:
                return False
    return True
 
#checks if the new block that was just placed will balance on the block below
#or if it will tip off of the block  
def isBalanced(data, fallingBlock, placedBlock):
    fallingBlockSize = fallingBlock[2] - fallingBlock[0]
    fallingBlockCenter = fallingBlock[0] + fallingBlockSize
    placedBlockSize = placedBlock[2] - placedBlock[0]
    placedBlockCenter = placedBlock[0] + placedBlockSize
    #checks if the centers of the two blocks are further away from each other
    #than half of the size of the block on top
    if fallingBlockCenter - placedBlockCenter > fallingBlockSize//2:
        data.nowBlock.append("right")
        return False
    elif placedBlockCenter - fallingBlockCenter > fallingBlockSize//2:
        data.nowBlock.append("left")
        return False
    else:
        return True
    
def redrawAll(canvas, data):
    #draws background
    canvas.create_rectangle(data.margin, data.margin, data.width-data.margin,
    data.height - data.margin, fill="lightcyan")
    if data.startState:
        canvas.create_text(data.width//2,data.height//4,
        text="Welcome to Mini Games", font="Arial 50 bold",fill="lightsalmon")
        canvas.create_text(data.width//2,data.height//3,
        text="Choose a game below",font="Arial 35 bold",fill="salmon")
        canvas.create_rectangle(data.margin+20,data.height//2,
        data.margin+data.width//2-30,data.height//2+100,fill="white")
        canvas.create_text(data.margin+data.width//4,data.height//2+30,
        text="Balancing",font="Arial 32 bold", fill="lightsalmon")
        canvas.create_text(data.margin+(data.width//2 - 20)//2,
        data.height//2+70,text="Blocks",font="Arial 32 bold",fill="lightsalmon")
        canvas.create_rectangle(data.width-data.margin-20,data.height//2,
        data.width-data.margin-data.width//2+30,data.height//2+100,fill="white")
        canvas.create_text(data.width*(3/4),data.height//2+50,
        text="Hangman",font="Arial 32 bold", fill="lightsalmon")
    if data.startBlockState:
        #draws centered white square and text with instructions
        canvas.create_rectangle(data.starterx1,data.startery1,data.starterx2,
        data.startery2,fill="white",outline="black")
        canvas.create_text(data.width//2,data.height//2,
        text="Press 'b' to begin",font="Arial 30 bold")
        #draws each randomly generated block
        for block in data.randomBlocks:
            canvas.create_rectangle(block[0],block[1],block[2],block[3],
            fill="peachpuff")
    if data.instructionBlockState:
        data.spaceAbove = 25
        #draws instructions on how to play the game
        canvas.create_text(data.width//2,data.margin+data.spaceAbove,
        text="Place the blocks on top of each other to",font="Arial 22",
        fill="black")
        canvas.create_text(data.width//2,data.margin+data.spaceAbove*2,
        text="create a pile that reaches the top of",font="Arial 22",
        fill="black")
        canvas.create_text(data.width//2,data.margin+data.spaceAbove*3,
        text="the screen without falling over.",font="Arial 22",
        fill="black")
        #draws the example of stacked blocks
        block1Size = 100
        block2Size = 80
        block3Size = 40
        canvas.create_rectangle(data.width//2,data.height//2+10,
        data.width//2+block1Size,data.height//2+20+block1Size,
        fill="lightsalmon")
        canvas.create_rectangle(data.width//2,data.height//2-70,
        data.width//2+block2Size,data.height//2-70+block2Size,
        fill="lightsalmon")
        canvas.create_rectangle(data.width//2,data.height//2-110,
        data.width//2+block3Size,data.height//2-110+block3Size,
        fill="lightsalmon")
        spaceBelow = 3/4
        #draws instructions on how to move the blocks
        canvas.create_text(data.width//2,data.height*spaceBelow,
        text="Use the arrow keys to move the falling",
        font="Arial 22", fill="black")
        canvas.create_text(data.width//2,data.height*spaceBelow+25,
        text="block after you have clicked and selected a block.",
        font="Arial 22", fill="black")
        #creates the continue button
        data.buttonWidth = data.width*(1/5)
        data.buttonHeight = data.height*(1/12)
        canvas.create_rectangle(data.width//2-data.buttonWidth//2,
        data.height-data.spaceAbove-data.buttonHeight,
        data.width//2 + data.buttonWidth//2,
        data.height-data.spaceAbove,fill="white")
        canvas.create_text(data.width//2,
        data.height-data.spaceAbove-data.buttonHeight//2,
        text="Continue", font="Arial 22",fill="black")
    if data.gameBlockState:
        #draws each moving block
        for block in data.movingBlocks:
            canvas.create_rectangle(block[0],block[1],block[2],block[3],
            fill=block[4])
        for block in data.bottomBlocks:
            canvas.create_rectangle(block[0],block[1],block[2],block[3],
            fill="tomato")
        #draws each stopped block
        for block in data.stoppedBlocks:
            canvas.create_rectangle(block[0],block[1],block[2],block[3],
            fill=block[4])
            if block[1] <= data.margin:
                data.gameBlockState = False
                data.winBlockState = True
        textSize = 22
        scoreText = "Score: %d" % (data.score)
        canvas.create_text(data.margin+textSize*2, data.margin+textSize,
        text=scoreText,font="Arial 18 bold", fill="indianred")
    if data.winBlockState:
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
    if data.loseBlockState:
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
    if data.startHangmanState:
        canvas.create_text(data.width//2,data.margin+30,
        text="Choose a category below",font="Arial 40 bold",fill="lightsalmon")
        canvas.create_text(data.width//2,data.margin+75,
        text="A word will be randomly generated and you will",
        font="Arial 25 bold",fill="lightsalmon")
        canvas.create_text(data.width//2,data.margin+105,
        text="have 6 chances to correctly guess the word",
        font="Arial 25 bold",fill="lightsalmon")
        #draws categories for the user to choose from
        canvas.create_rectangle(data.width//2-60,data.height//4-20,
        data.width//2+60,data.height//4+20,fill="white")
        canvas.create_text(data.width//2,data.height//4,text="Cities",
        font="Arial 32 bold",fill="tomato")
        canvas.create_rectangle(data.width//2-60,data.height//2-20,
        data.width//2+60,data.height//2+20,fill="white")
        canvas.create_text(data.width//2,data.height//2,text="Food",
        font="Arial 32 bold",fill="tomato")
        canvas.create_rectangle(data.width//2-60,data.height-data.height//4-20,
        data.width//2+60,data.height-data.height//4+20,fill="white")
        canvas.create_text(data.width//2,data.height-data.height//4,
        text="Pets",font="Arial 32 bold",fill="tomato")
    if data.gameHangmanState:
        canvas.create_text(data.width//2,data.margin+30,text="Hangman",
        font="Arial 32 bold",fill="lightsalmon")
        canvas.create_text(data.margin+110,data.height-120,
        text="Letters wrongly guessed",font="Arial 20",fill="lightsalmon")
        canvas.create_rectangle(data.margin,data.height-100,data.margin+215,
        data.height-data.margin,fill="white")
        canvas.create_rectangle(data.width-130,100,data.width-135,500,
        fill="black")
        canvas.create_rectangle(data.width-200,500,data.width-350,505,
        fill="black")

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