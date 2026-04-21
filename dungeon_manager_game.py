
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
    ("Gold", 5),
]

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
            print(f"{self.playerChar.name} attacks {enemy.type}")
            enemy.health -= attackPower(self.playerChar, enemy)

            # Enemy can only attack player back if it's still alive
            if enemy.health > 0:
                print(f"{enemy.type} attacks {self.playerChar.name}")
                self.playerChar.health -= attackPower(enemy, self.playerChar)
        
        if self.playerChar.health <= 0:
            print("You are dead.")
        if enemy.health <= 0:
            print(f"You have killed the {enemy.type}.")

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
    power = attacker.attack - defender.defense
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
        pass # TODO
    elif option == '6':
        # will exit the loop after this
        pass
    else:
        print("Not a valid option")
