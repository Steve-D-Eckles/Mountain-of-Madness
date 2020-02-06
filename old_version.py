# The Mountain of Madness
# 1/15/2020
# Steve Eckles

import random

prompt = ("> ")
stats = {
    'skill': random.randint(1, 6) + 6,
    'stamina': random.randint(2, 12) + 12,
    'luck': random.randint(1, 6) + 6,
    'gold': 3,
    'items': ['a sword', 'a shield', 'a set of clothes']
}

print("What is your name, adventurer?")
player_name = input(prompt)

if player_name == '':
    player_name = "Otaku Jeff"


def choose():
    choice = input(prompt)
    choice = choice.lower()
    if choice == 'help':
        print("Gameplay: Enter relevent commands when prompted to continue on your adventure.")
        print("Status: Enter 'stats' during any prompt to see your current stats.")
        print("Gold: Enter 'gold' during any prompt to see your current gold.")
        print("Items: Enter 'items' during any prompt to see your currently held items.")
        print("""Combat: When you are engaged in combat, you will see your attack
        (2d6 + SKILL) and your enemy's attack (2d6 + ENEMY SKILL). Whichever combatant
        rolled lower will receive 2 damage to his or her STAMINA score. No damage
        is dealt or received on a tie. Press ENTER after each attack to advance combat.""")
        print("""Luck: At certain points in the adventure, you must Test Your Luck.
        You will roll 2d6. If the result is lower than your LUCK score, you are
        lucky and your LUCK will be reduced by 1. If your result is higher than
        your LUCK score, you are unlucky and must face the consequences.\n""")
        return ''
    elif choice == 'stats':
        print(f"Your SKILL is {stats['skill']}. Your STAMINA is {stats['stamina']}. Your LUCK is {stats['luck']}.\n")
        return ''
    elif choice == 'gold':
        print(f"You are currently carrying {stats['gold']} gold.")
        return ''
    elif choice == 'items':
        if len(stats['items']) > 0:
            print(f"Your inventory currently contains a {', '.join(stats['items'][:-1])}, and {stats['items'][-1]}")
        else:
            print(f"Your inventory is empty.")
        return ''
    else:
        return choice

def combat(enemy, count, e_skill, e_stamina, stats):
    for i in range(1, count + 1):
        print(f"{enemy} {i} prepares to fight!", end='')
        choose()
        i_stamina = e_stamina
        while i_stamina > 0:
            enemy_roll = random.randint(2, 12) + e_skill
            player_roll = random.randint(2, 12) + stats['skill']
            print(f"{enemy} {i} attacks with {enemy_roll}. {player_name} defends with {player_roll}.")

            if enemy_roll > player_roll:
                stats['stamina'] -= 2
                if stats['stamina'] < 0:
                    stats['stamina'] = 0
                print(f"You've been hit! Your STAMINA is {stats['stamina']}.", end='')
            elif player_roll > enemy_roll:
                i_stamina -= 2
                if i_stamina < 0:
                    i_stamina = 0
                print(f"You landed a clean strike! {enemy}'s stamina is {i_stamina}'", end='')
            else:
                print("Neither combatant could bypass the other's defense!", end='')

            choose()
            if i_stamina == 0:
                print(f"{enemy} {i} has been slain!")
                choose()
            if stats['stamina'] == 0:
                print("You have failed! Your adventure is over.")
                input("Press ENTER to quit.\n> ")
                quit()
    return

def cave(cave_response, stats):
    while cave_response == '' or not cave_response in ['approach', 'search', 'wait']:
        print("""Choose one:
    -APPROACH the cave
    -SEARCH for another entrance
    -WAIT until nightfall""")
        cave_response = choose()

    if cave_response == 'approach':
        print("""You stride boldly towards the cave. As you approach, two GOBLIN GUARDS
emerge from the darkness. They are chittering in a language that you do not understand,
but you have seen enough combat to understand the cruel gleam in their eyes.
You must FIGHT!\n\nPress ENTER to begin the combat.""")
        choose()
        combat('GOBLIN GUARD', 2, 5, 4, stats)
        print("""Victory over the GOBLIN GUARDS is yours! You take a moment to
examine their belongings. Their arms and armor are crude and worthless, but you
find 1 GOLD and a COPPER KEY. You decide that you have found everything of value
that these lowly guards have to offer and head deeper into the cave.\n
Press ENTER to continue.""")
        stats['gold'] += 1
        stats['items'].append('a copper key')
        choose()
        first_fork(stats)

    elif cave_response == 'search':
        print("""You trace a wide, slow path through the local flora surrounding the mountain.
After several hours of searching, you find yourself back where you started with
nothing more accomplished than sore feet and dashed hopes. Night approaches...\n""")
        cave_response = 'wait'

    if cave_response == 'wait':
        print("""As the sun begins to set, you become aware of the toll your recent journey
has taken on your body. However, you are in good shape and accustomed to travel,
so it surprises you slightly when your eyelids grow heavy and begin to droop.
Too late you realize your mistake: there are Mela flowers growing in the undergrowth around you!
You recall hearing about these dangerous flowers in your youth: their pollen causes
intense drowsiness in most mammals. You struggle to pull yourself away from the area
lest prolonged exposure cause an unending slumber. You collapse some thirty feet away
in a small clearing and drift to sleep...

Press ENTER to TEST YOUR LUCK.""")

        choose()
        luck_test = random.randint(2, 12)
        print(f"You rolled {luck_test}. Your LUCK is {stats['luck']}")

        if luck_test <= stats['luck']:
            stats['luck'] -= 1
            print(f"""You are lucky. Your LUCK is reduced to {stats['luck']}. You
awaken in the early dawn hours with nothing worse to show for last night's misadventure
than a stiff back from sleeping on the cold ground.
You decide that you have no option other than to proceed into the mountain through
the cave entrance that you saw yesterday. You cautiously approach the low, wide opening.
As you draw closer to the threshold, you see crude wooden chairs around a small table
indicating that this area is typically occupied. You are relieved to find no guards
in the immediate area; you surmise that they must be out on patrol and decide to continue
deeper into the cave.\n
Press ENTER to ready yourself and proceed...""")
            choose()
            first_fork(stats)

        else:
            print("""You are unlucky. You are discovered in the night by two patrolling
GOBLIN GUARDS. The only mercy you experience is that the pollen-induced slumber
prevented you from feeling the sword enter your back. Your adventure is over.""")
            input("Press ENTER to quit.\n> ")

def first_fork(stats):
    print("""The light lessens as you descend a steady slope deeper into the cave.
You see a fork in the tunnel ahead, but your limited dark vision does not allow you
to see far down either path ahead of you. Will you:
    -Take the path on the LEFT
    -Take the path on the RIGHT""")

    fork_response = choose()
    while fork_response == '' or not fork_response in ['left', 'right']:
        print("""Pick one:
    -Take the path on the LEFT
    -Take the path on the RIGHT""")
        fork_response = choose()

    if fork_response == 'left':
        print("Hold on a minute")
        left_tine(stats)

    if fork_response == 'right':
        print("""You head down the tunnel to the right. After only a few moments
of walking, you come upon a closed wooden door. The door is locked, but you could
try to ram it down with your shoulder. Would you like to:
    -RAM the door
    -Turn BACK""")
        door_response = choose()
        while door_response == '' or not door_response in ['ram', 'back']:
            print("""Choose one:
    -RAM the door
    -Turn BACK""")
            door_response = choose()

        if door_response == 'ram':
            print("""You stretch out your shoulder and ready yourself to charge the
unsuspecting door. You must Test Your Luck. For each failure, you will take 2 points
of STAMINA damage. You may try as many times as you like, or you may turn BACK at
any time.\n\nPress ENTER to TEST YOUR LUCK""")
            while True:
                ram_response = choose()
                if ram_response == 'back':
                    left_tine(stats)
                luck_test = random.randint(2, 12)
                print(f"You rolled {luck_test}, your LUCK is {stats['luck']}")
                if luck_test > stats['luck']:
                    stats['stamina'] -= 2
                    print("You are unlucky and unable to break open the door. Try again or go BACK")
                    continue
                else: break

            stats['luck'] -= 1
            print("""You are lucky.""")

def game_start():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\nType 'help' during any normal prompt to see help messages.\n")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"""You are {player_name}, an adventurer of little renown. You have traveled far to the
south of your homeland in search of treasure and glory. After many days of traveling
through flat, boring plains; dank, dreadful bogs; and dense, dark forests, you
at last arrive at your destination: the fabled Mountain of Madness.\n
Inside is said to dwell a powerful sorcerer and his ragtag band of minions and
deadly beasts. You ready your sword and steel yourself for the trials ahead.\n""")

    print(f"Your SKILL is {stats['skill']}. Your STAMINA is {stats['stamina']}. Your LUCK is {stats['luck']}.")
    print("Type 'stats' during any normal prompt to see your stats.\n")
    print("Press ENTER to begin your adventure!")
    choose()

    # 1. CAVE - DAY
    print("""After some observation of the mountain from afar, you notice a small cave
entrance on its northern face. It's midday, but you don't see any guards from your
vantage point. Would you like to:
    -APPROACH the cave
    -SEARCH for another entrance
    -WAIT until nightfall""")

    cave_response = choose()

    cave(cave_response, stats)

game_start()
