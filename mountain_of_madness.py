# The Mountain of Madness (OOP Edition)
# 1/28/2020
# Steve Eckles

from textwrap import dedent
import mountain_scenes as scenes
import mountain_units as units

class Engine(object):
    def __init__(self, game_map):
        self.game_map = game_map

    def play(self):
        current_scene = game_map.opening_scene()

        while True:
            next_scene = current_scene.enter(player)
            current_scene = game_map.next_scene(next_scene)

class Map(object):

    scene_list = {
        'ex_search': scenes.ExteriorSearch(),
        'ex_approach': scenes.ExteriorApproach(),
        'ex_wait': scenes.ExteriorWait(),
        'first_fork': scenes.FirstFork()
    }

    def next_scene(self, scene_name):
        return Map.scene_list.get(scene_name)

    def opening_scene(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("\nType 'help' during any normal prompt to see help messages.\n")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(dedent(f"""
        You are {player.name}, an adventurer of little renown.
        You have traveled far to the south of your homeland in search of treasure
        and glory. After many days of traveling through flat, boring plains; dank,
        dreadful bogs; and dense, dark forests, you at last arrive at your destination:
        the fabled Mountain of Madness. Inside is said to dwell a powerful sorcerer
        and his ragtag band of minions and deadly beasts. You ready your sword and
        steel yourself for the trials ahead.\n
        """))

        print(f"Your SKILL is {player.stats['skill']}. Your STAMINA is {player.stats['stamina']}. Your LUCK is {player.stats['luck']}.")
        print("Type 'stats' during any normal prompt to see your stats.\n")
        print("Press ENTER to begin your adventure!")
        scenes.choose()
        return scenes.MountainExterior()

player = units.Player(input("What is your name, adventurer?\n> "))

if player.name == '':
    player.name = 'Otaku Jeff'

game_map = Map()
run_game = Engine(game_map)
run_game.play()
