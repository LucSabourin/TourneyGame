## WYWM Principles of Programming (Python) Assessment

The code accompanying this document is used for a program built to play a simple knight game, which allows you to
create knights, manage their inventories and skills, and engage in a tournement of combat.

## Getting Started

Start by running the setup.bat which will do the following:
1. Create a virtual environment from which to run this program;
2. Activate the virtual environment; and
3. Pip install any dependent libraries (from requirements.txt) for the virtual environment.
If you are not running a windows machine, perform the same steps based on your OS.

Once the setup.bat has completed, run the run.bat file which will do the following:
1. Activate the virtual environment; and
2. Start the game.

## Game Info

In order to engage in the tournament at least 2 knights need to be created. While the tournament _can_ run with 2
knights, it runs better with more than 2 knights (i.e. you have a better chance of winning).

Once the tournament has started, if you leave, you need to restart the process as it is similar to forfeiting the
tournament.

Before each round of combat, you will have a few things you can do to help improve your odds of success in the arena:
1. Train some skills (can only be done once per round):
    a) you can train to increase you vitality making you last longer in combat;
    b) you can train to increase you speed making you harder to hit and harder to dodge in combat;
    c) you can train to increase you base damage making each hit you land hit harder; and
    d) you can train to increase you base defence making each hit you receive hit softer.
2. Change equipped items:
    a) you can unequip any equipped items and store in your inventory; and
    b) you can replace any equipped items with a spare item in your inventory
3. Buy additional items (requires gold)
4. Sell spare items from inventory (requires items in inventory)
5. Heal damage received (requires gold)

Each combat, the winner will collect any spare weapons in the loser's inventory as well as all gold from the pot and
half the gold from the loser's coin purse. The winner will also be awarded a new set of equipment which may or may not
improve combat depending on their build (a mace and plate armour will slow you down more than a sword and mail armour).
The loser will also be automatically trained in vitality, speed, damage, and defence to help balance the new equipment
the winner receives.

Combat is run automatically, using calculations for criticial hits and critical failures for each piece of equipment
for either combantant. An attacker with a critical hit against a defender who experiences a critical failure can
make the difference between a one hit take down and a long grueling battle. There is a 'move' limit on combat so if
an immovable object hits an unstoppable force, the round will conclude as a draw for the player to move some stuff
around to better perform.

The tournament will automatically complete after 8 rounds of combat.

At the end of the tournement either after the completion of 8 rounds or when the player quits, the knight with the most
amount of gold will be listed as the winner (if all the knights have 0 gold).
