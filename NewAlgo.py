from Card import *
from DeckInfo import *
# from Main import *
from cardsInfo import *
from allCards import *

swarm = ['Minion Horde', 'Goblin Gang', 'Skeleton Army', 'Goblins',
         'Spear Goblins', 'Bats', 'Skeletons']

singleTargetdps = ['Three Musketeers', 'Elite Barbarians','Sparky', 
        'Cannon Cart', 'Wizard','Golden Knight', 'Hunter', 'Lumberjack', 
        'Inferno Dragon','Magic Archer', 'Musketeer', 'Mini P.E.K.K.A', 
        'Flying Machine','Bandit', 'Royal Ghost', 'Fisherman',
        'Mega Minion', 'Dart Goblin', 'X-Bow']

defensiveTowers = ['Cannon', 'Inferno Tower', 'Bomb Tower', 'Tesla']

splash = ['Archer Queen', 'Witch', 'Executioner', 'Electro Dragon', 'Wizard', 
          'Skeleton Dragons', 'Baby Dragon', 'Dark Prince', 'Hunter', 
          'Magic Archer', 'Valkyrie', 'Zappies', 'Firecracker', 'Ice Wizard', 
          'Princess', 'Bomber', 'Ice Golem', 'Fire Spirit', 'Electro Spirit', 
          'Bomb Tower', 'Royal Delivery']

heavySwarm = ['Archers', 'Minions', 'Guards', 'Royal Recruits', 'Barbarians']

buildingRush = ['Balloon', 'Ram Rider', 'Royal Hogs', 'Hog Rider',
                'Battle Ram', 'Miner', 'Elixir Golem', 'Wall Breakers',
                'Mortar', 'Goblin Drill', 'Goblin Barrel', 
                'Skeleton Barrel', 'Graveyard']

smallSpell = ['Arrows', 'Tornado', 'Earthquake', 'Zap', 'Giant Snowball', 
            'Barbarian Barrel', 'The Log', 'Poison']

bigSpell = ['Lightning', 'Rocket', 'Fireball']

tank = ['Rascals', 'Giant', 'Mega Knight', 'Bowler', 'Knight', 'P.E.K.K.A',
        'Giant Skeleton', 'Skeleton King', 'Prince',]

buildingAttackTank = ['Golem', 'Electro Giant', 'Lava Hound', 
                    'Royal Giant', 'Goblin Giant']

stunsAndDistractions = ['Freeze', 'Zap', 'Ice Spirit', 
                    'Electro Wizard', 'Tornado']

swarmHelperSpells = ['Rage', 'Freeze', 'Mirror', 'Clone']

spawnerBuildings = ['Barbarian Hut', 'Goblin Cage', 'Tombstone', 'Furnace',
                    'Goblin Hut']

other = ['Battle Healer', 'Elixir Collector', 'Heal Spirit', 
        'Mother Witch', 'Night Witch']

allCategories = (swarm + singleTargetdps + splash + heavySwarm + buildingRush + 
                smallSpell + bigSpell + tank + 
                buildingAttackTank + stunsAndDistractions + swarmHelperSpells + 
                spawnerBuildings + other)

# for card in cardsInfo:
#     if card not in bigList:
#         print(card)

def getAllCounters(cardName):
    if cardName in swarm:
        counters = smallSpell + splash + stunsAndDistractions + swarm
        return counters
    if cardName in splash:
        counters = singleTargetdps + bigSpell + tank + defensiveTowers
        return counters
    if cardName in singleTargetdps:
        counters = (swarm + bigSpell + heavySwarm + 
                    tank + singleTargetdps + defensiveTowers)
        return counters
    if cardName in heavySwarm:
        counters = (bigSpell + splash + singleTargetdps + heavySwarm + 
                    defensiveTowers)
        return counters
    if cardName in buildingRush:
        counters = (swarm + singleTargetdps + spawnerBuildings + defensiveTowers)
        return counters
    if cardName in tank:
        counters = swarm + singleTargetdps + heavySwarm + defensiveTowers
        return counters
    if cardName in buildingAttackTank:
        counters = (heavySwarm + swarm + singleTargetdps 
                    + spawnerBuildings + defensiveTowers)
        return counters
    if cardName in spawnerBuildings:
        counters = bigSpell + defensiveTowers
        return counters
    if cardName in defensiveTowers:
        counters = bigSpell + swarm
        return counters
    else:
        return []

def getAllSynergies(cardName):
    if cardName in swarm:
        synergies = swarmHelperSpells + smallSpell
        return synergies
    if cardName in splash:
        synergies = tank + buildingRush + singleTargetdps + buildingAttackTank
        return synergies
    if cardName in singleTargetdps:
        synergies = (splash + smallSpell + buildingRush + 
                    tank + buildingAttackTank)
        return synergies
    if cardName in heavySwarm:
        synergies = bigSpell
        return synergies
    if cardName in buildingRush:
        synergies = (splash + smallSpell + bigSpell + tank + 
                    singleTargetdps + stunsAndDistractions)
        return synergies
    if cardName in tank:
        synergies = singleTargetdps + splash + smallSpell
        return synergies
    if cardName in buildingAttackTank:
        synergies = (splash + smallSpell + bigSpell + 
                    singleTargetdps + stunsAndDistractions)
        return synergies
    if cardName in spawnerBuildings:
        synergies = bigSpell
        return synergies
    if cardName in defensiveTowers:
        synergies = allCategories
        return synergies
    else:
        return []

class Graph(object):
    def __init__(self):
        self.graph = {}
    def addEdge(self, node, neighbor, weight):
        if node in self.graph:
            self.graph[node][neighbor] = weight
        else:
            self.graph[node] = {neighbor : weight}
    def __repr__(self):
        return repr(self.graph)

def addCounterWeightings(cardCountersGraph, cardName, allCounters):
    for counter in allCounters:
        if counter != cardName:
            # Add weight of 10 to signify hard counter
            cardCountersGraph.addEdge(cardName, counter, 10)

def addSynergyWeightings(cardSynergiesGraph, cardName, allSynergies):
    for synergy in allSynergies:
        if synergy != cardName:
            # Add with weight of 1 to signify nice synergy
            cardSynergiesGraph.addEdge(cardName, synergy, 1)

deck = ['Cannon', 'Fireball', 'Skeletons', 'Ice Golem', 
			'The Log', 'Hog Rider', 'Musketeer', 'Ice Spirit']

# counterDeck = ['Barbarian Barrel', 'Bats', 'Giant Snowball', 'Inferno Tower',
#                'Miner', 'Poison', 'Prince', 'Spear Goblins']

matchup = ['Balloon', 'Baby Dragon', 'Giant Skeleton', 'Miner', 'Goblin Gang',
                'Tesla','Zap', 'Tornado']

# metaDeck1 = ['Barbarian Barrel','Fireball','Flying Machine', 'Goblin Cage',
#             'Golden Knight', 'Royal Hogs', 'Royal Recruits', 'Zappies']
# metaDeck2 = ['Balloon','Fireball','Guards','Lava Hound','Mega Minion',
#             'Skeleton Dragons','Tombstone','Zap']
# metaDeck3 = 
# metaDeck4 = 
# metaDeck5 = 
# metaDeck6 = 

# Gets counters for a single card
def getCountersForCard(card):
    counters = Graph()
    allCounters = getAllCounters(card)
    addCounterWeightings(counters, card, allCounters)
    return counters.graph

# Gets counters and synergies for 2 input decks
def getCountersAndSynergiesDicts(deck, matchup):
    deckCounters = Graph()
    deckSynergies = Graph()
    for key in deck:
        allCounters = getAllCounters(key)
        allSynergies = getAllSynergies(key)
        addCounterWeightings(deckCounters, key, allCounters)
        addSynergyWeightings(deckSynergies, key, allSynergies)

    matchupCounters = Graph()
    matchupSynergies = Graph()
    for key in matchup:
        allCounters = getAllCounters(key)
        allSynergies = getAllSynergies(key)
        addCounterWeightings(matchupCounters, key, allCounters)
        addSynergyWeightings(matchupSynergies, key, allSynergies)
    return deckCounters, deckSynergies, matchupCounters, matchupSynergies

# Check if a card that counters a deck gets countered by a different card in the deck
def notCounteredByAnotherCardInDeck(counter, deck):
    countersForCard = getCountersForCard(counter)
    if len(countersForCard) < 1:
        return True
    countersForCard = countersForCard[counter]
    # print('Counters for ', counter, ":", countersForCard)
    for key in countersForCard:
        if key in deck:
            print(key, "is in the deck so", counter, "is counter-countered!")
            return False
    return True

# Gets which cards in the matchup counters the deck
def getMatchupCounters(deck, matchup):
    deckCounters = getCountersAndSynergiesDicts(deck, matchup)[0]
    counterCount = {}
    counteredCards = {}
    deckCounters = deckCounters.graph
    for key in deckCounters:
        for counter in deckCounters[key]:
            if counter in matchup:
                if counter not in counterCount:
                    counterCount[counter] = 0
                # if notCounteredByAnotherCardInDeck(counter, deck):
                counterCount[counter] += 1
                if counter not in counteredCards:
                    counteredCards[counter] = set()
                counteredCards[counter].add(key)
    return counterCount, counteredCards

# Change this to get the most countered card in your deck
def getBestCounterAgainstDeckFromMatchup(deck, matchup):
    counters = getMatchupCounters(deck, matchup)
    countersCount = counters[0]
    bestDeckCounter = None
    bestNum = None
    for key in countersCount:
        if bestNum == None or countersCount[key] > bestNum:
            bestDeckCounter = key
            bestNum = countersCount[key]
    
def getMostCounteredCardFromDeckAgainstMatchup(deck, matchup):
    counters = getMatchupCounters(deck, matchup)
    counters = counters[1]
    counterCounts = {}
    counteredDict = {}
    for key in counters:
        for deckCard in counters[key]:
            if deckCard not in counteredDict:
                counteredDict[deckCard] = set()
                counterCounts[deckCard] = 0
            counteredDict[deckCard].add(key)
            counterCounts[deckCard] += 1
    return counteredDict, counterCounts

def getCardSwapReccomendations(deck, matchup):
    bestCounter = getBestCounterAgainstDeckFromMatchup(deck, matchup)
    return

print(getMatchupCounters(deck, matchup)[1])
# print()
# print(getMatchupCounters(deck, matchup)[1])

# print(getCardSwapReccomendations(deck, matchup))