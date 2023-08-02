"""Functions which operate to build a commmand prompt menu.

### Parameters:
----
item_types
    item slots to be considered.

### Functions:
----
setup()
    setup game
play(arena : Arena)
    main logic for the game, options to select knight for player, sell items
    belonging to player's knight, and begin combat round of tournament
select_knight(arena : Arena)
    select a knight to start as a player
train_menu(arena : Arena)
    increase a base stat to help improve performance in the tournament
sub_menu(arena : Arena, menu_type : int)
    menu for managing items; generates a list of equipment types and based
    on selection from main menu, will provide the option to change equiped an
    item, buy an item, or sell an item
equip_items(item_type : str, knight : Knight)
    select items to sell from a knight's inventory
buy_items(item_type : str, arena : Arena)
    select an item from the vendor to buy
sell_item(item_type : str, knight : Knight)
    select items to sell from a knight's inventory
heal_damage(arena : Arena)
    heal damage for player knight from Arena combat
get_name() -> str
    use error handling to retrieve name of a knight from user input
get_index(lower : int, upper : int) -> int
    used to error handle and verify index is appropriately selected
find_winner(arena : Arena)
    finds the winner of the tournament by finding the knight with the most
    gold
"""

# Import dependencies
from assessment import pandas, json
from assessment.classes import Arena, Knight, Weapon, Shield, Armour, load_file

item_types = ['weapons', 'shields', 'armours']

def setup():
    """Setup game."""

    # Instance Arena
    arena = Arena()

    # Setup menu loop
    while True:
        # Setup menu options
        print('0. Create New Knight')
        print('1. Start the Tournament')
        print('2. Exit')
        index = get_index(0, 2)

        # Add knight
        if index == 0:
            arena.add_knight(get_name())

        # Start the tournament
        elif index == 1:
            # If less than 2 knights, continues setup loop
            if len(arena.knights) < 2:
                print('At least 2 knights are required for the tournament.')

            else:
                play(arena)
                break

        # Exit game
        elif index == 2:
            print()
            print('Thanks for playing!')
            return

def play(arena: Arena):
    """Main logic for the game, options to select knight for player, sell items
    belonging to player's knight, and begin combat round of tournament.

    ### Parameters:
    ----
    arena : Arena
        arena housing knights for the main game
    """

    # Menu loop
    train = True
    while arena.level < 8:
        # Menu display
        print('\n' * 5)
        print('0. Begin Combat Round')
        print('1. Select Knight')
        print('2. Train Knight')
        print('3. Equip Items')
        print('4. Buy Items')
        print('5. Sell Items')
        print('6. Heal Damage')
        print('7. Exit')
        index = get_index(0, 7)

        # Begin combat round
        if index == 0:
            train = True
            arena.fight()

        # Move to knight selection menu
        elif index == 1:
            select_knight(arena)

        # Move to selling menu for player knight
        elif index == 2:
            if train:
                train_menu(arena)
                train = False

            # Error handling to ensure only one stat is boosted at a time
            else:
                print('You can only train one stat between rounds.')

        # Move to selling menu for player knight
        elif index == 3:
            sub_menu(arena, index)

        # Move to selling menu for player knight
        elif index == 4:
            sub_menu(arena, index)

        # Move to selling menu for player knight
        elif index == 5:
            sub_menu(arena, index)

        elif index == 6:
            heal_damage(arena)

        # Exit game
        elif index == 7:
            print()
            print('Thanks for playing!')
            break

    print()
    print('WINNER::')
    find_winner(arena)
    print('This concludes the tournament. Thank you for playing!')

def select_knight(arena: Arena):
    """Select a knight to start as a player.

    ### Parameters:
    ----
    arena : Arena
        arena housing knights for the main game
    """

    # Build knight selection menu
    print('\n' * 5)
    print('Select Knight')
    names = [knight.name for knight in arena.knights]
    for num, name in enumerate(names):
        print(f'{num}. {name}')

    # Add back option
    print(f'{len(names)}. Back')
    index = get_index(0, len(names))

    # Move selected knight to front of list
    if index < len(names):
        selected_knight = arena.knights[index]
        knights = [selected_knight]
        for num, knight in enumerate(arena.knights):
            if num != index:
                knights.append(knight)
        arena.knights = knights

        # Selection confirmation message
        print(f'{selected_knight.name} selected!')

def train_menu(arena: Arena) -> bool:
    """Increase a base stat to help improve performance in the tournament.

    ### Parameters:
    ----
    arena : Arena
        arena housing knights for the main game

    ### Returns:
    ----
    bool
        if a stat was increased return true, otherwise return false
    """

    # Build Training Menu
    trained = False
    knight = arena.knights[0]
    print('\n' * 5)
    print(f'0. Improve Max Health ..... {knight.max_health}')
    print(f'1. Improve Base Speed ..... {knight.base_speed}')
    print(f'2. Improve Base Damage .... {knight.base_damage}')
    print(f'3. Improve Base Defence ... {knight.base_defence}')
    print('4. Back')
    index = get_index(0, 4)

    # Go back to main menu
    if index == 4:
        trained = False

    # Improve max health
    elif index == 0:
        arena.knights[0].base_health = arena.knights[0].base_health + 10
        arena.knights[0].max_health = arena.knights[0].max_health + 10
        trained = True

    # Improve base speed
    elif index == 1:
        arena.knights[0].base_speed = arena.knights[0].base_speed + 2
        trained = True

    # Improve base damage
    elif index == 2:
        arena.knights[0].base_damage = arena.knights[0].base_damage + 5
        trained = True

    # Improve base defence
    elif index == 3:
        arena.knights[0].base_defence = arena.knights[0].base_defence + 5
        trained = True

    return trained

def sub_menu(arena: Arena, menu_type: int):
    """Menu for managing items; generates a list of equipment types and based
    on selection from main menu, will provide the option to change equiped an
    item, buy an item, or sell an item.

    ### Parameters:
    ----
    arena : Arena
        arena housing knights for the main game
    menu_type : int
        type of menu with which to proceed
    """

    # Menu loop
    while True:
        # Menu display
        for num, item_type in enumerate(item_types):
            print(f'{num}. {item_type.capitalize()}')
        print('3. Back')
        index = get_index(0, 3)

        if index != 3:
            # Change equipped items
            if menu_type == 3:
                equip_items(item_types[index], arena.knights[0])

            # Buy items
            elif menu_type == 4:
                buy_items(item_types[index], arena)

            # Sell items
            elif menu_type == 5:
                sell_items(item_types[index], arena.knights[0])

        # Back to main menu
        elif index == 3:
            break

def equip_items(item_type: str, knight: Knight):
    """Select items to sell from a knight's inventory.

    ### Parameters:
    ----
    item_type : str
        type of item to select for sale
    knight : Knight
        knight from whose inventory to sell items
    """

    # Loop for continuous sale if wanted by user
    while True:
        print(f'{item_type.capitalize()}::')
        # Display equipped item
        if knight.equipped[item_type] is not None:
            print('Equipped::')
            print(pandas.read_json(json.dumps([knight.equipped[item_type].__dict__])))
        else:
            print(f'No {item_type} equipped.')

        # Display list of items in inventory
        num_items = len(knight.inventory[item_type])
        if num_items > 0:
            print('Inventory::')
            knight.display_items(item_type)
        else:
            print(f'No {item_type} in inventory.')

        # Finish equip menu
        if knight.equipped[item_type] is not None:
            print(f'{num_items}. Unequip Item')

        print(f'{num_items + 1}. Back')
        index = get_index(0, num_items + 1)

        # Unequip item
        if index == num_items:
            knight.unequip_item(item_type)

        # Equip item
        elif index < num_items and num_items > 0:
            item = knight.inventory[item_type][index]
            knight.inventory[item_type].remove(item)
            knight.equip_item(item, item_type)

        # Go Back
        elif index == num_items + 1:
            return

def buy_items(item_type: str, arena: Arena):
    """Select an item from the vendor to buy.

    ### Parameters:
    ----
    item_type : str
        type of item to select for purchase
    arena : Arena
        arena housing knights for the main game
    """

    # Get player knight
    knight = arena.knights[0]

    # Build list of items for vendor
    keep = []
    for item in load_file(item_type):
        if item['level'] in [arena.level - 1, arena.level, arena.level + 1]:
            item.pop('level')
            keep.append(item)

    # Loop for purchasing items
    while True:
        print(f'{item_type.capitalize()}::')
        # Build purchase menu
        print(f'Player: {knight.name}' + ' ' * (30 - len(knight.name)) + f'Gold: {knight.gold}')
        print(pandas.read_json(json.dumps(keep)))
        print(f'{len(keep)}. Back')
        index = get_index(0, len(keep))

        if index < len(keep):
            # Error handling if cost exceeds player's gold
            if knight.gold >= keep[index]['value']:
                # Creates item
                if item_type == 'weapons':
                    item = Weapon(**keep[index])
                elif item_type == 'shields':
                    item = Shield(**keep[index])
                elif item_type == 'armours':
                    item = Armour(**keep[index])

                # Adds item to player inventory and removes gold
                knight.inventory[item_type].append(item)
                knight.gold -= keep[index]['value']

            # Error message if cost exceeds player's gold
            else:
                print('It seems that piece costs too much for you at the moment.')

        # Go back
        else:
            return

def sell_items(item_type: str, knight: Knight):
    """Select items to sell from a knight's inventory.

    ### Parameters:
    ----
    item_type : str
        type of item to select for sale
    knight : Knight
        knight from whose inventory to sell items
    """

    # Loop for continuous sale if wanted by user
    while True:
        num_items = len(knight.inventory[item_type])
        # Display items to select for sale
        if num_items > 0:
            print(f'{item_type.capitalize()}::')
            knight.display_items(item_type)
            print(f'{num_items}. Back')
            index = get_index(0, num_items)

            # Sell item
            if index < num_items:
                knight.sell_item(index, item_type)

            # Go Back
            else:
                return

        # Error handling if there are no items to sell of the given item type
        else:
            print(f'There are no {item_type} to sell.')
            return

def heal_damage(arena: Arena):
    """Heal damage for player knight from Arena combat.

    ### Parameters:
    ----
    arena : Arena
        arena housing knights for the main game
    """

    # End process if no gold in player's coin purse
    if arena.knights[0].gold == 0:
        print('I\'m sorry, but you need some gold in order to heal!')

    # End process if player already at max health
    elif arena.knights[0].base_health == arena.knights[0].max_health:
        print('You\'re perfectly healthy, I can\'t help you.')

    else:
        # Assign healing amounts
        heal_amount_upper = 0
        damage = int(arena.knights[0].max_health - arena.knights[0].base_health)
        if damage <= arena.knights[0].gold:
            heal_amount_upper = damage

        else:
            heal_amount_upper = arena.knights[0].gold

        heal_amount_lower = 1
        heal_amount_mid = int((heal_amount_upper + heal_amount_lower) / 2)

        # Healing menu
        print('Healer:')
        print(f'0. Max Healing: {heal_amount_upper} pts')
        print(f'1. Mid Healing: {heal_amount_mid} pts')
        print(f'2. Min Healing: {heal_amount_lower} pts')
        print('3. Back')
        index = get_index(0, 3)

        # Heal max amount
        if index == 0:
            arena.knights[0].base_health += heal_amount_upper
            arena.knights[0].gold -= heal_amount_upper

        # Heal mid amount
        elif index == 1:
            arena.knights[0].base_health += heal_amount_mid
            arena.knights[0].gold -= heal_amount_mid

        # Heal min amount
        elif index == 2:
            arena.knights[0].base_health += heal_amount_lower
            arena.knights[0].gold -= heal_amount_lower

        # Go back
        elif index == 3:
            return

def get_name() -> str:
    """Use error handling to retrieve name of a knight from user input.

    ### Returns:
    ----
    str
        name of the knight based on user input
    """

    # Error handling loop
    while True:
        name = input('\nPlease enter the name of a knight: ')
        # If user input is empty, continue loop
        if len(name) == 0:
            print('Please enter a name, you seemed to have missed it last time.')

        else:
            # Capitolize each word in user input
            final_name = ''
            for word in name.split(' '):
                final_name += word.capitalize() + ' '

            return final_name.strip()

def get_index(lower: int, upper: int) -> int:
    """Used to error handle and verify index is appropriately selected.

    ### Parameters:
    ----
    lower : int
        lower bound for index
    upper : int
        upper bound for index

    ### Returns:
    ----
    int
        index presenting user choice
    """

    # Loop for error handling
    while True:
        # Try block to get an integer from user input
        try:
            index = int(input('\nPlease enter the index of your selection: '))

        except ValueError:
            print('Please enter a numeric index to represent your selection.')

        else:
            # Error handle if index is too small
            if index < lower:
                print(f'Please keep your index selection greater than or equal to {lower}.')

            # Error handle if index is too big
            elif index > upper:
                print(f'Please keep your index selection less than or equal to {upper}.')

            else:
                return index

def find_winner(arena: Arena):
    """Finds the winner of the tournament by finding the knight with the most
    gold.

    ### Parameters:
    ----
    arena : Arena
        arena housing knights for the main game
    """

    # Get knight names and gold
    knights = {}
    for knight in arena.knights:
        knights[knight.name] = knight.gold

    # Find knight who has the most gold and print their win string
    max_gold = max(knights.values())
    for name, gold in knights.items():
        if gold == max_gold:
            for knight in arena.knights:
                if knight.name == name:
                    knight.win_string()
                    return
