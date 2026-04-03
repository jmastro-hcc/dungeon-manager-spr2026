
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

char.display()
