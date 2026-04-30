
import random

classFullName = {
    "W": "Warrior",
    "M": "Mage",
    "R": "Rogue",
}

# Items that could possibly be found in a treasure chest
# Tuples of (Item name, Quantity)
possibleTreasureChestItems = [
    ("Potion", 1),
    ("Toy Knife", 1),
    ("Gold", 5),
]

# Items that could be given as rewards
# There are different ones depending on the type of enemy. This dictionary
# maps the enemy type to a list of (Item, Quantity) tuples just like
# possibleTreasureChestItems above
possibleRewardItems = {}
possibleRewardItems["Troll"] = [
    ("Rusty Sword", 1),
    ("Gold", 25),
    ("Gold", 50),
    ("Gold", 150),
    ("Nothing", 0),
]

# Items that are weapons and can be used in a battle
weaponItems = ["Potion", "Toy Knife", "Rusty Sword"]

# Types of potions
potionTypes = ["Exploding Potion", "Health Potion"]

# Random set of paths out of a room.
# There's always at least one.
def randomPaths():
    paths = []
    if random.random() < 0.5:
        paths.append("(L)eft")
    if random.random() < 0.5:
        paths.append("(S)traight")
    if random.random() < 0.5:
        paths.append("(R)ight")
    if len(paths) == 0:
        paths.append("(S)traight")
    return paths

class GameState:
    def __init__(self, playerChar):
        self.playerChar = playerChar
        # Inventory is a dictionary mapping item names to how many the player has
        # Start out with 10 gold; everything else must be collected from treasure
        # chests or winning battles
        self.inventory = {"Gold": 10}
    
    # Create a new character, if the user wants to
    # Return True if they did
    def optionallyCreateNewCharacter(self):
        createNew = input("Do you want to start over with a new character? (Y/N) ")
        if createNew == 'Y':
            self.playerChar = createCharByUserInput()
            return True
        else:
            return False

    # Explore the dungeon
    def exploreDungeon(self):
        # randomly generate a set of paths the player can take
        # repeat until they go back to the menu
        path = ""
        while path != "M":
            paths = randomPaths()
            print()
            print("There are " + str(len(paths)) + " paths: " + ", ".join(paths))
            print("Or press M to go back to the menu.")
            path = input("Which path will you take? ")
            while path not in ["L", "S", "R", "M"]:
                path = input("That is not a valid path. Which path? ")
            if path != "M":
                # The choice of path is actually meaningless; the room is random regardless
                self.randomRoom()
                # The player might have died in an enemy encounter.
                # If so, it's game over.
                if self.playerChar.isDead():
                    print()
                    print("~~~~~ GAME OVER ~~~~~")
                    return
    
    # Enter a room
    def randomRoom(self):
        r = int(random.random() * 3)
        if r == 0:
            # Treasure chest
            print("You found a treasure chest")
            item, quantity = random.choice(possibleTreasureChestItems)
            print(f"Inside is {quantity} {item}")
            self.addItem(item, quantity)
        elif r == 1:
            # Enemy encounter
            self.battleEnemy()
        elif r == 2:
            # Empty room
            print("There's nothing here")
    
    # Enemy encounter
    def battleEnemy(self):
        enemy = randomEnemy()
        print(f"There is a {enemy.type} here!")
        while self.playerChar.health > 0 and enemy.health > 0:
            # Player attacks enemy
            # will add a menu with ability to use an item later
            self.attackMenu(enemy)

            # Enemy can only attack player back if it's still alive
            if enemy.health > 0:
                print(f"{enemy.type} attacks {self.playerChar.name}")
                self.playerChar.health -= attackPower(enemy, self.playerChar)
        
        if self.playerChar.health <= 0:
            print("You are dead.")
        if enemy.health <= 0:
            print(f"You have killed the {enemy.type}.")
            rewardItem, quantity = random.choice(possibleRewardItems[enemy.type])
            print(f"It had {quantity} {rewardItem} in its pockets")
            self.addItem(rewardItem, quantity)
    
    # A menu for attacking (using an item or otherwise) during a battle
    def attackMenu(self, enemy):
        print(f"Press P to punch the {enemy.type}, or use one of these items:")
        for itemName in self.inventory:
            # only list it as an option if it is a weapon and the player has any
            if itemName in weaponItems and self.inventory[itemName] > 0:
                print(f"  {itemName}")
        
        # there are multiple reasons why this might need to be asked again
        reAsk = True
        while reAsk:
            itemToUse = input("> ")
            if itemToUse == "P":
                # punch; valid option
                reAsk = False
            elif itemToUse not in self.inventory or self.inventory[itemToUse] <= 0:
                print(f"You do not have any {itemToUse}. Try something else.")
                reAsk = True
            elif itemToUse not in weaponItems:
                print(f"{itemToUse} is not a weapon. Try something else.")
                reAsk = True
            else:
                # valid item
                reAsk = False
        
        if itemToUse == "P":
            print(f"{self.playerChar.name} punches {enemy.type}")
            enemy.health -= attackPower(self.playerChar, enemy)
        elif itemToUse == "Toy Knife":
            # knife has 3 attack power
            print(f"{self.playerChar.name} used Toy Knife. +3 attack.")
            enemy.health -= attackPowerNumber(3, enemy)
            # you keep the knife even after using it
        elif itemToUse == "Rusty Sword":
            # rusty sword has 5 attack power
            print(f"{self.playerChar.name} used Rusty Sword. +5 attack.")
            enemy.health -= attackPowerNumber(3, enemy)
            # the sword breaks after you use it
            print("The Rusty Sword snaps in half.")
            self.inventory["Rusty Sword"] -= 1
        elif itemToUse == "Potion":
            # There are two possible potions, and you don't know what
            # each one is until you use it
            potion = random.choice(potionTypes)
            if potion == "Exploding Potion":
                print(f"{self.playerChar.name} used a potion. It explodes! +10 attack.")
                enemy.health -= attackPowerNumber(10, enemy)
                # about one third of the time, the player gets caught
                # in the blast
                if random.random() > 0.66:
                    print(f"{self.playerChar.name} is caught in the blast. -2 health.")
                    self.playerChar.health -= 2
            elif potion == "Health Potion":
                print(f"{self.playerChar.name} used a potion. It's a health potion! +8 health.")
                self.playerChar.health += 8
            # one potion has been used
            self.inventory["Potion"] -= 1

    # Add an item to the inventory
    def addItem(self, itemName, quantity):
        if itemName in self.inventory:
            self.inventory[itemName] += quantity
        else:
            self.inventory[itemName] = quantity
    
    # If the player has at least one of an item, subtract it and return True
    # If the player does not have the item, return False
    def useItem(self, itemName):
        if itemName in self.inventory and self.inventory[itemName] > 0:
            self.inventory[itemName] -= 1
            return True
        else:
            return False
    
    # Print everything in the inventory
    def displayInventory(self):
        print("Inventory:")
        for item in self.inventory:
            print(f"{item}: {self.inventory[item]}")



    # Save / load functionality
    # The save file format is:
    # <player name>
    # <player class>
    # <player health>
    # <player attack>
    # <player defense>
    # <inventory item>,<quantity>
    # <inventory item>,<quantity>
    # <inventory item>,<quantity>
    # etc.

    def saveGame(self, gameName):
        filename = gameName + ".txt"
        with open(filename, 'w') as f:
            f.write(self.playerChar.name + '\n')
            f.write(self.playerChar.cclass + '\n')
            f.write(str(self.playerChar.health) + '\n')
            f.write(str(self.playerChar.attack) + '\n')
            f.write(str(self.playerChar.defense) + '\n')
            for item in self.inventory:
                f.write(f"{item},{self.inventory[item]}\n")

def loadGame(gameName):
    filename = gameName + ".txt"
    with open(filename, 'r') as f:
        name = f.readline().strip()
        cclass = f.readline().strip()
        health = int(f.readline().strip())
        attack = int(f.readline().strip())
        defense = int(f.readline().strip())
        inventory = {}
        for line in f:
            item, quantity = line.split(',')
            inventory[item] = int(quantity)
    
    player = Character(name, cclass, health, attack, defense)
    game = GameState(player)
    game.inventory = inventory

    return game



class Character:
    def __init__(self, name, cclass, health, attack, defense):
        self.name = name
        self.cclass = cclass
        self.health = health
        self.attack = attack
        self.defense = defense
    
    # Print this character's stats to the screen
    def display(self):
        print(f"Name: {self.name}")
        print(f"Class: {classFullName[self.cclass]}")
        print(f"Health: {self.health}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
    
    # Am I still alive?
    def isAlive(self):
        return self.health > 0
    
    # Am I dead?
    def isDead(self):
        return not self.isAlive()

# Ask the user for information about a character
def createCharByUserInput():
    print("Create the character who will explore this dungeon")

    name = input("Name: ")

    cclass = input("Class - (W)arrior, (M)age, or (R)ogue: ")
    while cclass not in ["W", "M", "R"]:
        cclass = input("Not a valid class - type W, M, or R: ")

    return Character(name, cclass, 10, 1, 1)



class Enemy:
    def __init__(self, type, health, attack, defense):
        self.type = type
        self.health = health
        self.attack = attack
        self.defense = defense

# Generate a random enemy
def randomEnemy():
    # health from 5 to 15
    health = int(random.random() * 10 + 5)
    # attack from 1 to 5
    attack = int(random.random() * 5 + 1)
    # defense from 1 to 4
    defense = int(random.random() * 4 + 1)
    return Enemy("Troll", health, attack, defense)



# Calculate how much health to take away from a character
# based on their attack power and the victim's defense
def attackPower(attacker, defender):
    return attackPowerNumber(attacker.attack, defender)

# Calculate how much health to take away from a character
# based on thee given attack power and the victim's defense
def attackPowerNumber(givenPower, defender):
    power = givenPower - defender.defense
    if power < 1:
        # but it always has at least a little power
        power = 1
    return power



# Create the character and initialize the game state
game = GameState(createCharByUserInput())



# Main menu
option = '0'
while option != '6':
    print()
    print("=== MAIN MENU ===")
    print("1. View Character")
    print("2. Explore Dungeon")
    print("3. View Inventory")
    print("4. Save Game")
    print("5. Load Game")
    print("6. Exit")
    option = input("> ")
    if option == '1':
        game.playerChar.display()
    elif option == '2':
        game.exploreDungeon()
        # If the player died in the dungeon, they can either start over with a new character or quit
        if game.playerChar.isDead():
            startOver = game.optionallyCreateNewCharacter()
            if not startOver:
                break
    elif option == '3':
        print()
        game.displayInventory()
    elif option == '4':
        gName = input("Enter a name for the game: ")
        game.saveGame(gName)
    elif option == '5':
        gName = input("Enter name of the game to load: ")
        game = loadGame(gName)
    elif option == '6':
        # will exit the loop after this
        pass
    else:
        print("Not a valid option")
