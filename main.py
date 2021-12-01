from MatchupAlgo import *
from cmu_112_graphics import *
from cardsInfo import *
from allCards import *
import time
import math

# From
# https://stackoverflow.com/questions/42671252/python-pillow-valueerror-decompressed-data-too-large
# Used to remove limitation on max data to cache for photos
from PIL import PngImagePlugin

LARGE_ENOUGH_NUMBER = 100
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (1024 ** 2)

# IMAGE CITATIONS:
# Elixir.png from https://clashroyale.fandom.com/wiki/Elixir
# arena.png from https://aminoapps.com/c/clash-royale/page/blog/first-battle-in-royale-arena/4G68_NWtYuN5qabloNDN1o8NW7X7KqwWkJ
# All card info and images from data from clash royale API https://developer.clashroyale.com/#/

# Simulation Model
################################################


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
        self.health = 3568
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
            or self.cardName == "Elixir Collector"
            or self.cardName == "Mortar"
            or self.cardName == "X-bow"
        ):
            self.route = [(self.row, self.col)]
        if self.cardName in spellCards:
            self.route = [getTarget(app, self.row, self.col, self.team)]
        self.isOnCooldown = False
        self.isOnBoard = False
        self.cooldown = 0

    def move(self, app):
        if self.cardName in spellCards and self.route == []:
            self.kill(app)
        if self.route != []:
            move = self.route[0]
            self.row = move[0]
            self.col = move[1]
            self.route.pop(0)

    def spawn(self):
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
            if (
                self.cardName in spawnerBuildings
                or self.cardName in defensiveTowers
                or self.cardName == "Elixir Collector"
                or self.cardName == "Mortar"
                or self.cardName == "X-bow"
            ):
                self.route = [(self.row, self.col)]
            if self.cardName in spellCards:
                self.route = [getTarget(app, self.row, self.col, self.team)]
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
                or self.cardName == "Elixir Collector"
                or self.cardName == "Mortar"
                or self.cardName == "X-bow"
            ):
                self.route = [(self.row, self.col)]
            if self.cardName in spellCards:
                self.route = [getTarget(app, self.row, self.col, self.team)]

    def reroute(self, app):
        self.route = findBestPathBFS(
            app,
            (self.row, self.col),
            getTarget(app, self.row, self.col, self.team),
        )

    def __repr__(self):
        str = f"<card={self.cardName}, team={self.team}, isOnBoard={self.isOnBoard}, pos={(self.row, self.col)}>, route={self.route}cooldown={self.cooldown}, isOnCooldown={self.isOnCooldown}"
        return str


def targetCardDistance(app, row, col, otherRow, otherCol):
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    (x0_, y0_, x1_, y1_) = getCellBounds(app, otherRow, otherCol)
    y2 = average(y0_, y1_)
    y1 = average(y0, y1)
    x2 = average(x0_, x1_)
    x1 = average(x0, x1)
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def getTarget(app, row, col, team):
    towers = app.enemyTowers if team == "player" else app.playerTowers
    bestDistance = None
    bestTower = None
    if (
        towers[0].health == 0
        and towers[1].health == 0
        and towers[2].health == 0
    ):
        gameOver(app)
    for tower in towers:
        if tower.health != 0:
            distanceToTower = towerDistance(app, row, col, tower)
            if (bestTower == None) or distanceToTower < bestDistance:
                bestTower = tower
                bestDistance = distanceToTower
    gameOver(app)
    return bestTower.target


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
    boardHeight = app.newHeight - 2 * app.margin
    boardWidth = app.newWidth - 2 * app.margin
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
                cardObj.move(app)


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
    (x0, y0, x1, y1) = getCellBounds(app, tower.target[0], tower.target[1])
    xTower, yTower = average(x0, x1), average(y0, y1)
    return math.sqrt((xTower - xCards) ** 2 + (yTower - yCard) ** 2)


def checkForDeaths(app):
    for playerKey in app.playerCards:
        for enemyKey in app.enemyCards:
            playerCard = app.playerCards[playerKey]
            enemyCard = app.enemyCards[enemyKey]
            if (
                playerCard.isOnBoard
                and enemyCard.isOnBoard
                and cardDistance(app, playerCard, enemyCard) <= (4 * 21)
            ):
                if playerCard.cardName in getAllCounters(enemyCard.cardName):
                    app.message = (
                        f"{enemyCard.cardName} counters {playerCard.cardName}!"
                    )
                    playerCard.kill(app)
                    enemyCard.reroute(app)
                if enemyCard.cardName in getAllCounters(playerCard.cardName):
                    app.message = (
                        f"{playerCard.cardName} counters {enemyCard.cardName}!"
                    )
                    enemyCard.kill(app)
                    playerCard.reroute(app)


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
    startRow, startCol = start[0], start[1]
    targetRow, targetCol = target[0], target[1]
    queue = []
    path = []
    visited = set()
    queue.append([startRow, startCol, path])

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
        enemyAttackCount = 0
        for card in enemyTeam:
            if (
                enemyTeam[card].row,
                enemyTeam[card].col,
            ) == tower.target and enemyTeam[card].isOnBoard:
                enemyAttackCount += 1
        tower.attack(enemyAttackCount * 100)
        if towerTeam[0].health == 0 or towerTeam[1].health == 0:
            towerTeam[2].isActive = True
        if towerTeam[2].health == 0:
            gameOver(app)
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
    if app.enemyTowers[2].health == 0:
        app.winner = "player"
        app.gameOver = True
        return
    if app.playerTowers[2].health == 0:
        app.winner = "enemy"
        app.gameOver = True
        return


# Model
################################################


def initCardImages(app):
    result = [([0] * app.cardArrayCols) for row in range(app.cardArrayRows)]
    index = 0
    for row in range(app.cardArrayRows):
        for col in range(app.cardArrayCols):
            if index >= len(allCards):
                break
            tempImage = app.loadImage(
                f"card-images/{allCards[index]['name']}.png"
            )
            scaledImage = app.scaleImage(tempImage, 1 / 4)
            lessScaledImage = app.scaleImage(tempImage, 1 / 3)
            result[row][col] = {
                "name": allCards[index]["name"],
                "image": scaledImage,
                "big-image": lessScaledImage,
            }
            index += 1
    return result


def resetApp(app):
    app.state = "createDeck"
    app.currDeckRow = 0
    app.currDeckCol = 0
    app.deck = [([0] * app.deckCols) for row in range(app.deckRows)]
    app.isDeckFull = False
    app.analysis = None


def initSimulationInfo(app):
    app.newWidth = 420
    app.newHeight = 680

    app.gameOver = False
    app.winner = None
    app.timerDelay = 500
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
    app.playerDeck = app.prepDeck
    app.enemyDeck = findBestCounterDeck(app.prepDeck)
    app.adjacencyList = initAdjacencyList(app)
    addTeamCards(app, app.playerDeck, "player")
    addTeamCards(app, app.enemyDeck, "enemy")
    app.spawnedTime = time.time()
    randomSpawn(app)
    app.arenaImage = app.loadImage("arena.png")
    app.arenaImage = app.scaleImage(app.arenaImage, 0.88)
    app.message = ""


def appStarted(app):
    app.buttonY = 300
    app.buttonX = (app.width) // 2
    app.deckMargin = 500
    app.deckHeight = app.height // 4.3
    app.margin = 40
    app.inputDeckWrapperPadding = 45
    app.deckRows = 2
    app.deckCols = 4
    app.cardArrayRows = 6
    app.cardArrayCols = 18
    resetApp(app)
    app.cardImagesMatrix = initCardImages(app)
    app.analysis = None
    app.elixir = app.loadImage("elixir.png")
    app.elixirImage = app.scaleImage(app.elixir, 0.20)


def initImageMatrix(app, matchupObj):
    imageMatrx = [[0, 0, 0, 0], [0, 0, 0, 0]]
    deck = [[0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(len(matchupObj.matchup)):
        if i < 4:
            deck[0][i] = matchupObj.matchup[i]
        else:
            j = i - 4
            deck[1][j] = matchupObj.matchup[i]
    for row in range(2):
        for col in range(4):
            cachedImage = app.loadImage(f"card-images/{deck[row][col]}.png")
            imageMatrx[row][col] = app.scaleImage(cachedImage, 1 / 4)
    return imageMatrx


# Controller
################################################


def initCounterAndSuggestionData(app, matchup):
    suggestionSynergies = list(matchup.suggestionBestSynergy)
    random.shuffle(suggestionSynergies)
    if len(suggestionSynergies) > 4:
        lengthOfSynergies = 4
    else:
        lengthOfSynergies = len(suggestionSynergies)
    cachedSynergyImages = [
        app.loadImage(f"card-images/{suggestionSynergies[i]}.png")
        for i in range(lengthOfSynergies)
    ]
    synergiesImages = [
        app.scaleImage(cachedSynergyImages[i], 1 / 4)
        for i in range(len(cachedSynergyImages))
    ]

    # Getting matchup info
    counteredCard = matchup.counteredCard
    selectCounters = [matchup.counters[i] for i in range(len(matchup.counters))]
    suggestion = matchup.suggestion
    # Caching images
    cachedcounteredCardImage = app.loadImage(f"card-images/{counteredCard}.png")
    cachedselectCountersImages = [
        app.loadImage(f"card-images/{selectCounters[i]}.png")
        for i in range(len(matchup.counters))
    ]
    cachedSuggestionImage = app.loadImage(f"card-images/{suggestion}.png")
    # Loading scaled images
    counteredCardImage = app.scaleImage(cachedcounteredCardImage, 1 / 4)
    selectCountersImages = [
        app.scaleImage(cachedselectCountersImages[i], 1 / 4)
        for i in range(len(matchup.counters))
    ]
    suggestionImage = app.scaleImage(cachedSuggestionImage, 1 / 4)
    result = {}
    result["counteredCard"] = counteredCardImage
    result["counters"] = selectCountersImages
    result["suggestion"] = suggestionImage
    result["synergies"] = suggestionSynergies
    result["synergiesImages"] = synergiesImages
    result["elixirChange"] = matchup.elixirChange
    result["matchupElixir"] = matchup.getAverageElixir(matchup.matchup)
    return result


def initAnalysisInfo(app):
    allAnalysis = dict()
    deck = app.prepDeck
    matchups = [metaDeck1, metaDeck2, metaDeck3, metaDeck4]

    rand1 = random.randint(0, len(matchups) - 1)
    app.matchup1 = Matchup(deck, matchups[rand1])
    matchups.pop(rand1)

    rand2 = random.randint(0, len(matchups) - 1)
    app.matchup2 = Matchup(deck, matchups[rand2])
    matchups.pop(rand2)

    rand3 = random.randint(0, len(matchups) - 1)
    app.matchup3 = Matchup(deck, matchups[rand3])
    matchups.pop(rand3)

    rand4 = random.randint(0, len(matchups) - 1)
    app.matchup4 = Matchup(deck, matchups[rand4])
    matchups.pop(rand4)

    allAnalysis = {
        1: app.matchup1,
        2: app.matchup2,
        3: app.matchup3,
        4: app.matchup4,
    }
    app.analysis = allAnalysis
    app.matchupImageMatrices = {
        1: initImageMatrix(app, app.matchup1),
        2: initImageMatrix(app, app.matchup2),
        3: initImageMatrix(app, app.matchup3),
        4: initImageMatrix(app, app.matchup4),
    }
    app.matchupCounterAndSuggestionData = {
        1: initCounterAndSuggestionData(app, app.matchup1),
        2: initCounterAndSuggestionData(app, app.matchup2),
        3: initCounterAndSuggestionData(app, app.matchup3),
        4: initCounterAndSuggestionData(app, app.matchup4),
    }


def analyzeDeckHandler(app):
    prepDeck = []
    for row in range(app.deckRows):
        for col in range(app.deckCols):
            name = app.deck[row][col]["name"]
            prepDeck.append(name)
    app.prepDeck = prepDeck
    app.analysis = True
    app.state = "analysis"
    initAnalysisInfo(app)
    initSmallDeck(app)


def cardIsNotDuplicate(app, card):
    for row in range(app.deckRows):
        if card in app.deck[row]:
            return False
    return True


def getDeckContainerBounds(app, row, col):
    gridWidth = app.width - (2 * app.deckMargin)
    gridHeight = app.deckHeight
    cellWidth = gridWidth // app.deckCols
    cellHeight = gridHeight // app.deckRows
    gapX = 5
    gapY = 5
    x0 = app.deckMargin + (cellWidth * col) + gapX
    y0 = app.margin + (cellHeight * row) + gapY
    x1 = app.deckMargin + (cellWidth * (col + 1)) - gapX
    y1 = app.margin + (cellHeight * (row + 1)) - gapY
    return (x0, y0, x1, y1)


def getDeckListBounds(app, row, col):
    gridWidth = app.width - (2 * app.margin)
    gridHeight = app.height - app.deckHeight - 3 * app.margin
    cellWidth = gridWidth // app.cardArrayCols
    cellHeight = gridHeight // app.cardArrayRows
    x0 = app.margin + (cellWidth * col)
    y0 = app.margin + app.deckHeight + (cellHeight * row)
    x1 = app.margin + (cellWidth * (col + 1))
    y1 = app.margin + app.deckHeight + (cellHeight * (row + 1))
    shiftY = 75
    return (x0, y0 + shiftY, x1, y1 + shiftY)


def getMatchupBounds(app, key, row, col):
    gridWidth = 260
    gridHeight = 160
    cellWidth = gridWidth // 4
    cellHeight = gridHeight // 2
    startY = app.margin + (gridHeight + 30) * (key - 1)
    x0 = app.margin + (cellWidth * col)
    y0 = app.margin + (cellHeight * row) + startY
    x1 = app.margin + (cellWidth * (col + 1))
    y1 = app.margin + (cellHeight * (row + 1)) + startY
    return (x0, y0, x1, y1)


def getCounterBounds(app, key):
    x = app.margin + 350
    y = app.margin + ((160 + 30) * (key - 1)) + 110
    return x, y


def getSuggestionBounds(app, key):
    x = app.margin + 740 + 30
    y = app.margin + ((160 + 30) * (key - 1))
    return x, y


def initSmallDeck(app):
    app.smallDeck = [[0, 0, 0, 0], [0, 0, 0, 0]]
    for row in range(2):
        for col in range(4):
            tempImage = app.loadImage(
                f"card-images/{app.deck[row][col]['name']}.png"
            )
            scaledImage = app.scaleImage(tempImage, 1 / 6)
            app.smallDeck[row][col] = scaledImage


def timerFired(app):
    if app.state == "simulation":
        if app.gameOver == False:
            executeCardRoutes(app)
            checkForDeaths(app)
            damageTowers(app)
            gameOver(app)
            refreshTargets(app)
            updateAllCooldowns(app)
            if (time.time() - app.spawnedTime) >= 5:
                randomSpawn(app)
                app.spawntedTime = time.time()


def keyPressed(app, event):
    if event.key == "s":
        initSimulationInfo(app)
        app.state = "simulation"


def mousePressed(app, event):
    (x0, y0, x1, y1) = getButtonBounds(app)
    if app.state == "createDeck":
        if (
            (app.isDeckFull)
            and (x0 <= event.x <= x1)
            and (y0 <= event.y <= y1)
            and (app.analysis == None)
        ):
            analyzeDeckHandler(app)
            return
        if (
            (x0 <= event.x <= x1)
            and (y0 <= event.y <= y1)
            and (app.analysis != None)
        ):
            resetApp(app)
            return
    elif app.state == "analysis" or app.state == "simulation":
        if (app.width - 50 <= event.x <= app.width) and (0 <= event.y <= 50):
            app.state = "createDeck"
    for row in range(app.cardArrayRows):
        for col in range(app.cardArrayCols):
            (x0, y0, x1, y1) = getDeckListBounds(app, row, col)
            if (
                (x0 <= event.x <= x1)
                and (y0 <= event.y <= y1)
                and (app.isDeckFull == False)
                and (cardIsNotDuplicate(app, app.cardImagesMatrix[row][col]))
            ):
                image = app.cardImagesMatrix[row][col]
                app.deck[app.currDeckRow][app.currDeckCol] = image
                if (app.currDeckRow == app.deckRows - 1) and (
                    app.currDeckCol == app.deckCols - 1
                ):
                    app.isDeckFull = True
                elif app.currDeckCol + 1 < app.deckCols:
                    app.currDeckCol += 1
                else:
                    app.currDeckRow += 1
                    app.currDeckCol = 0


# View
################################################


def drawExitButton(app, canvas):
    # Exit button
    canvas.create_rectangle(
        app.width - 50, 0, app.width, 50, fill="red", outline="red"
    )
    canvas.create_text(
        app.width - 25 - 1,
        25,
        font="Arial 48 bold",
        text="X",
        fill="white",
    )


def drawMatchupDecks(app, canvas):
    # Matchups
    canvas.create_text(
        app.margin + 130,
        app.margin,
        font="Arial 28 bold",
        text="Deck Matchups",
        fill="navy",
    )
    for key in app.matchupImageMatrices:
        for row in range(2):
            for col in range(4):
                (x0, y0, x1, y1) = getMatchupBounds(app, key, row, col)
                x, y = (x0 + x1) // 2, (y0 + y1) // 2
                canvas.create_image(
                    x,
                    y,
                    image=ImageTk.PhotoImage(
                        app.matchupImageMatrices[key][row][col]
                    ),
                )
        (x0, y0, x1, y1) = getMatchupBounds(app, key, 0, 0)
        canvas.create_text(
            x0 + 310,
            y0 + 80,
            text=str(app.matchupCounterAndSuggestionData[key]["matchupElixir"]),
            font="Arial 16 bold",
        )
        canvas.create_image(
            x0 + 285,
            y0 + 80,
            image=ImageTk.PhotoImage(app.elixirImage),
        )


def drawCounters(app, canvas):
    canvas.create_text(
        app.margin + 555,
        app.margin,
        fill="navy",
        text="Weakest Card in Your Deck",
        font="Arial 28 bold",
    )
    for key in app.analysis:
        x, y = getCounterBounds(app, key)
        x += 50
        counteredCardName = app.analysis[key].counteredCard
        counterNames = []
        if len(app.analysis[key].counters) <= 4:
            numberOfCounters = len(app.analysis[key].counters)
        else:
            numberOfCounters = 4
        # Uneven Text handling
        for i in range(numberOfCounters):
            words = app.analysis[key].counters[i].split()
            if len(words) == 2:
                difference = len(words[1]) - len(words[0])
                if difference <= 0:
                    name = words[0] + "\n" + ((" " * -difference) + words[1])
                else:
                    name = (" " * difference) + words[0] + "\n" + words[1]
            else:
                name = ("\n").join(app.analysis[key].counters[i].split())
            counterNames.append(name)
        counteredCardImage = app.matchupCounterAndSuggestionData[key][
            "counteredCard"
        ]
        counters = [
            app.matchupCounterAndSuggestionData[key]["counters"][i]
            for i in range(numberOfCounters)
        ]
        # Counter
        for i in range(numberOfCounters):
            if "\n" in counterNames[i]:
                yValue = y - 61
            else:
                yValue = y - 50
            canvas.create_text(
                x + (70 * i),
                yValue,
                text=f"{counterNames[i]}",
                font="Arial 14 bold",
                fill="black",
            )
            canvas.create_image(
                x + (70 * i),
                y,
                image=ImageTk.PhotoImage(counters[i]),
            )
        canvas.create_text(
            x + 55 + (70 * i),
            y - 10,
            text="Counters",
            font="Arial 8 bold",
            fill="red",
        )
        canvas.create_text(
            x + 55 + (70 * i),
            y,
            text="→",
            font="Arial 36 bold",
            fill="red",
        )
        # Countered card
        canvas.create_text(
            x + 110 + (70 * i),
            y - 50,
            text=f"{counteredCardName}",
            font="Arial 14 bold",
            fill="black",
        )
        canvas.create_image(
            x + 110 + (70 * i),
            y,
            image=ImageTk.PhotoImage(counteredCardImage),
        )


def drawSuggestions(app, canvas):
    # Suggestions
    canvas.create_text(
        app.margin + 510 + 550,
        app.margin,
        fill="navy",
        text="Suggestions",
        font="Arial 28 bold",
    )
    for key in app.analysis:
        counteredCardName = app.analysis[key].counteredCard
        suggestionName = app.analysis[key].suggestion
        suggestionImage = app.matchupCounterAndSuggestionData[key]["suggestion"]
        synergyList = app.matchupCounterAndSuggestionData[key][
            "synergiesImages"
        ]
        synergyImages = []
        for i in range(len(synergyList)):
            synergyImages.append(synergyList[i])
        counteredCardImage = app.matchupCounterAndSuggestionData[key][
            "counteredCard"
        ]
        x, y = getSuggestionBounds(app, key)
        x += 70
        canvas.create_text(x + 20, y + 80, text="Replace", font="Arial 14 bold")
        canvas.create_image(
            x + 85, y + 80, image=ImageTk.PhotoImage(counteredCardImage)
        )
        canvas.create_text(x + 140, y + 80, text="with", font="Arial 14 bold")
        canvas.create_image(
            x + 195, y + 80, image=ImageTk.PhotoImage(suggestionImage)
        )
        canvas.create_text(
            x + 195 + 120,
            y + 80,
            text="which has synergy with:",
            font="Arial 14 bold",
        )
        x -= 70
        x += 85
        for i in range(len(synergyImages)):
            canvas.create_image(
                x + (70 * i),
                y + 160,
                image=ImageTk.PhotoImage(synergyImages[i]),
            )
        canvas.create_text(
            x + (70 * 4) - 10,
            y + 140,
            text="Synergy",
            font="Arial 8 bold",
            fill="green",
        )
        canvas.create_text(
            x + (70 * 4) - 10,
            y + 160,
            text="⇄",
            font="Arial 36 bold",
            fill="green",
        )
        canvas.create_image(
            x + 330, y + 160, image=ImageTk.PhotoImage(suggestionImage)
        )
        elixirChange = app.matchupCounterAndSuggestionData[key]["elixirChange"]
        absElixir = abs(elixirChange)
        if elixirChange >= 0:
            myText = f"+ {absElixir}"
        else:
            myText = f"- {absElixir}"
        canvas.create_text(
            x + 440,
            y + 160,
            text=myText,
            font="Arial 18 bold",
            fill=("green" if elixirChange <= 0 else "red"),
        )
        canvas.create_image(
            x + 405, y + 160, image=ImageTk.PhotoImage(app.elixirImage)
        )


def drawMyDeck(app, canvas):
    canvas.create_text(
        350,
        app.height - 30,
        text="Your Deck:",
        font="Arial 16 bold",
        fill="navy",
    )
    i = 0
    for row in range(2):
        for col in range(4):
            canvas.create_image(
                420 + (i * 43),
                app.height - 30,
                image=ImageTk.PhotoImage(app.smallDeck[row][col]),
            )
            i += 1
    avgElixir = Matchup(app.prepDeck, app.prepDeck).getAverageElixir(
        app.prepDeck
    )
    if avgElixir <= 3.5:
        color = "green"
        text = "LOW"
    elif avgElixir <= 4.0:
        color = "orange"
        text = "MEDIUM"
    else:
        color = "red"
        text = "HIGH"
    canvas.create_text(
        782,
        app.height - 30,
        text=str(avgElixir),
        font="Arial 16 bold",
        fill="black",
    )
    canvas.create_image(
        758,
        app.height - 30,
        image=ImageTk.PhotoImage(app.elixirImage),
    )
    canvas.create_text(
        830,
        app.height - 30,
        text=text,
        font="Arial 16 bold",
        fill=color,
    )


def drawSimulateButton(app, canvas):
    canvas.create_text(
        1070,
        app.height - 20,
        text="PRESS 'S' TO SIMULATE YOUR DECK",
        fill="blue",
        font="Arial 18 bold",
    )


def drawAnalysisPopup(app, canvas):
    drawExitButton(app, canvas)
    drawMatchupDecks(app, canvas)
    drawCounters(app, canvas)
    drawSuggestions(app, canvas)
    drawMyDeck(app, canvas)
    drawSimulateButton(app, canvas)


def redrawAll(app, canvas):
    if app.state == "createDeck":
        drawInputDeck(app, canvas)
        drawInputDeckContainer(app, canvas)
        drawCardsMatrixImages(app, canvas)
        drawAnalyzeButton(app, canvas)
        if app.analysis != None:
            drawClearButton(app, canvas)
    elif app.state == "analysis":
        drawAnalysisPopup(app, canvas)
    elif app.state == "simulation":
        drawExitButton(app, canvas)
        if app.gameOver:
            drawRecap(app, canvas)

        else:
            drawBackgroundImage(app, canvas)
            drawBoard(app, canvas)
            drawTeamCards(app, canvas, "player")
            drawTeamCards(app, canvas, "enemy")
            drawAllPaths(app, canvas)
            drawTowerHealths(app, canvas)
            canvas.create_text(
                900,
                app.height // 2,
                text=f"Running simulation...",
                font="Arial 24 bold",
            )
            canvas.create_text(
                900,
                app.height // 2 + 30,
                text=f"{app.message}",
                font="Arial 24 bold",
            )


def drawClearButton(app, canvas):
    if app.isDeckFull:
        (x0, y0, x1, y1) = getButtonBounds(app)
        canvas.create_rectangle(x0, y0, x1, y1, fill="gray", width=2)
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        canvas.create_text(
            cx, cy, text="Clear", fill="black", font="Arial 24 bold"
        )


def drawAnalyzeButton(app, canvas):
    if app.isDeckFull:
        (x0, y0, x1, y1) = getButtonBounds(app)
        canvas.create_rectangle(x0, y0, x1, y1, fill="green", width=2)
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        canvas.create_text(
            cx, cy, text="Analyze!", fill="white", font="Arial 24 bold"
        )


def getButtonBounds(app):
    length = 300
    height = 40
    (x0, y0, x1, y1) = (
        app.buttonX - length // 2,
        app.buttonY - height // 2,
        app.buttonX + length // 2,
        app.buttonY + height // 2,
    )
    return (x0, y0, x1, y1)


def drawInputDeckContainer(app, canvas):
    (x0A, y0A, x_1, y_1) = getDeckContainerBounds(app, 0, 0)
    (x_0, y_0, x1A, y1A) = getDeckContainerBounds(
        app, app.deckRows - 1, app.deckCols - 1
    )
    canvas.create_rectangle(
        x0A - app.inputDeckWrapperPadding,
        y0A - app.inputDeckWrapperPadding // 3,
        x1A + app.inputDeckWrapperPadding,
        y1A + app.inputDeckWrapperPadding * 1.5,
    )
    for row in range(app.deckRows):
        for col in range(app.deckCols):
            (x0, y0, x1, y1) = getDeckContainerBounds(app, row, col)
            if (row, col) == (app.currDeckRow, app.currDeckCol) and (
                app.isDeckFull == False
            ):
                canvas.create_rectangle(
                    x0, y0, x1, y1, fill="#CDCDCD", outline="red", width=5
                )
                canvas.create_text(
                    app.width // 2,
                    app.buttonY,
                    text="Click on a card below!",
                    font="Arial 24 bold",
                    fill="green",
                )
            elif app.deck[row][col] == 0:
                canvas.create_rectangle(x0, y0, x1, y1, fill="#CDCDCD", width=2)


def drawInputDeck(app, canvas):
    for row in range(app.deckRows):
        for col in range(app.deckCols):
            if app.deck[row][col] != 0:
                (x0, y0, x1, y1) = getDeckContainerBounds(app, row, col)
                selectedCardImage = app.deck[row][col]["big-image"]
                x, y = (x0 + x1) // 2, (y0 + y1) // 2
                canvas.create_image(
                    x, y, image=ImageTk.PhotoImage(selectedCardImage)
                )


def drawCardsMatrixImages(app, canvas):
    for row in range(app.cardArrayRows):
        for col in range(app.cardArrayCols):
            (x0, y0, x1, y1) = getDeckListBounds(app, row, col)
            (x0, y0, x1, y1) = (x0 + 5, y0 + 5, x1 - 5, y1 - 5)
            x, y = (x0 + x1) // 2, (y0 + y1) // 2
            if app.cardImagesMatrix[row][col] != 0:
                cachedImage = app.cardImagesMatrix[row][col]["image"]
                canvas.create_image(x, y, image=ImageTk.PhotoImage(cachedImage))


# Simulation View
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            r = 7
            if app.board[row][col] == True:
                canvas.create_oval(x0 + r, y0 + r, x1 - r, y1 - r, fill="green")
            else:
                canvas.create_oval(x0 + r, y0 + r, x1 - r, y1 - r, fill="gray")


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
    # IMAGE FROM https://aminoapps.com/c/clash-royale/page/blog/first-battle-in-royale-arena/4G68_NWtYuN5qabloNDN1o8NW7X7KqwWkJ
    canvas.create_image(
        app.newWidth // 2,
        app.newHeight // 2 + 90,
        image=ImageTk.PhotoImage(app.arenaImage),
    )


def drawRecap(app, canvas):
    if app.winner == "player":
        canvas.create_text(
            app.width // 2,
            app.height // 2,
            text="Your deck won!",
            font="Arial 36 bold",
        )
    else:
        canvas.create_text(
            app.width // 2,
            app.height // 2,
            text="Your deck lost :(",
            font="Arial 36 bold",
        )


def drawAllPaths(app, canvas):
    for cardName in app.playerCards:
        route = app.playerCards[cardName].route
        for coords in route:
            (x0, y0, x1, y1) = getCellBounds(app, coords[0], coords[1])
            r = 7
            canvas.create_oval(x0 + r, y0 + r, x1 - r, y1 - r, fill="blue")
    for cardName in app.enemyCards:
        route = app.enemyCards[cardName].route
        for coords in route:
            (x0, y0, x1, y1) = getCellBounds(app, coords[0], coords[1])
            canvas.create_oval(x0 + r, y0 + r, x1 - r, y1 - r, fill="red")


def drawTowerHealths(app, canvas):
    for towerTeam in [app.playerTowers, app.enemyTowers]:
        for tower in towerTeam:
            changeY = -4 if tower.team == "enemy" else +3
            if type(tower) == LeftPrincessTower:
                (x0, y0, _, _) = getCellBounds(
                    app, tower.target[0] + changeY, tower.target[1] - 1
                )
                (_, _, x1, y1) = getCellBounds(
                    app, tower.target[0] + changeY, tower.target[1] + 2
                )
                canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                canvas.create_rectangle(
                    x0,
                    y0,
                    x0 + ((x1 - x0) * (tower.health / 2534)),
                    y1,
                    fill="red",
                )
                canvas.create_text(
                    average(x0, x1),
                    average(y0, y1),
                    text=f"{tower.health} HP",
                    font="Arial 16 bold",
                    fill="white",
                )
            elif type(tower) == RightPrincessTower:
                (x0, y0, _, _) = getCellBounds(
                    app, tower.target[0] + changeY, tower.target[1] - 2
                )
                (_, _, x1, y1) = getCellBounds(
                    app, tower.target[0] + changeY, tower.target[1] + 1
                )
                canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                canvas.create_rectangle(
                    x0,
                    y0,
                    x0 + ((x1 - x0) * (tower.health / 2534)),
                    y1,
                    fill="red",
                )
                canvas.create_text(
                    average(x0, x1),
                    average(y0, y1),
                    text=f"{tower.health} HP",
                    font="Arial 16 bold",
                    fill="white",
                )
            elif type(tower) == KingTower:
                changeY = -5 if tower.team == "enemy" else +3
                (x0, y0, _, _) = getCellBounds(
                    app, tower.target[0] + changeY, tower.target[1] - 2
                )
                (_, _, x1, y1) = getCellBounds(
                    app, tower.target[0] + changeY, tower.target[1] + 3
                )
                canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                canvas.create_rectangle(
                    x0,
                    y0,
                    x0 + ((x1 - x0) * (tower.health / 3568)),
                    y1,
                    fill="red",
                )
                canvas.create_text(
                    average(x0, x1),
                    average(y0, y1),
                    text=f"{tower.health} HP",
                    font="Arial 16 bold",
                    fill="white",
                )


runApp(width=1400, height=1000)
