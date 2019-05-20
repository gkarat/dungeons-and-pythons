"""
Autor: Georgii Karataev, 485740

Prohlašuji, že celý zdrojový kód jsem zpracoval(a) zcela samostatně.
Jsem si vědom(a), že  nepravdivost tohoto tvrzení může být důvodem
k hodnocení F v předmětu IB111 a k disciplinárnímu řízení.
"""

from collections import deque
import random
from sys import exit

# This game works only with existing csv files in the same folder!

"""
    Tridy
Zname nedostatky: skoro zadne
Styl: docela fajn
"""

class Player:
    def __init__(self, name, hp, ep, race, hunter_skills, mage_skills, weapons):
        self.name = name
        self.hp = int(hp)
        self.hp_max = int(hp)
        self.ep = int(ep)
        self.ep_max = int(ep)
        self.race = race

        if race == 'mage':
            self.skills = list(mage_skills.values())
        elif race == 'hunter':
            self.skills = list(hunter_skills.values())

        # I left stick as a starting weapon for the hero
        self.weapon = weapons["Stick"]

    def __str__(self):
        out = "{0} {1} (HP {2}/150) (EP {3}/80)".format(self.race.capitalize() \
                                                        , self.name, self.hp, self.ep).center(70)
        out += "\n\nYour weapon:\n" + str(self.weapon).center(70) + "\n" + "Your skills:\n"
        for skill in self.skills:
            out += str(skill).center(70) + "\n"
        return out

    def attack(self, enemy, attack_way):
        if type(attack_way).__name__ == "Weapon":
            if random.random() <= attack_way.probability:
                enemy.hp -= attack_way.damage
                print("You used", attack_way.name, "and dealt", attack_way.damage, "to", enemy.name)
                return
            else:
                print("You used", attack_way.name, "and missed!")
                return
        elif type(attack_way).__name__ == "Skill":
            if random.random() <= attack_way.probability:
                enemy.hp -= attack_way.damage
                self.ep -= attack_way.energy_cost
                print("You attacked with", attack_way.name, "and dealt", attack_way.damage, "to",
                      enemy.name)
                return
            else:
                self.ep -= attack_way.energy_cost
                print("You attacked with", attack_way.name, "and missed!")
                return

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def add_ep(self, amount):
        self.ep += amount
        if self.ep > self.ep_max:
            self.ep = self.ep_max


class Monster:
    def __init__(self, name, hp, ep, monster_skills):
        self.name = name
        self.hp = int(hp)
        self.hp_max = int(hp)
        self.ep = int(ep)
        self.ep_max = int(ep)
        self.skills = monster_skills

    def __str__(self):
        out = "{0} HP: {1}/{2} EP: {3}/{4}\n".format(self.name, self.hp, self.hp_max, self.ep, self.ep_max) + \
              ("{0} skills:\n".format(self.name))
        for skill in self.skills:
            out += str(skill) + "\n"
        return out

    def attack(self, enemy, attack_way):
        if random.random() <= attack_way.probability:
            enemy.hp -= attack_way.damage
            self.ep -= attack_way.energy_cost
            print(self.name, "attacked with", attack_way.name, "and dealt", attack_way.damage, "to",
                  enemy.name)
            return
        else:
            self.ep -= attack_way.energy_cost
            print(self.name, "attacked with", attack_way.name, "and missed!")
            return

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def add_ep(self, amount):
        self.ep += amount
        if self.ep > self.ep_max:
            self.ep = self.ep_max


class Skill:
    def __init__(self, name, damage, energy_cost, probability):
        self.name = name
        self.damage = int(damage)
        self.energy_cost = int(energy_cost)
        self.probability = float(probability)

    def __str__(self):
        out = ("{0} - Damage: {1} Energy cost: {2} Chance of hit: {3}".format( \
            self.name, self.damage, self.energy_cost, self.probability))
        return out


class Room:
    def __init__(self, difficulty, monsters):

        # for every room is a special list for defining monsters in it
        self.monsters_in_room = []

        # fills a room with monsters depending on the difficulty
        m_name = random.choice(list(monsters))
        if difficulty == 'e':
            self.monsters_in_room.append(monsters.get(m_name))
        elif difficulty == 'm':
            for i in range(random.randint(1, 2)):
                while monsters.get(m_name) in self.monsters_in_room:
                    m_name = random.choice(list(monsters))
                self.monsters_in_room.append(monsters.get(m_name))
        elif difficulty == 'h':
            for i in range(random.randint(2, 3)):
                while monsters.get(m_name) in self.monsters_in_room:
                    m_name = random.choice(list(monsters))
                self.monsters_in_room.append(monsters.get(m_name))

    # prints a status of a room
    def __str__(self):
        out = ""
        for monster in self.monsters_in_room:
            out += str(self.monsters_in_room.index(monster)) + " - " + str(monster) + "\n"
        return out


class Weapon:
    def __init__(self, name, damage, probability):
        self.name = name
        self.damage = int(damage)
        self.probability = float(probability)

    def __str__(self):
        return "{0} - Damage: {1} Chance of hit {2}".format(self.name, self.damage, self.probability)

"""
    funkce
Zname nedostatky: skoro zadne
Styl: - attack_choose a attack_type_input muzou prijit nejak zamotane
    - chtel bych nejak zjednodusit kod pro overeni spravnosti inputu
"""

def csv_upload():
    mage_skills = {}
    hunter_skills = {}
    skills = {}
    weapons = {}
    monsters = {}

    with open('mage_skills.csv') as file:
        for line in file:
            temp = line.split(',')
            mage_skills[temp[0]] = Skill(temp[0], float(temp[1]), float(temp[2]), float(temp[3]))

    with open('hunter_skills.csv') as file:
        for line in file:
            temp = line.split(',')
            hunter_skills[temp[0]] = Skill(temp[0], float(temp[1]), float(temp[2]), float(temp[3]))

    with open('skills.csv') as file:
        for line in file:
            temp = line.split(',')
            skills[temp[0]] = Skill(temp[0], float(temp[1]), float(temp[2]), float(temp[3]))

    with open('weapons.csv') as file:
        for line in file:
            temp = line.split(',')
            weapons[temp[0]] = Weapon(temp[0], float(temp[1]), float(temp[2]))

    with open('monsters.csv') as file:
        for line in file:
            temp = line.split(',')
            monster_skills = []
            # appending skills as objects for a monster
            for skill_name in temp[3].split(';'):
                monster_skills.append(skills.get(skill_name))
            monsters[temp[0]] = Monster(temp[0], temp[1], temp[2], monster_skills)
    return mage_skills, hunter_skills, skills, weapons, monsters


# controls if creature has enough energy for the skill
def is_enough_ep(creature, skill):
    return creature.ep >= skill.energy_cost


# complex function for a valid attack type input from a user
def attack_type_input():
    attack_type = input("Press 0 if you want to attack with your weapon. " + \
                        "Press 1 if you want to use your skill: ")
    while True:
        if attack_type.isdigit():
            if int(attack_type) in [0, 1]:
                break
        print("Please input a valid value!")
        attack_type = input()
    return int(attack_type)


# asks user for a valid input (closely connected with attack_type_input())
def attack_choose(player):
    attack_type = attack_type_input()

    if attack_type == 1:
        for skill in player.skills:
            print(player.skills.index(skill), "-", str(skill))

        skill_number = int(input("Please select a skill: "))
        while not 0 <= skill_number < len(player.skills):
            print("Please input a valid value!")
            skill_number = int(input())

        while not is_enough_ep(player, player.skills[skill_number]):
            print("You don't have enough energy!")
            return attack_choose(player)
        return player.skills[skill_number]
    return player.weapon


# asks user for a valid target choosing
def target_input(room):
    target = input("Please select a target... ")
    while True:
        if target.isdigit():
            if 0 <= int(target) < len(room.monsters_in_room):
                break
        print("Please input a valid value!")
        target = input()
    return int(target)


def monster_attack(room, player):
    # chooses randomly monster in the room
    attacking_monster = random.choice(room.monsters_in_room)
    # chooses one of its skills to attack with
    monster_using_skill = random.choice(attacking_monster.skills)
    while not is_enough_ep(attacking_monster, monster_using_skill):
        attacking_monster = random.choice(room.monsters_in_room)
        monster_using_skill = random.choice(attacking_monster.skills)

    # main function from a class Monster calling
    attacking_monster.attack(player, monster_using_skill)


def round_make(player, room):
    # writes player stats
    print(player)

    # starts a single battle
    fight(player, room)

    # if player.hp <= 0 -> end of the game
    if player.hp <= 0:
        exit("Sorry, you are a loser :( Goodbye!")

    # 10 ep for everyone in the room after every single round
    for monster in room.monsters_in_room:
        monster.add_ep(10)
    player.add_ep(10)


# defines situation when player found a new weapon
def new_weapon(rooms, room, weapons, player):

    # if it is not a last room
    if not rooms.index(room) == len(rooms) - 1:

        # randomly generates a new weapon
        new_weapon = random.choice(list(weapons.values()))
        while new_weapon == player.weapon:
            new_weapon = random.choice(list(weapons.values()))

        print("You found", new_weapon)

        answer = input("Do you want to equip it? (y / n) ")
        while answer not in ['y', 'n']:
            print("Please input a valid value!")
            answer = input()

        if answer == 'y':
            del weapons[player.weapon.name]
            player.weapon = new_weapon
        else:
            del weapons[new_weapon.name]


# defines every round
def fight(player, room):
    print("=== Monsters in the room ===".center(70))
    print(room)

    target = target_input(room)
    attack_type = attack_choose(player)

    # player attack
    player.attack(room.monsters_in_room[target], attack_type)

    # removing dead monster from a room, but setting back his stats for a case if it will appear in other rooms
    if room.monsters_in_room[target].hp <= 0:
        room.monsters_in_room[target].hp, room.monsters_in_room[target].ep = \
            room.monsters_in_room[target].hp_max, room.monsters_in_room[target].ep_max
        room.monsters_in_room.pop(target)

    # checks if any monster left in a room
    if len(room.monsters_in_room) < 1:
        return

    # monster attack
    monster_attack(room, player)


def game():
    print("""
         ▄▄▌ ▐ ▄▌▄▄▄ .▄▄▌   ▄▄·       • ▌ ▄ ·. ▄▄▄ .
     ██· █▌▐█▀▄.▀·██•  ▐█ ▌▪▪     ·██ ▐███▪▀▄.▀·
     ██▪▐█▐▐▌▐▀▀▪▄██▪  ██ ▄▄ ▄█▀▄ ▐█ ▌▐▌▐█·▐▀▀▪▄
     ▐█▌██▐█▌▐█▄▄▌▐█▌▐▌▐███▌▐█▌.▐▌██ ██▌▐█▌▐█▄▄▌
      ▀▀▀▀ ▀▪ ▀▀▀ .▀▀▀ ·▀▀▀  ▀█▄▀▪▀▀  █▪▀▀▀ ▀▀▀ 
      """)
    # uploading csv files
    mage_skills, hunter_skills, skills, weapons, monsters = csv_upload()

    races = ["mage", "hunter"]
    difficulties = ['e', 'm', 'h']

    # game process
    print("=== to the Dungeons and Pythons ===".center(48))

    name = str(input("Hero, write your name: "))
    race = str(input("Okay {0}, choose your race (mage / hunter): ".format(name)))
    while race not in races:
        print("Please input a valid value!")
        race = str(input())

    difficulty = str(input("Tell me how difficult your journey will be? (e / m / h) "))
    while difficulty not in difficulties:
        print("Please input a valid value!")
        difficulty = str(input())

    # initiating the player
    player = Player(name, 150, 80, race, hunter_skills, mage_skills, weapons)

    # creating and filling rooms
    rooms_number = {'e': 4, 'm': 6, 'h': 8}
    rooms = deque(Room(difficulty, monsters) for i in range(rooms_number[difficulty]))

    # game process
    for room in rooms:
        print(("#" * 50).center(70) + "\n\n" + "You entered a room".center(70) + "\n\n" + ("#" * 50).center(70))

        # 1st round
        round_make(player, room)

        while len(room.monsters_in_room) > 0:
            print("\n" + "NEXT ROUND".center(70) + "\n")
            round_make(player, room)

        # if it is not a last room, suggests a new weapon to choose
        new_weapon(rooms, room, weapons, player)

        # by the end of a room heals a player and maximizes his energy
        player.heal(20)
        player.ep = player.ep_max

    print("You have won! My congratulations!")

game()