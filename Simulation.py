from PIL.ImageDraw import Outline
from cmu_112_graphics import *
from MatchupAlgo import *

# from Main import *
from cardsInfo import *
from allCards import *
from DeckInfo import *
import time

# From
# https://stackoverflow.com/questions/42671252/
# python-pillow-valueerror-decompressed-data-too-large
# Used to remove limitation on max data to cache for photos
from PIL import PngImagePlugin

LARGE_ENOUGH_NUMBER = 10000
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (2048 ** 2)
# Model


def repr2dList(L):
    if L == []:
        return "[]"
    output = []
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [[""] * cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append("[\n")
    for row in range(rows):
        output.append(" [ ")
        for col in range(cols):
            if col > 0:
                output.append(", " if col < len(L[row]) else "  ")
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((" ]," if row < rows - 1 else " ]") + "\n")
    output.append("]")
    return "".join(output)


def print2dList(L):
    print(repr2dList(L))


deck = [
    "Cannon",
    "Fireball",
    "Skeletons",
    "Ice Golem",
    "The Log",
    "Hog Rider",
    "Musketeer",
    "Ice Spirit",
]

matchup = [
    "Balloon",
    "Baby Dragon",
    "Giant Skeleton",
    "Miner",
    "Goblin Gang",
    "Tesla",
    "Zap",
    "Tornado",
]


class Card(object):
    def __init__(self, cardName, team, app):
        self.cardName = cardName
        self.team = team
        if self.team == "enemy":
            self.row = random.randint(0, 13)
            self.col = random.randint(0, 17)
            # self.route = findBestPath(app, self.row, self.col)
            self.route = [(+1, 0)] * 20
        elif self.team == "player":
            self.row = random.randint(17, 31)
            self.col = random.randint(0, 17)
            # self.route = findBestPath(app, self.row, self.col)
            self.route = [(-1, 0)] * 20
        self.isOnCooldown = False
        self.isOnBoard = False
        self.cooldown = 0

    def move(self):
        self.row += self.direction[0]
        self.col += self.direction[1]

    def spawn(self):
        self.cooldown = 5
        self.isOnBoard = True
        self.isOnCooldown = True

    def updateCooldown(self):
        if self.cooldown <= 0:
            self.isOnCooldown = False
            self.cooldown = 0
        else:
            self.cooldown -= 1
            print(self.cardName, self.cooldown)

    def __repr__(self):
        str = f"<card={self.cardName}, team={self.team}, isOnBaord={self.isOnBoard}, pos={(self.row, self.col)}>, route={self.route}cooldown={self.cooldown}, isOnCooldown={self.isOnCooldown}"
        return str


def reconstruct(app, row, col, target, backwardsPath):
    path = []
    for row in range(app.rows - 1, -1, -1):
        for col in range(app.cols - 1, -1, -1):
            if backwardsPath[row][col] != None:
                path.append(backwardsPath[row][col])
    path.reverse()
    return path


# def getNeighbors(app, node):
#     row, col = node
#     neighbors = []
#     for drow in (-1, 0, +1):
#         for dcol in (-1, 0, +1):
#             if drow == 0 and dcol == 0:
#                 continue
#             newRow, newCol = row + drow, col + dcol
#             if (0 <= newRow <= app.rows - 1) and (0 <= newCol <= app.cols - 1):
#                 neighbors.append((newRow, newCol))
#     return neighbors


def findPath(app, start, target):
    # get queue / enqueue data structure?
    # add row, col to queue
    # make visited list full of 32 * 18 falses
    # make prev list of 32 * 18 long None
    # loop through while the list isn't empty
    # get rid of first el of list (dequeue) -> this is our node
    # get all neighbors of the node using agency list or matrix
    # loop through all univsited neighbors
    # enqueue the neighbor (put at end of list)
    # make the neighbor as visited
    # make prev list at this neighbor = node from before
    # return prev list
    queue = []
    queue.append(start)
    visited = [False] * 575
    visited[start] = True
    prev = [None] * 575
    while len(queue) != 0:
        node = queue.pop(0)
        neighbors = app.adjancencyList[node]
        if node == target:
            return prev
        for neighbor in neighbors:
            if visited[neighbor] == False:
                queue.append(neighbor)
                visited[neighbor] = True
                prev[neighbor] = node
    return prev


def bfs(app, row, col, target):
    backwardsPath = findPath(app, row, col, target)
    path = reconstruct(app, row, col, target, backwardsPath)
    return path


def findBestPath(app, row, col):
    visited = []
    # Middle of the bridge for now
    targetRow, targetCol = 15, 3
    target = (targetRow, targetCol)
    return findBestPathHelper(app, row, col, target, visited)


def findBestPathHelper(app, row, col, target, visited):
    print(visited)
    coords = (row, col)
    if coords in visited:
        return False
    if coords == target:
        return visited
    visited.append(coords)
    for drow in (-1, 0, +1):
        for dcol in (-1, 0, +1):
            if drow == 0 and dcol == 0:
                continue
            newRow = row + drow
            newCol = col + dcol
            if (
                (0 <= newRow <= app.rows - 1)
                and (0 <= newCol <= app.cols - 1)
                and (app.board[newRow][newCol])
            ):
                solution = findBestPathHelper(
                    app, newRow, newCol, target, visited
                )
                if solution != False:
                    return solution
    visited.remove((row, col))
    return False


class PrincessTower(object):
    pass


class KingTower(object):
    pass


def average(x0, x1):
    return (x0 + x1) // 2


def initBoard(app):
    board = [([False] * app.cols) for row in range(app.rows)]
    for row in range(app.rows):
        for col in range(app.cols):
            if (row <= 13 or row >= 17) or (col == 3 or col == 14):
                board[row][col] = True
    return board


def initAllCardImages(app):
    result = {}
    for cardName in cardsInfo:
        cacheImage = app.loadImage(f"card-images/{cardName}.png")
        scaledImage = app.scaleImage(cacheImage, 1 / 6)
        result[cardName] = scaledImage
    return result


def getCellBounds(app, row, col):
    boardHeight = app.height - 2 * app.margin
    boardWidth = app.width - 2 * app.margin
    cellWidth = boardWidth // app.cols
    cellHeight = boardHeight // app.rows
    x0 = app.margin + (cellWidth * col)
    y0 = app.margin + (cellHeight * row)
    x1 = app.margin + (cellWidth * (col + 1))
    y1 = app.margin + (cellHeight * (row + 1))
    return (x0, y0, x1, y1)


def addCard(app, cardName, team):
    if team == "player":
        app.playerCards[cardName] = Card(cardName, team, app)
    elif team == "enemy":
        app.enemyCards[cardName] = Card(cardName, team, app)


def addTeamCards(app, deck, team):
    for cardName in deck:
        addCard(app, cardName, team)


def executeCardRoutes(app):
    teams = [app.playerCards, app.enemyCards]
    for team in teams:
        for cardName in team:
            cardObj = team[cardName]
            if (cardObj.isOnBoard == True) and (len(cardObj.route) > 0):
                move = cardObj.route[0]
                cardObj.row += move[0]
                cardObj.col += move[1]
                cardObj.route.pop(0)


def updateAllCooldowns(app):
    teams = [app.playerCards, app.enemyCards]
    for team in teams:
        for cardName in team:
            cardObj = team[cardName]
            if (cardObj.cooldown != 0) and (cardObj.isOnCooldown):
                cardObj.updateCooldown


def randomSpawn(app):
    teams = [app.playerCards, app.enemyCards]
    if (time.time() - app.spawnedTime) >= 1:
        for team in teams:
            teamList = (
                app.playerDeck if team == app.playerCards else app.enemyDeck
            )
            index = random.randint(0, len(teamList) - 1)
            cardName = teamList[index]
            cardObj = team[cardName]
            if cardObj.isOnCooldown == False:
                cardObj.spawn()
        app.spawnedTime = time.time()


def getNumberedNeighbors(row, col, grid):
    neighbors = []
    for drow in (-1, 0, +1):
        for dcol in (-1, 0, +1):
            if drow == 0 and dcol == 0:
                continue
            if (0 <= row + drow < len(grid)) and (
                0 <= col + dcol < len(grid[0])
            ):
                neighbors.append(grid[row + drow][col + dcol])
    return neighbors


def initAdjacencyList(app):
    numberedGrid = [([0] * app.cols) for row in range(app.rows)]
    index = 0
    for row in range(app.rows):
        for col in range(app.cols):
            numberedGrid[row][col] = index
            index += 1
    result = {}
    for row in range(app.rows):
        for col in range(app.cols):
            number = numberedGrid[row][col]
            neighbors = getNumberedNeighbors(row, col, numberedGrid)
            for neighbor in neighbors:
                if number not in result:
                    result[number] = set()
                result[number].add(neighbor)
    print(result)
    return result


def appStarted(app):
    app.timerDelay = 300
    app.margin = 20
    app.cols = 18
    app.rows = 32
    app.board = initBoard(app)
    app.allCardImages = initAllCardImages(app)
    app.playerCards = {}
    app.enemyCards = {}
    app.playerDeck = deck
    app.enemyDeck = matchup
    addTeamCards(app, deck, "player")
    addTeamCards(app, matchup, "enemy")
    app.spawnedTime = time.time()
    randomSpawn(app)
    # print(app.playerCards["Cannon"])
    app.adjancencyList = initAdjacencyList(app)
    # print(bfs(app, 0, 0, (15, 3)))


# View
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            if app.board[row][col]:
                canvas.create_rectangle(x0, y0, x1, y1, fill="green")
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill="gray")


def drawTeamCards(app, canvas, team):
    if team == "player":
        team = app.playerCards
    elif team == "enemy":
        team = app.enemyCards
    for card in team:
        cardObj = team[card]
        if cardObj.isOnBoard:
            (x0, y0, x1, y1) = getCellBounds(app, cardObj.row, cardObj.col)
            x, y = average(x0, x1), average(y0, y1)
            canvas.create_image(
                x, y, image=ImageTk.PhotoImage(app.allCardImages[card])
            )


def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawTeamCards(app, canvas, "player")
    drawTeamCards(app, canvas, "enemy")
    for cell in app.playerCards["Cannon"].route:
        x0, y0, x1, y1 = getCellBounds(
            app, app.playerCards["Cannon"].row, app.playerCards["Cannon"].col
        )
        canvas.create_rectangle(x0, y0, x1, y1, fill="orange")
        x0, y0, x1, y1 = getCellBounds(app, cell[0], cell[1])
        canvas.create_rectangle(x0, y0, x1, y1, fill="red")


# Controller
def timerFired(app):
    updateAllCooldowns(app)
    randomSpawn(app)
    executeCardRoutes(app)


def keyPressed(app, event):
    pass


runApp(width=420, height=680)
