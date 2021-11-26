from Card import *
from DeckInfo import *
import random

# from Main import *
from cardsInfo import *
from allCards import *

swarm = [
    "Minion Horde",
    "Goblin Gang",
    "Skeleton Army",
    "Goblins",
    "Spear Goblins",
    "Bats",
    "Skeletons",
]

singleTargetdps = [
    "Three Musketeers",
    "Elite Barbarians",
    "Sparky",
    "Cannon Cart",
    "Wizard",
    "Golden Knight",
    "Hunter",
    "Lumberjack",
    "Inferno Dragon",
    "Magic Archer",
    "Musketeer",
    "Mini P.E.K.K.A",
    "Flying Machine",
    "Bandit",
    "Royal Ghost",
    "Fisherman",
    "Mega Minion",
    "Dart Goblin",
    "X-Bow",
]

defensiveTowers = ["Cannon", "Inferno Tower", "Bomb Tower", "Tesla"]

splash = [
    "Archer Queen",
    "Witch",
    "Executioner",
    "Electro Dragon",
    "Wizard",
    "Skeleton Dragons",
    "Baby Dragon",
    "Dark Prince",
    "Hunter",
    "Magic Archer",
    "Valkyrie",
    "Zappies",
    "Firecracker",
    "Ice Wizard",
    "Princess",
    "Bomber",
    "Ice Golem",
    "Fire Spirit",
    "Electro Spirit",
    "Bomb Tower",
    "Royal Delivery",
]

heavySwarm = ["Archers", "Minions", "Guards", "Royal Recruits", "Barbarians"]

buildingRush = [
    "Balloon",
    "Ram Rider",
    "Royal Hogs",
    "Hog Rider",
    "Battle Ram",
    "Miner",
    "Elixir Golem",
    "Wall Breakers",
    "Mortar",
    "Goblin Drill",
    "Goblin Barrel",
    "Skeleton Barrel",
    "Graveyard",
]

smallSpell = [
    "Arrows",
    "Tornado",
    "Earthquake",
    "Zap",
    "Giant Snowball",
    "Barbarian Barrel",
    "The Log",
    "Poison",
]

bigSpell = ["Lightning", "Rocket", "Fireball"]

tank = [
    "Rascals",
    "Giant",
    "Mega Knight",
    "Bowler",
    "Knight",
    "P.E.K.K.A",
    "Giant Skeleton",
    "Skeleton King",
    "Prince",
]

buildingAttackTank = [
    "Golem",
    "Electro Giant",
    "Lava Hound",
    "Royal Giant",
    "Goblin Giant",
]

stunsAndDistractions = [
    "Freeze",
    "Zap",
    "Ice Spirit",
    "Electro Wizard",
    "Tornado",
]

swarmHelperSpells = ["Rage", "Freeze", "Mirror", "Clone"]

spawnerBuildings = [
    "Barbarian Hut",
    "Goblin Cage",
    "Tombstone",
    "Furnace",
    "Goblin Hut",
]

other = [
    "Battle Healer",
    "Elixir Collector",
    "Heal Spirit",
    "Mother Witch",
    "Night Witch",
]

allCategories = (
    swarm
    + singleTargetdps
    + splash
    + heavySwarm
    + buildingRush
    + smallSpell
    + bigSpell
    + tank
    + buildingAttackTank
    + stunsAndDistractions
    + swarmHelperSpells
    + spawnerBuildings
    + other
)

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
        counters = (
            swarm
            + bigSpell
            + heavySwarm
            + tank
            + singleTargetdps
            + defensiveTowers
        )
        return counters
    if cardName in heavySwarm:
        counters = (
            bigSpell + splash + singleTargetdps + heavySwarm + defensiveTowers
        )
        return counters
    if cardName in buildingRush:
        counters = swarm + singleTargetdps + spawnerBuildings + defensiveTowers
        return counters
    if cardName in tank:
        counters = swarm + singleTargetdps + heavySwarm + defensiveTowers
        return counters
    if cardName in buildingAttackTank:
        counters = (
            heavySwarm
            + swarm
            + singleTargetdps
            + spawnerBuildings
            + defensiveTowers
        )
        return counters
    if cardName in spawnerBuildings:
        counters = bigSpell + defensiveTowers
        return counters
    if cardName in defensiveTowers:
        counters = bigSpell + swarm
        return counters
    if (
        cardName in stunsAndDistractions
        or cardName in swarmHelperSpells
        or cardName in other
        or cardName in smallSpell
        or cardName in bigSpell
    ):
        counters = stunsAndDistractions + smallSpell
        return counters
    else:
        return []


# need small spell, big spell


def getAllSynergies(cardName):
    if cardName in swarm:
        synergies = swarmHelperSpells + smallSpell
        return synergies
    if cardName in splash:
        synergies = tank + buildingRush + buildingAttackTank
        return synergies
    if cardName in singleTargetdps:
        synergies = (
            splash + smallSpell + buildingRush + tank + buildingAttackTank
        )
        return synergies
    if cardName in heavySwarm:
        synergies = bigSpell
        return synergies
    if cardName in buildingRush:
        synergies = (
            splash
            + smallSpell
            + bigSpell
            + tank
            + singleTargetdps
            + stunsAndDistractions
        )
        return synergies
    if cardName in tank:
        synergies = singleTargetdps + splash + smallSpell
        return synergies
    if cardName in buildingAttackTank:
        synergies = (
            splash
            + smallSpell
            + bigSpell
            + singleTargetdps
            + stunsAndDistractions
        )
        return synergies
    if cardName in spawnerBuildings:
        synergies = bigSpell
        return synergies
    if cardName in smallSpell or cardName in bigSpell:
        synergies = (
            singleTargetdps + defensiveTowers + stunsAndDistractions + other
        )
        return synergies
    if cardName in stunsAndDistractions:
        synergies = smallSpell + bigSpell
        return synergies
    if cardName in swarmHelperSpells:
        synergies = swarm
        return synergies
    if cardName in defensiveTowers or cardName in other:
        synergies = smallSpell + bigSpell
        return synergies
    else:
        return []
    # if cardName in defensiveTowers:
    #     synergies = allCategories
    #     return synergies
    # stuns and distractions, swam helper spells, defensive tower, other


class Graph(object):
    def __init__(self):
        self.graph = {}

    def addEdge(self, node, neighbor, weight):
        if node in self.graph:
            self.graph[node][neighbor] = weight
        else:
            self.graph[node] = {neighbor: weight}

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


# deck = [
#     "Cannon",
#     "Fireball",
#     "Skeletons",
#     "Ice Golem",
#     "The Log",
#     "Hog Rider",
#     "Musketeer",
#     "Ice Spirit",
# ]

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

# metaDeck1 = ['Barbarian Barrel','Fireball','Flying Machine', 'Goblin Cage',
#             'Golden Knight', 'Royal Hogs', 'Royal Recruits', 'Zappies']
# deck = [
#     "Balloon",
#     "Fireball",
#     "Guards",
#     "Lava Hound",
#     "Mega Minion",
#     "Skeleton Dragons",
#     "Tombstone",
#     "Zap",
# ]
deck = [
    "Barbarian Barrel",
    "Bats",
    "Giant Snowball",
    "Inferno Tower",
    "Miner",
    "Poison",
    "Prince",
    "Spear Goblins",
]
# metaDeck4 =
# metaDeck5 =
# metaDeck6 =

# Gets counters for a single card


def getCountersForCard(card):
    counters = Graph()
    allCounters = getAllCounters(card)
    addCounterWeightings(counters, card, allCounters)
    return counters.graph


# Gest synergies for a single card


def getSynergiesForCard(card):
    synergies = Graph()
    allSynergies = getAllSynergies(card)
    addSynergyWeightings(synergies, card, allSynergies)
    return synergies.graph


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


# Gets the card  in deck that is most countered by the matchup


def getMostCounteredCardFromDeckAgainstMatchup(deck, matchup):
    counters = getMatchupCounters(deck, matchup)[1]
    counterCounts = {}
    counteredDict = {}
    for key in counters:
        for deckCard in counters[key]:
            if deckCard not in counteredDict:
                counteredDict[deckCard] = set()
                counterCounts[deckCard] = 0
            counteredDict[deckCard].add(key)
            counterCounts[deckCard] += 1
    mostCountered = None
    bestCounterCount = None
    for key in counterCounts:
        if (mostCountered == None) or (counterCounts[key] > bestCounterCount):
            bestCounterCount = counterCounts[key]
            mostCountered = key
    return mostCountered, counteredDict[mostCountered]


# Finds synergy with most synergies with other cards in deck
# Ties broken randomly
# lower complexity algo than backtracking


def getCardSwapReccomendations(deck, matchup):
    bestCounter = getMostCounteredCardFromDeckAgainstMatchup(deck, matchup)[0]
    deckMinusCounter = copy.deepcopy(deck)
    deckMinusCounter.remove(bestCounter)
    synergiesDict = {}
    synergyCountDict = {}
    for card in deck:
        synergies = getAllSynergies(card)
        for synergy in synergies:
            if synergy not in deck and synergy != bestCounter:
                if synergy not in synergiesDict:
                    synergiesDict[synergy] = set()
                synergiesDict[synergy].add(card)
                if synergy not in synergyCountDict:
                    synergyCountDict[synergy] = 0
                synergyCountDict[synergy] += 1
    bestSynergy = None
    bestCount = None
    for key in synergyCountDict:
        if (bestSynergy == None) or (synergyCountDict[key] > bestCount):
            bestCount = synergyCountDict[key]
            bestSynergy = key
    print(synergyCountDict)
    return bestSynergy, synergiesDict[bestSynergy], synergyCountDict


cards = []
for card in cardsInfo:
    cards.append(card)
random.shuffle(cards)

# Checks if a certain card addition has counters >=4 cards in the matchup
# and has some synergies in the current deck
def foundBestCard(testCard, counterDeckSoFar, matchup):
    if len(counterDeckSoFar) < 5 and testCard in spellCards:
        return False
    matchup = set(matchup)
    countersCount = 0
    counters = []
    for card in matchup:
        countersOfCard = getAllCounters(card)
        if testCard in countersOfCard:
            countersCount += 1
            counters.append(card)
    synergiesCount = 0
    synergies = []
    for card in counterDeckSoFar:
        if card != testCard:
            synergiesOfCard = getAllSynergies(card)
            if testCard in synergiesOfCard:
                synergiesCount += 1
                synergies.append(card)
    if (countersCount >= 3) and (
        synergiesCount >= ((len(counterDeckSoFar) - 2) // 2) - 3
    ):
        return counters, synergies
    return False


# Makes sure a deck is not all spells
def isDiverseDeck(deck):
    spellCount = 0
    winCount = 0
    groundCount = 0
    for card in deck:
        if card in spellCards:
            spellCount += 1
        elif card in winCards:
            winCount += 1
        elif card in groundCards:
            groundCount += 1
    return (spellCount == 1 or spellCount == 2) and (
        winCount >= 1 or groundCount >= 1
    )


# Backtracking helper which finds the best counter deck to the input deck
def findBestCounterDeck(matchup):
    counterDeckSoFar = []
    return findBestCounterDeckHelper(counterDeckSoFar, matchup)


# Backtracking function to find a counter deck
def findBestCounterDeckHelper(counterDeckSoFar, matchup):
    print(counterDeckSoFar)
    if len(counterDeckSoFar) == 8 and isDiverseDeck(counterDeckSoFar):
        return counterDeckSoFar
    else:
        for card in cards:
            if (
                (len(counterDeckSoFar) <= 7)
                and (card not in counterDeckSoFar)
                and (foundBestCard(card, counterDeckSoFar, matchup))
            ):
                counterDeckSoFar.append(card)
                solution = findBestCounterDeckHelper(counterDeckSoFar, matchup)
                if solution != False:
                    return solution
                counterDeckSoFar.pop()
    return False


# Matchup between two decks. Returns cards that counter and a suggestion
# To replace the weakest link in your deck. Uses graph algo and counters algo


class Matchup(object):
    def __init__(self, deck, matchup):
        self.deck = deck
        self.matchup = matchup
        self.suggestion = getCardSwapReccomendations(self.deck, self.matchup)[
            0
        ]
        self.suggestionBestSynergy = getCardSwapReccomendations(
            self.deck, self.matchup
        )[2]
        self.suggestionCounters = getCardSwapReccomendations(
            self.deck, self.matchup
        )[1]
        self.counteredCard = getMostCounteredCardFromDeckAgainstMatchup(
            self.deck, self.matchup
        )[0]
        self.counters = list(
            getMostCounteredCardFromDeckAgainstMatchup(
                self.deck, self.matchup
            )[1]
        )

    def getAverageElixir(self, someDeck):
        total = 0
        for card in someDeck:
            total += cardsInfo[card]["elixir"]
        return round(total / 8, 1)

    def __repr__(self):
        string = f"{', '.join(self.deck)}\nAverage elixir: {self.getAverageElixir(self.deck)}\n\t\t\tV.S.\n{', '.join(self.matchup)}\nAverage elixir: {self.getAverageElixir(matchup)}\n\nThe weakest card in your deck in this matchup is {self.counteredCard}.\n{self.counteredCard} get countered by \n{', '.join(self.counters)} from the opposing deck.\nWe suggest you replace {self.counteredCard} with {self.suggestion}.\n{self.suggestion} synergizes very well with \n{', '.join(self.suggestionBestSynergy)}.\n{self.suggestion} counters \n{', '.join(self.suggestionCounters)}.\n\nMore deck matchups coming soon!"
        return string
