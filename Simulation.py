from cmu_112_graphics import *
from MatchupAlgo import *

# from Main import *
from cardsInfo import *
from allCards import *
from DeckInfo import *
import time
import math

# From
# https://stackoverflow.com/questions/42671252/
# python-pillow-valueerror-decompressed-data-too-large
# Used to remove limitation on max data to cache for photos
from PIL import PngImagePlugin

LARGE_ENOUGH_NUMBER = 10000
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (2048 ** 2)

# Model

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


class LeftPrincessTower(object):
    def __init__(self, team):
        self.health = 2534
        self.isDead = False
        self.isActive = True
        self.team = team
        if self.team == "player":
            self.target = (23, 2)
        elif self.team == "enemy":
            self.target = (8, 2)

    def attack(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.isDead = True
            self.health = 0

    def __repr__(self):
        return f"<{self.team} side left princess tower health={self.health}>"


class RightPrincessTower(object):
    def __init__(self, team):
        self.health = 2534
        self.isDead = False
        self.isActive = True
        self.team = team
        if self.team == "player":
            self.target = (23, 15)
        elif self.team == "enemy":
            self.target = (8, 15)

    def attack(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.isDead = True
            self.health = 0

    def __repr__(self):
        return f"<{self.team} side right princess tower health={self.health}>"


class KingTower(object):
    def __init__(self, team):
        self.health = 2534
        self.isDead = False
        self.isActive = False
        self.team = team
        if self.team == "player":
            self.target = (26, 8)
        elif self.team == "enemy":
            self.target = (5, 8)

    def attack(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.isDead = True
            self.health = 0

    def __repr__(self):
        return f"<{self.team} {self.isActive} active side king tower health={self.health}>"


class Card(object):
    def __init__(self, cardName, team, app):
        self.cardName = cardName
        self.team = team
        if self.team == "enemy":
            self.row = random.randint(0, 15)
            self.col = random.randint(0, 17)
            while (
                findBestPathBFS(
                    app,
                    (self.row, self.col),
                    getTarget(app, self.row, self.col, self.team),
                )
                == None
            ):
                self.row = random.randint(0, 15)
                self.col = random.randint(0, 17)
            self.route = findBestPathBFS(
                app,
                (self.row, self.col),
                getTarget(app, self.row, self.col, self.team),
            )
        elif self.team == "player":
            self.row = random.randint(17, 31)
            self.col = random.randint(0, 17)
            while (
                findBestPathBFS(
                    app,
                    (self.row, self.col),
                    getTarget(app, self.row, self.col, self.team),
                )
                == None
            ):
                self.row = random.randint(17, 31)
                self.col = random.randint(0, 17)
            self.route = findBestPathBFS(
                app,
                (self.row, self.col),
                getTarget(app, self.row, self.col, self.team),
            )
        if (
            self.cardName in spawnerBuildings
            or self.cardName in defensiveTowers
        ):
            self.route = [(self.row, self.col)]
        self.isOnCooldown = False
        self.isOnBoard = False
        self.cooldown = 0

    def move(self):
        if self.route != []:
            move = self.route[0]
            self.row = move[0]
            self.col = move[1]
            self.route.pop(0)

    def spawn(self):
        # print("spawning", self.cardName)
        self.cooldown = 50
        self.isOnBoard = True
        self.isOnCooldown = True

    def updateCooldown(self):
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.isOnCooldown = False
            self.cooldown = 0

    def kill(self, app):
        self.isOnBoard = False
        if self.team == "enemy":
            self.row = random.randint(0, 15)
            self.col = random.randint(0, 17)
            while (
                findBestPathBFS(
                    app,
                    (self.row, self.col),
                    getTarget(app, self.row, self.col, self.team),
                )
                == None
            ):
                self.row = random.randint(0, 15)
                self.col = random.randint(0, 17)
            self.route = findBestPathBFS(
                app,
                (self.row, self.col),
                getTarget(app, self.row, self.col, self.team),
            )
        elif self.team == "player":
            self.row = random.randint(17, 31)
            self.col = random.randint(0, 17)
            while (
                findBestPathBFS(
                    app,
                    (self.row, self.col),
                    getTarget(app, self.row, self.col, self.team),
                )
                == None
            ):
                self.row = random.randint(17, 31)
                self.col = random.randint(0, 17)
            self.route = findBestPathBFS(
                app,
                (self.row, self.col),
                getTarget(app, self.row, self.col, self.team),
            )

    def reroute(self, app):
        self.route = findBestPathBFS(
            app,
            (self.row, self.col),
            getTarget(app, self.row, self.col, self.team),
        )


def getTarget(app, row, col, team):
    towers = app.enemyTowers if team == "player" else app.playerTowers
    bestDistance = None
    bestTower = None
    if (
        towers[0].health == 0
        and towers[1].health == 0
        and towers[2].health == 0
    ):
        print("HITTING GAME OVER")
        gameOver(app)
    for tower in towers:
        if (tower.health != 0) and (tower.isActive):
            distanceToTower = towerDistance(app, row, col, tower)
            if (bestTower == None) or distanceToTower <= bestDistance:
                bestTower = tower
                bestDistance = distanceToTower
    return bestTower.target


def __repr__(self):
    str = f"<card={self.cardName}, team={self.team}, isOnBaord={self.isOnBoard}, pos={(self.row, self.col)}>, route={self.route}cooldown={self.cooldown}, isOnCooldown={self.isOnCooldown}"
    return str


def average(x0, x1):
    return (x0 + x1) // 2


def initBoard(app):
    board = [([False] * app.cols) for row in range(app.rows)]
    for row in range(app.rows):
        for col in range(app.cols):
            if (row <= 13 or row >= 17) or (col == 3 or col == 14):
                board[row][col] = True
            if (row == 0 or row == 31) and not (6 <= col <= 11):
                board[row][col] = False
            # King tower enemy side
            if (1 <= row <= 4) and (7 <= col <= 10):
                board[row][col] = False
            # King tower player side
            if (27 <= row <= 30) and (7 <= col <= 10):
                board[row][col] = False
            # Princess tower left enemy side
            if (5 <= row <= 7) and (2 <= col <= 4):
                board[row][col] = False
            # Princess tower right enemy side
            if (5 <= row <= 7) and (13 <= col <= 15):
                board[row][col] = False
            # Princess tower left player side
            if (24 <= row <= 26) and (2 <= col <= 4):
                board[row][col] = False
            # Princess tower right player side
            if (24 <= row <= 26) and (13 <= col <= 15):
                board[row][col] = False
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
            if cardObj.isOnBoard == True:
                cardObj.move()


def updateAllCooldowns(app):
    team = app.playerCards
    for cardName in team:
        cardObj = team[cardName]
        cardObj.updateCooldown()
    team = app.enemyCards
    for cardName in team:
        cardObj = team[cardName]
        cardObj.updateCooldown()


def randomSpawn(app):
    teamInfo = app.playerCards
    teamList = app.playerDeck
    list = []
    for card in teamList:
        if teamInfo[card].isOnCooldown == False:
            list.append(card)
    if len(list) > 0:
        index = random.randint(0, len(list) - 1)
        cardName = list[index]
        cardObj = teamInfo[cardName]
        cardObj.spawn()
        app.spawnedTime = time.time()
    teamInfo = app.enemyCards
    teamList = app.enemyDeck
    list = []
    for card in teamList:
        if teamInfo[card].isOnCooldown == False:
            list.append(card)
    if len(list) > 0:
        index = random.randint(0, len(list) - 1)
        cardName = list[index]
        cardObj = teamInfo[cardName]
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


def cardDistance(app, cardObj1, cardObj2):
    (player_x0, player_y0, player_x1, player_y1) = getCellBounds(
        app, cardObj1.row, cardObj1.col
    )
    (x0, y0, x1, y1) = getCellBounds(app, cardObj2.row, cardObj2.col)
    xPlayer, yPlayer = average(player_x0, player_x1), average(
        player_y0, player_y1
    )
    xEnemy, yEnemy = average(x0, x1), average(y0, y1)
    return math.sqrt((xEnemy - xPlayer) ** 2 + (yEnemy - yPlayer) ** 2)


def towerDistance(app, row, col, tower):
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    xCards, yCard = average(x0, x1), average(y0, y1)
    xTower, yTower = tower.target
    return math.sqrt((xTower - xCards) ** 2 + (yTower - yCard) ** 2)


def checkForDeaths(app):
    for playerKey in app.playerCards:
        for enemyKey in app.enemyCards:
            playerCard = app.playerCards[playerKey]
            enemyCard = app.enemyCards[enemyKey]
            if (
                playerCard.isOnBoard
                and enemyCard.isOnBoard
                and cardDistance(app, playerCard, enemyCard) <= (2 * 21)
            ):
                if playerCard.cardName in getAllCounters(enemyCard.cardName):
                    # print(playerCard.cardName, "counters", enemyCard.cardName)
                    playerCard.kill(app)
                if enemyCard.cardName in getAllCounters(playerCard.cardName):
                    # print(enemyCard.cardName, "counters", playerCard.cardName)
                    enemyCard.kill(app)


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
    return result


def findBestPathBFS(app, start, target):
    startRow, startCol = start
    targetRow, targetCol = target
    queue = []
    path = []
    queue.append([startRow, startCol, path])
    visited = set()

    while len(queue) > 0:
        currRow, currCol, path = queue.pop(0)
        if currRow == targetRow and currCol == targetCol:
            return path
        if app.board[currRow][currCol] != True:
            continue
        for drow in [-1, 0 + 1]:
            for dcol in [-1, 0, +1]:
                if drow == 0 and dcol == 0:
                    continue
                newRow = currRow + drow
                newCol = currCol + dcol
                if (
                    (0 <= newRow <= app.rows - 1)
                    and (0 <= newCol <= app.cols - 1)
                    and ((newRow, newCol) not in visited)
                ):
                    newPath = path + [(newRow, newCol)]
                    queue.append([newRow, newCol, newPath])
                    visited.add((newRow, newCol))
    return None


def damageTowers(app):
    towerTeam = "player"
    damageTowersHelper(app, towerTeam)
    towerTeam = "enemy"
    damageTowersHelper(app, towerTeam)
    return


def damageTowersHelper(app, towerTeam):
    if towerTeam == "player":
        towerTeam = app.playerTowers
        enemyTeam = app.enemyCards
    elif towerTeam == "enemy":
        towerTeam = app.enemyTowers
        enemyTeam = app.playerCards
    for tower in towerTeam:
        # print(tower)
        enemyAttackCount = 0
        for card in enemyTeam:
            if (enemyTeam[card].row, enemyTeam[card].col) == tower.target:
                enemyAttackCount += 1
        tower.attack(enemyAttackCount * 100)
        if towerTeam[0].health == 0 or towerTeam[1].health == 0:
            towerTeam[2].isActive = True
        if towerTeam[2].health == 0:
            gameOver(app)
            print("HITTING GAME OVER")
            break


def refreshTargets(app):
    team = app.playerCards
    enemyTowers = app.enemyTowers
    for cardName in team:
        for tower in enemyTowers:
            if (
                team[cardName].row,
                team[cardName].col,
            ) == tower.target and tower.health == 0:
                team[cardName].reroute(app)
    team = app.enemyCards
    enemyTowers = app.playerTowers
    for cardName in team:
        for tower in enemyTowers:
            if (
                team[cardName].row,
                team[cardName].col,
            ) == tower.target and tower.health == 0:
                team[cardName].reroute(app)


def gameOver(app):
    print(app.enemyTowers)
    if app.enemyTowers[2].health == 0:
        app.winner = "player"
        app.gameOver = True
        print("PLAYER WON PLAYER WON!!!")
        return
    if app.playerTowers[2].health == 0:
        app.winner = "enemy"
        app.gameOver = True
        print("ENEMY WON ENEMY WON!!!")
        return


def appStarted(app):
    app.gameOver = False
    app.winner = None
    app.timerDelay = 400
    app.margin = 20
    app.cols = 18
    app.rows = 32
    app.board = initBoard(app)
    app.allCardImages = initAllCardImages(app)
    app.playerCards = {}
    app.enemyCards = {}
    app.playerTowers = [
        LeftPrincessTower("player"),
        RightPrincessTower("player"),
        KingTower("player"),
    ]
    app.enemyTowers = [
        LeftPrincessTower("enemy"),
        RightPrincessTower("enemy"),
        KingTower("enemy"),
    ]
    app.playerDeck = deck
    app.enemyDeck = matchup
    app.adjacencyList = initAdjacencyList(app)
    addTeamCards(app, deck, "player")
    addTeamCards(app, matchup, "enemy")
    app.spawnedTime = time.time()
    randomSpawn(app)
    app.arenaImage = app.loadImage("arena.png")
    app.arenaImage = app.scaleImage(app.arenaImage, 0.88)


# View
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            r = 6
            if app.board[row][col] == True:
                canvas.create_oval(x0 + r, y0 + r, x1 - r, y1 - r, fill="green")
            else:
                canvas.create_oval(x0 + r, y0 + r, x1 - r, y1 - r, fill="gray")
            # canvas.create_text(
            #     average(x0, x1),
            #     average(y0, y1),
            #     text=f"({row},{col})",
            #     font="Arial 5 bold",
            # )


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


def drawBackgroundImage(app, canvas):
    canvas.create_image(
        app.width // 2,
        app.height // 2 + 90,
        image=ImageTk.PhotoImage(app.arenaImage),
    )


def drawRecap(app, canvas):
    if app.winner == "player":
        canvas.create_text(
            app.width // 2,
            app.height // 2,
            text="Your deck won!",
            font="Arial 24 bold",
        )
    else:
        canvas.create_text(
            app.width // 2,
            app.height // 2,
            text="Your deck lost :(",
            font="Arial 24 bold",
        )


def drawAllPaths(app, canvas):
    for cardName in app.playerCards:
        route = app.playerCards[cardName].route
        for coords in route:
            (x0, y0, x1, y1) = getCellBounds(app, coords[0], coords[1])
            r = 6
            canvas.create_oval(x0 + r, y0 + r, x1 - r, y1 - r, fill="blue")
    for cardName in app.enemyCards:
        route = app.enemyCards[cardName].route
        for coords in route:
            (x0, y0, x1, y1) = getCellBounds(app, coords[0], coords[1])
            canvas.create_oval(x0 + r, y0 + r, x1 - r, y1 - r, fill="red")


def redrawAll(app, canvas):
    if app.gameOver:
        drawRecap(app, canvas)
    else:
        drawBackgroundImage(app, canvas)
        drawBoard(app, canvas)
        drawTeamCards(app, canvas, "player")
        drawTeamCards(app, canvas, "enemy")
        drawAllPaths(app, canvas)


# Controller
def timerFired(app):
    if app.gameOver == False:
        executeCardRoutes(app)
        checkForDeaths(app)
        damageTowers(app)
        gameOver(app)
        refreshTargets(app)
        updateAllCooldowns(app)
        if (time.time() - app.spawnedTime) >= 3:
            randomSpawn(app)
            app.spawntedTime = time.time()


def keyPressed(app, event):
    pass


runApp(width=420, height=680)
