# Cards separated by win condition, air troops, ground cards, and spell cards
winCards = {'Hog Rider', 'Goblin Giant', 'Ram Rider', 'Skeleton Barrel', 
				'Battle Ram', 'Goblin Barrel', 'Electro Giant', 'Graveyard',
				'Royal Giant', 'X-Bow', 'Balloon', 'Sparky', 'Three Musketeers',
				'Giant', 'Golem', 'Goblin Drill', 'Elixir Golem', 'Mega Knight',
				'Lava Hound', 'P.E.K.K.A', 'Royal Hogs', 'Mortar', 'Miner', 
				'Wall Breakers'}

airCards = {'Fire Spirit', 'Spear Goblins', 'Bats', 'Archers', 'Minions',
				'Goblin Gang', 'Firecracker', 'Skeleton Dragons', 'Tesla',
				'Minion Horde', 'Mega Minion', 'Rascals', 'Dart Goblin',
				'Musketeer', 'Flying Machine', 'Zappies', 'Wizard', 'Inferno Tower',
				'Three Musketeers', 'Baby Dragon', 'Witch', 'Hunter', 'Executioner',
				'Princess', 'Ice Wizard', 'Magic Archer', 'Inferno Dragon', 'Electro Wizrd',
				'Night Witch', 'Archer Queen', 'Balloon', 'Fireball', 'Tordado',
				'Rocket', 'Snowball', 'Arrows', 'Zap' }

groundCards = {'Bandit', 'Giant Skeleton', 'Bomber', 'Barbarians',
					'Ice Golem', 'Valkyrie', 'Bomb Tower', 'Goblins', 'Mini P.E.K.K.A',
					'Cannon', 'Skeleton Army', 'Fisherman', 'Royal Ghost',
					'Battle Healer', 'Barbarian Hut', 'Skeletons', 'Tombstone',
					'Bowler', 'Dark Prince', 'Cannon Cart', 'Rascals', 'Goblin Gang',
					'Lumberjack', 'Prince', 'Royal Recruits', 'Guards', 'Knight',
					'Night Witch', 'Elite Barbarians'}

spellCards = {'Earthquake', 'Zap', 'Arrows', 'Royal Delivery', 'Rage',
				   'Barbarian Barrel', 'Fireball', 'Clone', 'Freeze', 'The Log',
				   'Rocket', 'Poison', 'Mirror', 'Lightning', 'Torando', 'Snowball'}


from Card import *
class DeckInfo:
	def __init__(self, deck):
		self.deck = deck
		self.good = []
		self.bad = []
		self.cardTypesDict = self.getCardTypeCount()
		self.averageElixir = self.getAverageElixir()
		self.startScore = 100
		self.deckScore = self.getDeckScore()

	# Gets dictionary containing deck separated by type
	def getCardTypeCount(self):
		cardTypes = dict()
		for card in self.deck:
			name = card.name
			if name in winCards:
				winConditionsList = cardTypes.get('win condition', [])
				winConditionsList.append(name)
				cardTypes['win condition'] = winConditionsList
			if name in airCards:
				airTroopsList = cardTypes.get('air troop', [])
				airTroopsList.append(name)
				cardTypes['air troop'] = airTroopsList
			if name in groundCards:
				groundCardsList = cardTypes.get('ground troop', [])
				groundCardsList.append(name)
				cardTypes['ground troop'] = groundCardsList
			if name in spellCards:
				spellCardsList = cardTypes.get('spell card', [])
				spellCardsList.append(name)
				cardTypes['spell card'] = spellCardsList

		return cardTypes

	# Analyzes minimum needed # of cards for each card type
	def analyzeTroopCounts(self):
		for key in self.cardTypesDict:
			troopList = self.cardTypesDict[key]
			if len(troopList) == 1:
				self.startScore -= 10
				self.bad.append(f"You're only {key} is {troopList[0]}! Consider adding another {key}.")
			elif len(troopList) == 0:
				self.startScore -= 10
				self.bad.append(f"You don't have any {key}s in your deck! Consider adding 2 {key}s.")
			else:
				self.good.append(f"You have 2 {key}s. Great!")

	# Gets average elixir of a deck
	def getAverageElixir(self):
		totalElixir = 0
		deckSize = 8
		for card in self.deck:
			totalElixir += card.elixir
		return round(totalElixir / deckSize, 1)

	# Calls all analyze methods and returns score
	def getDeckScore(self):
		self.analyzeElixir()
		self.analyzeTroopCounts()
		return self.startScore

	# Analyzes average elixir of this deck
	def analyzeElixir(self):
		if self.averageElixir <= 3.0:
			self.startScore -= 0
			self.good.append(f"This deck is very easy to cycle with an average elixir of only {self.averageElixir}.")
		elif 3.1 <= self.averageElixir <= 4.2:
			self.startScore -= 5
			self.good.append(f"This deck is a medium-high elixir deck with an average exlixir of {self.averageElixir}.")
		elif self.averageElixir >= 4.3:
			self.startScore -= 10
			self.bad.append(f"This deck has a very high elixir cost at an average exlixir of {self.averageElixir}.")
			self.suggestions.append(f"This deck has a high elixir cost. Consider replacing some high elixir cards with ones that cost less elixir.")

	# Puts results in a readable string form
	def __repr__(self):
		analysis = ''''''

		deckList = [card.name for card in self.deck]
		deck = f"Deck: {deckList}\n"

		good = '''\nGood:\n'''
		for comment in self.good:
			good += f"{comment}\n"

		bad = '''\nBad:\n'''
		for comment in self.bad:
			bad += f"{comment}\n"

		analysis += deck
		analysis += good
		analysis += bad

		analysis += f"\nThe total score for this deck is {self.deckScore}!"
		return analysis

