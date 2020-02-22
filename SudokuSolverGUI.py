import math, pygame, sys, time, requests
pygame.init()
pygame.display.set_caption('Sudoku Solver')

#screen setup
size = 600
screenSize = width, height = size, size
screen = pygame.display.set_mode(screenSize)
font = pygame.font.Font('freesansbold.ttf', 35)
#Color Constants
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
BLACK = (50, 50, 50)
#board setup
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]
solved = False

""" Takes a sudoku board and initializes the solving functionality"""
def solve(board):
    pygame.display.set_caption('Sudoku Solver (Solving Board)')
    solveCell(board, 0, 0)
    pygame.display.set_caption('Sudoku Solver')

def solveCell(board, row, col):
    #Increment row at the end and return true when all rows are complete
    if col == len(board):
        col = 0
        row = row + 1
        if row == len(board):
            return True

    #skip cells that are not empty
    if board[row][col] != 0:
        #call solveCell on the next column
        return solveCell(board, row, col + 1)

    #loop through possible numbers and check if they work
    for num in range(1, 10):
        #check if the possible number works in the cell
        if (valid(board, row, col, num)):
            #place new number in the cell and redraw the board
            board[row][col] = num

            #
            #redraw the board after every step it makes (runs slower but looks cooler)
            #
            drawBoard(board)

            #solve for the next cell, and if that cell ever fails, return to this one and empty it
            if solveCell(board, row, col + 1):
                return True
            board[row][col] = 0
""" Takes a board, with a row and column, and determines if the provided number works in the cell """
def valid(board, row, col, num):
        #check row
        for i in range(len(board)):
            if board[row][i] == num:
                #number breaks board
                return False

        #check column
        for j in range(len(board)):
            if board[j][col] == num:
                #number breaks board
                return False

        #check sub region
        regionSize = 3
        #get the region index for the row and column
        rowIndex = math.floor(row / regionSize) * regionSize
        colIndex = math.floor(col / regionSize) * regionSize
        
        #check each cell in the sub region
        for x in range(rowIndex, rowIndex + regionSize):
            for y in range(colIndex, colIndex + regionSize):
                if board[x][y] == num:
                    return False
        
        #return true if there were no errors
        return True

""" prints a board in a readable format """
def printBoard(board):
    for i in range(len(board)):
        print(board[i])

""" draws the background template and the numbers on the board """
def drawBoard(board):
    screen.fill(BLACK)
    subSize = 200
    blockSize = 66
    #loop through each cell on each row
    for i in range(9):
        for j in range(9):
            #add offset for each cell, adds extra space between sub groups
            xOffset =  i * blockSize + math.floor(i/3)+2
            yOffset = j * blockSize + math.floor(j/3)+2
            #draw the background tile
            subRect = pygame.Rect(xOffset, yOffset, blockSize - 1, blockSize - 1)
            pygame.draw.rect(screen, WHITE, subRect)
            #get the corresponding number from the board and display it to the board
            boxNum = str(board[j][i])
            if boxNum == "0":
                boxNum = ""
            boxText = font.render(boxNum, True, BLACK)
            screen.blit(boxText, [xOffset + 22, yOffset + 20])
    pygame.display.flip()

""" resets the values of the board to 0 """
def resetBoard():
    #loop through each row and column
    for row in range(len(board)):
        for col in range(len(board)):
            #reset value to 0
            board[row][col] = 0
    #redraww the board when complete
    drawBoard(board)
            
""" resets the board and obtains a new board request via api """
def getNewBoard():
    pygame.display.set_caption('Sudoku Solver (Reseting Board)')
    #resets the board
    resetBoard()
    #gets new board request
    response = requests.get("http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&level=2")
    #parse the squares object from the request in a list
    squares = response.json()['squares']
    #iterate over each square object from list and push the value into the board
    for s in squares:
        x = s['x']
        y = s['y']
        num = s['value']
        board[x][y] = num

    pygame.display.set_caption('Sudoku Solver')

#initialize the board on the screen
drawBoard(board)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        #on right click, start solve process
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #if the puzzle is solved, generate a new board
            if solved == True:
                getNewBoard()
                drawBoard(board)
                solved = False
            #if the puzzle is not solved, begin solve process
            elif solved == False:
                solve(board)
                drawBoard(board)
                solved = True
    pygame.display.flip()