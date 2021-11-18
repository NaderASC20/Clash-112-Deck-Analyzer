from Card import *
from DeckInfo import *
from cmu_112_graphics import *

from PIL import PngImagePlugin
LARGE_ENOUGH_NUMBER = 100
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (1024**2)

# Testing funcitonality with a sample deck
testDeck = [Card(cardsInfo['Cannon']), Card(cardsInfo['Fireball']), 
			Card(cardsInfo['Skeletons']), Card(cardsInfo['Ice Golem']), 
			Card(cardsInfo['The Log']), Card(cardsInfo['Hog Rider']),
			Card(cardsInfo['Musketeer']), Card(cardsInfo['Ice Spirit'])]

testDeckAnalysis = DeckInfo(testDeck)

# Model
################################################
def initCardImages(app):
	result = [([0]*app.listCols) for row in range(app.listRows)]
	index = 0
	for row in range(app.listRows):
		for col in range(app.listCols):
				tempImage = app.loadImage(f'card-images/{allCards[index].name}.png')
				scaledImage = app.scaleImage(tempImage, 1/4)
				result[row][col] = scaledImage
				index += 1
	return result


def appStarted(app):
	app.deck = testDeck
	app.deckMargin = 500
	app.deckHeight = app.height//5
	app.margin = 20
	app.deckRows = 2
	app.deckCols = 4
	app.listRows = 5
	app.listCols = 21
	app.cardImagesMatrix = initCardImages(app)
	# app.cardMatrix = initCardMatrix(app)
# Controller
################################################

def timerFired(app):
	pass


def keyPressed(app, event):
	pass


def mousePressed(app, event):
	pass


def mouseReleased(app, event):
	pass

# View
################################################

def redrawAll(app, canvas):
	drawDeckContainer(app, canvas)
	drawDeckImages(app, canvas)
	# drawButton(app, canvas)
	# drawCardsList(app, canvas)

def drawDeckContainer(app, canvas):
	for row in range(app.deckRows):
		for col in range(app.deckCols):
			(x0, y0, x1, y1) = getDeckContainerBounds(app, row, col)
			canvas.create_rectangle(x0, y0, x1, y1, fill='gray')


def getDeckContainerBounds(app, row, col):
	gridWidth = app.width - (2 * app.deckMargin)
	gridHeight = app.deckHeight
	cellWidth = gridWidth // app.deckCols
	cellHeight = gridHeight // app.deckRows
	gapX  = 5
	gapY = 5
	x0 = app.deckMargin + (cellWidth * col) + gapX
	y0 = app.margin + (cellHeight * row) + gapY
	x1 = app.deckMargin + (cellWidth * (col + 1)) - gapX
	y1 = app.margin + (cellHeight * (row + 1)) - gapY
	return (x0, y0, x1, y1)


def getDeckListBounds(app, row, col):
	gridWidth = app.width - (2 * app.margin)
	gridHeight = app.height - app.deckHeight - app.margin
	cellWidth = gridWidth // app.listCols
	cellHeight = gridHeight // app.listRows
	x0 = app.margin + (cellWidth * col) + 3
	y0 = app.margin + app.deckHeight + (cellHeight * row) + 3
	x1 = app.margin + (cellWidth * (col + 1)) - 3
	y1 = app.margin +app.deckHeight + (cellHeight * (row + 1)) - 3
	return (x0, y0, x1, y1)

def drawDeckImages(app, canvas):
	for row in range(app.listRows):
		for col in range(app.listCols):
			(x0, y0, x1, y1) = getDeckListBounds(app, row, col)
			x, y = (x0 + x1) // 2, (y0 + y1) // 2
			canvas.create_image(x, y, image=ImageTk.PhotoImage(app.cardImagesMatrix[row][col]))
			canvas.create_rectangle(x0, y0, x1, y1, fill='red')

runApp(width=1400, height=1000)

