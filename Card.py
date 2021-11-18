from DeckInfo import *
import clashroyale
from dotenv import load_dotenv
from cmu_112_graphics import *
import os

# Sets up clash royale api
load_dotenv()
officialClient = clashroyale.official_api.Client(os.getenv('CLASH_TOKEN'))
royaleClient = clashroyale.royaleapi.Client(os.getenv('CLASH_TOKEN'))

# Gets all cards and maps them by card name in cardInfo dict
allCards = officialClient.get_all_cards()
cardsInfo = dict()
for card in range(len(allCards)):
	cardName = allCards[card].name
	info = officialClient.get_card_info(cardName)
	if info != None:
		cardsInfo[cardName] = dict(officialClient.get_card_info(cardName))
	else:
		cardsInfo[cardName] = {'name': cardName, 'alert': 'NO INFO FROM ROAYLE API'}

for i in range(len(allCards)):
	cardName = allCards[i].name
	cardsInfo[cardName]['imageURL'] = allCards[i]['iconUrls']['medium']

# Card class which takes card dict from api results
class Card(object):
	def __init__(self, apiCard):
		self.key = apiCard['key']
		self.name = apiCard['name']
		self.elixir = apiCard['elixir']
		self.type = apiCard['type']
		self.rarity = apiCard['rarity']
		self.arena = apiCard['arena']
		self.description = apiCard['description']
		self.imageURL = apiCard['imageURL']

	def __repr__(self):
		return (f"<{self.name}, " 
				f"{self.elixir} elixir, {self.type},"
				f"{self.rarity}, arena {self.arena}, {self.imageURL}>")
