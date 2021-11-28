from Card import *

# from DeckInfo import *
from NewAlgo import *
from cmu_112_graphics import *
from cardsInfo import *
from allCards import *

# From
# https://stackoverflow.com/questions/42671252/
# python-pillow-valueerror-decompressed-data-too-large
# Used to remove limitation on max data to cache for photos
from PIL import PngImagePlugin

LARGE_ENOUGH_NUMBER = 100
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (1024 ** 2)

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
    # Turn deck into 2d list
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
    app.matchups = [metaDeck1, metaDeck2, metaDeck3, metaDeck4]
    allAnalysis = dict()
    deck = app.prepDeck
    app.matchup1 = Matchup(deck, metaDeck1)
    app.matchup2 = Matchup(deck, metaDeck2)
    app.matchup3 = Matchup(deck, metaDeck3)
    app.matchup4 = Matchup(deck, metaDeck4)
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


def timerFired(app):
    pass


def keyPressed(app, event):
    pass


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
    elif app.state == "analysis":
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
        # counterName = app.analysis[key].counters[0]
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


def drawAnalysisPopup(app, canvas):
    drawExitButton(app, canvas)
    drawMatchupDecks(app, canvas)
    drawCounters(app, canvas)
    drawSuggestions(app, canvas)
    drawMyDeck(app, canvas)


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
        # canvas.create_text(
        #     app.width - 100,
        #     100,
        #     text=f"{app.analysis}",
        #     font="Arial 10 bold",
        #     anchor=NE,
        #     fill="red",
        # )


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


runApp(width=1400, height=1000)
