from DeckInfo import *
import clashroyale
from dotenv import load_dotenv
from cmu_112_graphics import *
import os
from cardsInfo import *

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