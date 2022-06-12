import random
import json
from time import sleep

class Human:
    def __init__(self, name, place=None):
        self.location = None
        try:
            self.travel(place)
        except:
            pass
        self.name = name
        self.money = 20 
        self.gladness = 50
    def greeting(self, human):
        print(f"Hello {human.name}, I am {self.name}")
    def drive(self):
        if self.car:
            self.car.drive()
    def work(self):
        self.money += random.randint(5, 10)
        self.gladness -= random.randint(2, 5)
    def rest(self):
        self.money -= random.randint(3, 7)
        self.gladness += random.randint(2, 5)
        try:
            self.money -= self.location.money
            self.gladness += self.location.gladness
        except:
            pass
    def travel(self, place):
        if self.location:
            self.location.remove(self)
        self.location = place
        self.location.add(self)
        if not hasattr(self, "car"):
            self.money -= 2

class Place:
    def __init__(self, name, g, m):
        self.name = name
        self.humans = []
        self.gladness = g
        self.money = m
    def add(self, human):
        if not human in self.humans:
            self.humans.append(human)
    def remove(self, human):
        if human in self.humans:
            self.humans.remove(human)

class House:
    def __init__(self):
        self.humans = []
    def add(self, human):
        if not human in self.humans:
            self.humans.append(human)
    def greetingAll(self):
        for human in self.humans:
            for some_human in self.humans:
                if human != some_human:
                    human.greeting(some_human)

class Car:
    def __init__(self, name, year, price):
        self.name = name
        self.year = year
        self.price = price
    def drive(self):
        print(f"{self.name} едет")
    def buy(self, human):
        if human.money >= self.price:
            self.owner = human
            human.car = self
            human.money -= self.price
            print(f"{human.name} купил {self.name}")
        else:
            print(f"{human.name} не хватает средств на {self.name}")
    
class Player(Human):
    def __init__(self, location, name, h, w):
        super().__init__(name, location)
        self.height = h
        self.weight = w
    def save(self):
        with open('./save.json', 'w') as f:
            data = {}
            data["name"] = self.name
            data["h"] = self.height
            data["w"] = self.weight
            json.dump(data, f)
    def actions(self):
        print("Выберите действие: ")
        print("1. Отдохнуть")
        print("2. Пойти на работу")
        print("3. Купить машину")
        print("4. Баланс")
        print("5. Люди рядом")
        print("6. Перейти в локацию")
    def day(self):
        choice = int(input("-> "))
        if choice == 1:
            self.rest()
        elif choice == 2:
            self.work()
        elif choice == 3:
            print("Машины: ")
            for i in range(len(autopark)):
                print(f"{i + 1}. {autopark[i].name}")
            choice = int(input("-> "))
            if choice > 0 and choice < len(autopark):
                autopark[choice - 1].buy(self)
        elif choice == 4:
            print(f"Баланс: {self.money}")
            self.day()
        elif choice == 5:
            print("Люди рядом: ")
            humans = list(self.location.humans)
            humans.remove(self)
            for i in range(len(humans)):
                print(f"{i + 1}. {humans[i].name}")
            choice = int(input("-> "))
            if choice > 0 and choice < len(humans) + 1:
                self.npcsActions(humans[choice - 1])
        elif choice == 6:
            print("Локации: ")
            for i in range(len(places)):
                print(f"{i + 1}. {places[i].name}")
            choice = int(input("-> "))
            if choice > 0 and choice < len(places) + 1:
                self.travel(places[choice - 1])
        else:
            self.day()
    def npcsActions(self, human):
        pass
        #Вывод всех созданных действий npcs_actions

class Thief(Human):
    def __init__(self, name):
        super().__init__(name)
        self.strength = random.randint(1, 10)
    def steal(self, human):
        human.money -= self.strength
        self.money += self.strength
        print(f"Вор украл деньги у {human.name}")

class NPC(Human):
    def __init__(self, name, place=None):
        super().__init__(name, place)
        self.relationship = 0

class Action:
    def __init__(self, name, money, gladness, relationship, duo, condtition):
        self.name = name
        self.money = money
        self.gladness = gladness
        self.relationship = relationship
        self.duo = duo
        self.condtition = condtition
    def do(self, initiator, target):
        if isinstance(initiator, Player):
            target.relationship += self.relationship
        if isinstance(initiator, Player) and self.condition > target.relationship:
            if self.duo:
                initiator.money += self.money
                initiator.gladness += self.gladness
                target.money += self.money
                target.gladness += self.gladness
            else:
                initiator.money += self.money
                initiator.gladness += self.gladness
                target.money -= self.money
                target.gladness -= self.gladness
        else:
            print("Невозможно совершить данное действие")

house = None
autopark = None
player = None
thief = None
places = None
home = None
npcs_actions = None

def game_start():
    global house, autopark, thief, places, home
    house = House()
    thief = Thief("Vladislav")

    home = Place("Home", 0, 0)

    npcs_actions = [
        Action("Поговорить", 0, 2, 2, True, 0)
        #Добавить действий
    ]

    places = [
        home,
        Place("Park", 2, 3),
        Place("Museum", 4, 6),
        Place("Cafe", 10, 20),
    ]

    h1 = Human("Sergey", random.choice(places))
    h2 = Human("Ivan", random.choice(places))
    h3 = Human("Dima", random.choice(places))
    h4 = Human("Petr", random.choice(places))
    h5 = Human("Nastya", random.choice(places))
    h6 = Human("Katya", random.choice(places))
    h7 = Human("Alex", random.choice(places))
    h8 = Human("Kristina", random.choice(places))

    house.add(h1)
    house.add(h2)
    house.add(h3)
    house.add(h4)
    house.add(h5)
    house.add(h6)
    house.add(h7)
    house.add(h8)

    autopark = [
        Car("BMW", 2019, 200),
        Car("Bentli", 2019, 100),
        Car("Bugatti", 2019, 300),
    ]

def create_player():
    global player
    h = input("Введите рост персонажа: ")
    w = input("Введите вес персонажа: ")
    name = input("Введите имя персонажа: ")
    player = Player(name, h, w)
    player.save()

def init_player():
    global player
    try:
        with open('./save.json') as json_file:
            data = json.load(json_file)
            if not data:
                create_player()
            else:
                player = Player(home, data["name"], data["h"], data["w"])
        house.add(player)
    except:
        print("Добавьте файл save.json в папку к файлу")
        input("Нажмите Enter...")
        exit()

game_start()
init_player()

day = 1
while True:
    print("Day: ", day)
    print("Location: ", player.location.name)
    print("Money: ", player.money)
    print("Gladness: ", player.gladness)
    player.actions()
    player.day()
    #while True с итератором
    for human in house.humans:
        if isinstance(human, Player):
            continue
        actions = [human.rest, human.work, human.travel]
        place = random.choice(places)
        action = random.choice(actions)
        if action == human.travel:
            action(place)
        else:
            action()
        if random.randint(1,100) <= 5:
            if not hasattr(human, "car"):
                print(f"{human.name} хочет купить машину")
                car = random.choice(autopark)
                if not hasattr(car, "owner"):
                    car.buy(human)
    if random.randint(1,100) <= 20:
        thief.steal(random.choice(house.humans))
    day += 1