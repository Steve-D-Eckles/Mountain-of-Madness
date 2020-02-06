from random import randint
from textwrap import dedent
import units


class Scene(object):
    """Contains methods for use by child classes

    Methods:
        enter: prints a description of the scene and expected inputs to the user
        choose: gets input from the user, checks for keywords, and produces
                output or returns the keywords
        repeat_input: constructs a list of available options for the current scene
        combat: creates a combat scenario
    """

    def enter(self, player):
        print("You shouldn't be here. Whoops!")
        raise SystemExit

    def choose(self):

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

    def repeat_input(self, args):
        result = ['Pick one:\n']
        for arg in args:
            result.append(f'\t-{arg}\n')
        return ''.join(result)

    def combat(self, enemy, count, player):
        """Handle combat encounters using Unit and Player objects from mountain_units"""
        for i in range(1, count + 1):
            print(f"{enemy.name} {i} prepares to fight!", end='')
            self.choose()
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

                self.choose()
                if i_stamina == 0:
                    print(f"{enemy.name} {i} has been slain!")
                    self.choose()
                if player.stats['stamina'] == 0:
                    print("You have failed! Your adventure is over.")
                    input("Press ENTER to quit.\n> ")
                    raise SystemExit
        return

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
        exterior_choice = self.choose()
        while exterior_choice not in MountainExterior.choices:
            print(self.repeat_input(['APPROACH the cave', 'SEARCH for another entrance', 'WAIT until nightfall']))
            exterior_choice = self.choose()
        return MountainExterior.choices.get(exterior_choice)

class ExteriorSearch(Scene):
    def enter(self, player):
        print(dedent("""
        You trace a wide, slow path through the local flora surrounding the mountain.
        After several hours of searching, you find yourself back where you started with
        nothing more accomplished than sore feet and dashed hopes. Night approaches...
        """))
        return 'ex_wait'

class ExteriorApproach(Scene):
    def enter(self, player):
        print(dedent("""
        You stride boldly towards the cave. As you approach, two GOBLIN GUARDS
        emerge from the darkness. They are chittering in a language that you do not understand,
        but you have seen enough combat to understand the cruel gleam in their eyes.
        You must FIGHT!
        Press ENTER to begin the combat.
        """))
        self.choose()
        self.combat(units.Unit('GOBLIN GUARD', 5, 4), 2, player)
        print(dedent("""
        Victory over the GOBLIN GUARDS is yours! You take a moment to
        examine their belongings. Their arms and armor are crude and worthless, but you
        find 1 GOLD and a COPPER KEY. You decide that you have found everything of value
        that these lowly guards have to offer and head deeper into the cave.\n
        Press ENTER to continue.
        """))
        player.stats['gold'] += 1
        player.stats['items'].append('a copper key')
        self.choose()
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

        self.choose()
        luck_test = randint(2, 12)
        print(f"You rolled {luck_test}. Your LUCK is {player.stats['luck']}")

        if luck_test <= player.stats['luck']:
            player.stats['luck'] -= 1
            print(dedent(f"""
            You are lucky. Your LUCK is reduced to {player.stats['luck']}.
            You awaken in the early dawn hours with nothing worse to show for last
            night's misadventure than a stiff back from sleeping on the cold ground.
            You decide that you have no option other than to proceed into the mountain through
            the cave entrance that you saw yesterday. You cautiously approach the low, wide opening.
            As you draw closer to the threshold, you see crude wooden chairs around a small table
            indicating that this area is typically occupied. You are relieved to find no guards
            in the immediate area; you surmise that they must be out on patrol and decide to continue
            deeper into the cave.\n
            Press ENTER to ready yourself and proceed...
            """))
            self.choose()
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
        print(dedent("""
        The light lessens as you descend a steady slope into the depths of the cave.
        You see a fork in the tunnel ahead, but your limited dark vision does not allow you
        to see far down either path ahead of you. Will you:
        \t-Take the path on the LEFT
        \t-Take the path on the RIGHT
        """))

        fork_response = self.choose()
        while fork_response == '' or not fork_response in ['left', 'right']:
            print(self.repeat_input(['Take the path on the LEFT', 'Take the path on the RIGHT']))
            fork_response = self.choose()

        if fork_response == 'left':
            return 'first_fork_left'
        elif fork_response == 'right':
            return 'first_fork_right'

class FirstForkLeft(Scene):
    def enter(self, player):
        print(dedent("""
            This passage widens as you continue along its length until it terminates
            in a large room. You see several simple beds along the walls, each
            with a simple wooden container at its foot. There is also a large
            round table at the other end of the room, with one of its chairs currently
            occupied by a large, snoring mass. On the other side of the table is an
            iron door. There is also a wooden door directly across from you.
            Would you like to:
            \t-Attempt to exit the room through the WOODEN DOOR
            \t-Attempt to exit the room through the IRON DOOR
            \t-Search the FOOTLOCKERS
            \t-Search the sleeping BUGBEAR
        """))

        barracks_response = self.choose()
        if barracks_response == 'footlockers':
            return 'footlockers'
        else:
            print("Thanks for playing the DEMO. Support me on patreon for the latest release.")
            raise SystemExit

class Footlockers(Scene):
    def enter(self, player):
        print(dedent("""
        You quickly but quietly search through each of the footlockers. Each contains
        simple clothing and other assorted personal items, but none appear to be of
        any value; however, the final footlocker looks nicer than the others and
        is the only one that appears to actually be locked. If you have a COPPER KEY,
        you may OPEN the locker. Otherwise, pick one:
        \t-Attempt to exit the room through the WOODEN DOOR
        \t-Attempt to exit the room through the IRON DOOR
        \t-Search the sleeping BUGBEAR
        """))
        footlocker_response = self.choose()
        if footlocker_response == 'open':
            if 'a copper key' in player.stats['items']:
                print(dedent("""
                You open the footlocker and find a Ring of Luck. You put it on your finger and gain
                one LUCK.
                """))
                player.stats['items'].append('a Ring of Luck')
                player.stats['luck'] += 1
            else:
                print("You don't have the key.")

            print("Thanks for playing the DEMO. Support me on patreon for the latest release.")
            raise SystemExit

        else:
            print("Thanks for playing the DEMO. Support me on patreon for the latest release.")
            raise SystemExit

class FirstForkRight(Scene):
    def enter(self, player):
        print(dedent("""
        You head down the tunnel to the right. After only a few moments of walking,
        you come upon a closed wooden door. The door is locked, but you could try
        to ram it down with your shoulder. Would you like to:
        \t-RAM the door
        \t-Turn BACK
        """))

        door_response = self.choose()
        while door_response == '' or not door_response in ['ram', 'back']:
            print(self.repeat_input(['RAM the door', 'Turn BACK']))
            door_response = self.choose()

        if door_response == 'ram':
            return 'door_ram'
        elif door_response == 'back':
            print("You head back to where the path forked and proceed the other way.")
            return 'first_fork_left'

class DoorRam(Scene):
    def enter(self, player):
        print(dedent("""
        You stretch out your shoulder and ready yourself to charge the unsuspecting
        door. You must Test Your Luck. For each failure, you will take 2 points of
        STAMINA damage. You may try as many times as you like, or you may turn BACK
        at any time.
        Press ENTER to TEST YOUR LUCK
        """))

        while True:
            ram_response = self.choose()
            if ram_response == 'back':
                return 'first_fork_left'
            luck_test = randint(1, 6) + randint(1, 6)
            print(f"You rolled {luck_test}. Your LUCK is {player.stats['luck']}")
            if luck_test > player.stats['luck']:
                player.stats['stamina'] -= 2
                if player.stats['stamina'] <= 0:
                    print(dedent("""
                    Bleeding but determined, you throw your broken body once more
                    upon the unrelenting wooden door. You take a moment to reflect
                    on how your end was brought about by an inanimate object, and
                    you wonder what the sorcerer's minions will think when they
                    find you here.
                    Your vision fades to black. Your adventure is over.
                    Press ENTER to exit.
                    """))
                    input('> ')
                    raise SystemExit
                else:
                    print(dedent(f"""
                    You are unlucky and fail to bust open the door. Your STAMINA is
                    {player.stats['stamina']}. Try again or go BACK.
                    """))
                    continue
            else:
                player.stats['luck'] -= 1
                return 'pit'

class Pit(Scene):
    def enter(self, player):
        print(dedent(f"""
        You are Lucky. Your LUCK is reduced by one and is now {player.stats['luck']}.
        The rusted bolt on the other side of the door breaks free from the wall
        with a resounding crack as you barrel at full force into the door. The door
        flies open and you fall headlong into the room as your momentum carries you
        forward; however, you quickly realize that the ground won't be able to break
        your fall because there isn't any ground here at all! You are unable to
        stop yourself from being impaled on the spikes at the bottom of the pit trap.
        Your adventure is over.
        Press ENTER to exit.
        """))
        input('> ')
        raise SystemExit
