from random import randint

class Unit(object):
    """Enemy template / base for player"""
    def __init__(self, name, *stats):
        self.name = name
        self.stats = {
            'skill': stats[0],
            'stamina': stats[1]
        }

class Player(Unit):
    """Extended unit with extra stats to serve as the player character"""
    def __init__(self, name):
        super(Player, self).__init__(name, randint(1, 6) + 6, randint(1, 6) + randint(1, 6) + 12)
        self.stats['luck'] = randint(1, 6) + 6
        self.stats['gold'] = 3
        self.stats['items'] = ['a sword', 'a shield', 'a set of clothes']
