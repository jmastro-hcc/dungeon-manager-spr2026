
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
    if power < 0:
        # can't take negative health
        power = 0
    return power



# Create the character
print("Create the character who will explore this dungeon")

name = input("Name: ")

cclass = input("Class - (W)arrior, (M)age, or (R)ogue: ")
while cclass not in ["W", "M", "R"]:
    cclass = input("Not a valid class - type W, M, or R: ")

char = Character(name, cclass, 10, 1, 1)

# Initialize the game state
game = GameState(char)



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
        char.display()
    elif option == '2':
        game.exploreDungeon()
    elif option == '3':
        print()
        game.displayInventory()
    elif option == '4':
        pass # TODO
    elif option == '5':
        pass # TODO
    elif option == '6':
        # will exit the loop after this
        pass
    else:
        print("Not a valid option")
