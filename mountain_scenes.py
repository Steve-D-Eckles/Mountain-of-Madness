from random import randint
from textwrap import dedent
import mountain_units as units

def choose():
    """Get user input or output gameplay information upon request"""
    choice = input('> ')
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
        print(f"Your SKILL is {player.stats['skill']}. Your STAMINA is {player.stats['stamina']}. Your LUCK is {player.stats['luck']}.\n")
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

def combat(enemy, count, player):
    """Handle combat encounters using Unit and Player objects from mountain_units"""
    for i in range(1, count + 1):
        print(f"{enemy.name} {i} prepares to fight!", end='')
        choose()
        i_stamina = enemy.stats['stamina']
        while i_stamina > 0:
            enemy_roll = randint(1, 6) + randint(1, 6) + enemy.stats['skill']
            player_roll = randint(1, 6) + randint(1, 6) + player.stats['skill']
            print(f"{enemy.name} {i} attacks with {enemy_roll}. {player.name} defends with {player_roll}.")

            if enemy_roll > player_roll:
                player.stats['stamina'] -= 2
                if player.stats['stamina'] < 0:
                    player.stats['stamina'] = 0
                print(f"You've been hit! Your STAMINA is {player.stats['stamina']}.", end='')
            elif player_roll > enemy_roll:
                i_stamina -= 2
                if i_stamina < 0:
                    i_stamina = 0
                print(f"You landed a clean strike! {enemy.name}'s stamina is {i_stamina}", end='')
            else:
                print("Neither combatant could bypass the other's defense!", end='')

            choose()
            if i_stamina == 0:
                print(f"{enemy.name} {i} has been slain!")
                choose()
            if player.stats['stamina'] == 0:
                print("You have failed! Your adventure is over.")
                input("Press ENTER to quit.\n> ")
                raise SystemExit
    return

class Scene(object):
    """Fallback Parent Scene"""

    def enter(self, player):
        print("You shouldn't be here. Whoops!")
        raise SystemExit

class MountainExterior(Scene):

    choices = {
        'approach': 'ex_approach',
        'wait': 'ex_wait',
        'search': 'ex_search'
    }

    def enter(self, player):
        print(dedent("""
        After some observation of the mountain from afar, you notice a small cave
        entrance on its northern face. It's midday, but you don't see any guards from your
        vantage point. Would you like to:
        \t-APPROACH the cave
        \t-SEARCH for another entrance
        \t-WAIT until nightfall
        """))
        exterior_choice = choose()
        while exterior_choice not in MountainExterior.choices:
            exterior_choice = choose()
        return MountainExterior.choices.get(exterior_choice)

class ExteriorSearch(Scene):
    def enter(self, player):
        print(dedent("""
        You trace a wide, slow path through the local flora surrounding the mountain.
        After several hours of searching, you find yourself back where you started with
        nothing more accomplished than sore feet and dashed hopes. Night approaches...\n
        """))
        return 'ex_wait'

class ExteriorApproach(Scene):
    def enter(self, player):
        print(dedent("""
        You stride boldly towards the cave. As you approach, two GOBLIN GUARDS
        emerge from the darkness. They are chittering in a language that you do not understand,
        but you have seen enough combat to understand the cruel gleam in their eyes.
        You must FIGHT!\n\nPress ENTER to begin the combat.
        """))
        choose()
        combat(units.Unit('GOBLIN GUARD', 5, 4), 2, player)
        print(dedent("""
        Victory over the GOBLIN GUARDS is yours! You take a moment to
        examine their belongings. Their arms and armor are crude and worthless, but you
        find 1 GOLD and a COPPER KEY. You decide that you have found everything of value
        that these lowly guards have to offer and head deeper into the cave.\n
        Press ENTER to continue.
        """))
        player.stats['gold'] += 1
        player.stats['items'].append('a copper key')
        choose()
        return 'first_fork'

class ExteriorWait(Scene):
    def enter(self, player):
        print(dedent("""
        As the sun begins to set, you become aware of the toll your recent journey
        has taken on your body. However, you are in good shape and accustomed to travel,
        so it surprises you slightly when your eyelids grow heavy and begin to droop.
        Too late you realize your mistake: there are Mela flowers growing in the
        undergrowth around you! You recall hearing about these dangerous flowers
        in your youth: their pollen causes intense drowsiness in most mammals.
        You struggle to pull yourself away from the area lest prolonged exposure
        cause an unending slumber. You collapse some thirty feet away in a small
        clearing and drift to sleep...

        Press ENTER to TEST YOUR LUCK.
        """))

        choose()
        luck_test = randint(2, 12)
        print(f"You rolled {luck_test}. Your LUCK is {player.stats['luck']}")

        if luck_test <= player.stats['luck']:
            player.stats['luck'] -= 1
            print(dedent(f"""
            You are lucky. Your LUCK is reduced to {player.stats['luck']}. You
            awaken in the early dawn hours with nothing worse to show for last night's misadventure
            than a stiff back from sleeping on the cold ground.\n
            You decide that you have no option other than to proceed into the mountain through
            the cave entrance that you saw yesterday. You cautiously approach the low, wide opening.
            As you draw closer to the threshold, you see crude wooden chairs around a small table
            indicating that this area is typically occupied. You are relieved to find no guards
            in the immediate area; you surmise that they must be out on patrol and decide to continue
            deeper into the cave.\n
            Press ENTER to ready yourself and proceed...
            """))
            choose()
            return 'first_fork'

        else:
            print(dedent("""
            You are unlucky. You are discovered in the night by two patrolling
            GOBLIN GUARDS. The only mercy you experience is that the pollen-induced slumber
            prevented you from feeling the sword enter your back. Your adventure is over.
            """))
            input("Press ENTER to quit.\n> ")
            raise SystemExit

class FirstFork(Scene):
    def enter(self, player):
        print("hello")
        raise SystemExit
