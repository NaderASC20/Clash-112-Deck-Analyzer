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
	result = [([0]*app.cardArrayCols) for row in range(app.cardArrayRows)]
	index = 0
	for row in range(app.cardArrayRows):
		for col in range(app.cardArrayCols):
				if index >= len(allCards): break
				tempImage = app.loadImage(f'card-images/{allCards[index].name}.png')
				scaledImage = app.scaleImage(tempImage, 1/4)
				lessScaledImage = app.scaleImage(tempImage, 1/3)
				result[row][col] = {'name': allCards[index].name, 
									'image': scaledImage, 'big-image': lessScaledImage}
				index += 1
	return result

def appStarted(app):
	# Matrix data
	app.deckRows = 2
	app.deckCols = 4
	app.cardArrayRows = 6
	app.cardArrayCols = 18
	app.currDeckRow = 0
	app.currDeckCol = 0
	# Positions and Margins
	app.buttonY = 300
	app.buttonX = (app.width ) // 2
	app.deckMargin = 500
	app.deckHeight = app.height//4.3
	app.margin = 40
	app.inputDeckWrapperPadding = 45
	app.deck = [([0] * app.deckCols) for row in range(app.deckRows)]
	app.cardImagesMatrix = initCardImages(app)
	app.isDeckFull = False
	app.analysis = None
	# app.cardMatrix = initCardMatrix(app)

def analyzeDeckHandler(app):
	prepDeck = []
	for row in range(app.deckRows):
		for col in range(app.deckCols):
			name = app.deck[row][col]['name']
			if 'elixir' not in cardsInfo[name]:
				return name
			cardObject = Card(cardsInfo[name])
			prepDeck.append(cardObject)
	analysis = DeckInfo(prepDeck)
	print(analysis)
	app.analysis = analysis

# Controller
################################################
def timerFired(app):
	pass

def keyPressed(app, event):
	pass

def mousePressed(app, event):
	(x0, y0, x1, y1) = getButtonBounds(app)
	if ((app.isDeckFull) and 
		(x0 <= event.x <= x1) and 
		(y0 <= event.y <= y1)):
		response = analyzeDeckHandler(app)
		if response != None:
			print(f"no info avaiable for {response}")
		return

	for row in range(app.cardArrayRows):
		for col in range(app.cardArrayCols):
			(x0, y0, x1, y1) = getDeckListBounds(app, row, col)
			if ((x0 <= event.x <= x1) and 
				(y0 <= event.y <= y1) and 
				(app.isDeckFull == False) and
				(cardIsNotDuplicate(app, app.cardImagesMatrix[row][col]))):
				image = app.cardImagesMatrix[row][col]
				app.deck[app.currDeckRow][app.currDeckCol] = image
				if ((app.currDeckRow == app.deckRows - 1) and 
					(app.currDeckCol == app.deckCols - 1)):
					app.isDeckFull = True
				elif app.currDeckCol + 1 < app.deckCols:
					app.currDeckCol += 1
				else:
					app.currDeckRow += 1
					app.currDeckCol = 0

def cardIsNotDuplicate(app, card):
	for row in range(app.deckRows):
		if card in app.deck[row]: return False
	return True

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
	gridHeight = app.height - app.deckHeight - 3*app.margin
	cellWidth = gridWidth // app.cardArrayCols
	cellHeight = gridHeight // app.cardArrayRows
	x0 = app.margin + (cellWidth * col)
	y0 = app.margin + app.deckHeight + (cellHeight * row)
	x1 = app.margin + (cellWidth * (col + 1))
	y1 = app.margin + app.deckHeight + (cellHeight * (row + 1))
	shiftY = 75
	return (x0, y0 + shiftY, x1, y1 + shiftY)

# View
################################################
def redrawAll(app, canvas):
	drawInputDeckContainer(app, canvas)
	drawCardsMatrixImages(app, canvas)
	drawInputDeck(app, canvas)
	drawAnalyzeButton(app, canvas)
	if app.analysis != None:
		canvas.create_text(20, 100, text=f'{app.analysis}', font='Arial 10 bold', anchor=NW)
	# drawButton(app, canvas)
	# drawCardsList(app, canvas)

def drawAnalyzeButton(app, canvas):
	if app.isDeckFull:
		(x0, y0, x1, y1) = getButtonBounds(app)
		canvas.create_rectangle(x0, y0, x1, y1, fill='green', width=2)
		cx, cy = (x0+x1)//2, (y0+y1)//2
		canvas.create_text(cx,cy, text="Analyze!", fill='white', font='Arial 24 bold')

def getButtonBounds(app):
		length = 300
		height = 40
		(x0, y0, x1, y1) = (app.buttonX - length//2, app.buttonY - height//2, 
							app.buttonX + length//2, app.buttonY + height//2)
		return (x0, y0, x1, y1)

def drawInputDeckContainer(app, canvas):
	(x0A, y0A, x_1, y_1) = getDeckContainerBounds(app, 0, 0)
	(x_0, y_0, x1A, y1A) = getDeckContainerBounds(app, app.deckRows-1, app.deckCols-1)
	canvas.create_rectangle(x0A - app.inputDeckWrapperPadding, y0A - app.inputDeckWrapperPadding//3, 
							x1A + app.inputDeckWrapperPadding, y1A + app.inputDeckWrapperPadding*1.5)
	for row in range(app.deckRows):
		for col in range(app.deckCols):
			(x0, y0, x1, y1) = getDeckContainerBounds(app, row, col)
			if ((row, col) == (app.currDeckRow, app.currDeckCol) and 
				(app.isDeckFull == False)):
				canvas.create_rectangle(x0, y0, x1, y1, fill='#CDCDCD', 
										outline='red', width=5)
				canvas.create_text(app.width//2, app.buttonY, 
								text='Click on a card below!', font='Arial 24 bold', fill='green')
			elif app.deck[row][col] == 0:
				canvas.create_rectangle(x0, y0, x1, y1, fill='#CDCDCD', width=2)

def drawInputDeck(app, canvas):
	for row in range(app.deckRows):
		for col in range(app.deckCols):
			if app.deck[row][col] != 0:
				(x0, y0, x1, y1) = getDeckContainerBounds(app, row, col)
				selectedCardImage = app.deck[row][col]['big-image']
				x,y = (x0+x1)//2, (y0+y1)//2
				canvas.create_image(x,y, image=ImageTk.PhotoImage(selectedCardImage))

def drawCardsMatrixImages(app, canvas):
	for row in range(app.cardArrayRows):
		for col in range(app.cardArrayCols):
			(x0, y0, x1, y1) = getDeckListBounds(app, row, col)
			(x0, y0, x1, y1) = (x0 + 5, y0 + 5, x1 - 5, y1 - 5)
			x, y = (x0 + x1) // 2, (y0 + y1) // 2
			if app.cardImagesMatrix[row][col] != 0:
				# canvas.create_rectangle(x0, y0, x1, y1, fill='green')
				# canvas.create_rectangle(x0, y0, x1, y1, fill='red')
				canvas.create_text(x, y, text='no \nimages \nfolder', font='Arial 8 bold')
				cachedImage = app.cardImagesMatrix[row][col]['image']
				canvas.create_image(x, y, image=ImageTk.PhotoImage(cachedImage))

runApp(width=1400, height=1000)