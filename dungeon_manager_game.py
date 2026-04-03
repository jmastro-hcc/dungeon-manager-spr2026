
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
        print(f"Class: {self.cclass}")
        print(f"Health: {self.health}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")



# Create the character
print("Create the character who will explore this dungeon")

name = input("Name: ")

cclass = input("Class - (W)arrior, (M)age, or (R)ogue: ")
while cclass not in ["W", "M", "R"]:
    cclass = input("Not a valid class - type W, M, or R: ")

char = Character(name, cclass, 10, 1, 1)

#char.display()



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
        pass # TODO
    elif option == '3':
        pass # TODO
    elif option == '4':
        pass # TODO
    elif option == '5':
        pass # TODO
    elif option == '6':
        # will exit the loop after this
        pass
    else:
        print("Not a valid option")
