"""Classes used to store and process data for knight game.

### Classes
----
Equipment(min_stat : float, max_stat : float, weight : float)
    class to define items/pieces of equipment (parent class for Armour,
    Shield, and Weapon)
Armour(name : str, min_stat : float, max_stat : float, weight : float, value : int)
    class to define pieces of armour
Shield(name : str, min_stat : float, max_stat : float, weight : float, value : int)
    class to define shields
Weapon(name : str, min_stat : float, max_stat : float, weight : float, value : int)
    class to define weapons
Knight(name : str)
    class to define a knight fighting in the tournament
Arena()
    class for the Arena which manages combat, interactions between entities,
    and generates visuals

### Functions
display_combat(player : Knight, opponent : Knight, message : str)
    display for each stage in a combat
load_file(file_name : str) -> list
    loads json file to product a list of dictionaries representing
    serialized equipment
generate_item(level : int, item_type : str)
    generate a piece of equipment based on the level of the arena and type
    of weapon

### Parameters:
----
root_dir
    location of armours, shields, and weapons serialized values
"""

# Import dependencies
from assessment import random, choice, os, sqrt, json, pandas, sleep

root_dir = os.path.dirname(os.path.abspath(__file__)) + '/'


class Equipment():
    """Class to define items/pieces of equipment (parent class for Armour,
    Shield, and Weapon).

    ### Attributes:
    ----
    min_stat : float
        minimum stat of the item
    max_stat : float
        maximum stat of the item
    weight : float
        weight of the item

    ### Methods:
    ----
    defend() -> float
        provides combined defense stat for the item
    attack() -> float
        provides combined attack stat for the item
    """

    def __init__(self, min_stat: float, max_stat: float, weight: float):
        self.min_stat = min_stat
        self.max_stat = max_stat
        self.weight = weight

    def defend(self) -> float:
        """Provides combined defense stat for the armour.

        ### Returns:
        ----
        float
            combined denfense stat for the armour
        """

        rand = random()
        defence = 0
        # Critical Hit
        if rand <= 0.1:
            defence = self.max_stat * 2.5 * self.weight / 50

        # Critical Failure
        elif rand >= 0.9:
            defence = 0

        # Standard Hit
        else:
            defence = ((self.max_stat - self.min_stat) * random() + self.min_stat)
            defence = defence * self.weight / 50

        return defence

    def attack(self) -> float:
        """Provides combined attack stat for the armour.

        ### Returns:
        ----
        float
            combined attack stat for the armour
        """

        rand = random()
        damage = 0
        # Critical Hit
        if rand <= 0.1:
            damage = self.max_stat / sqrt(self.weight)

        # Critical Failure
        elif rand >= 0.9:
            damage = 0

        # Standard Hit
        else:
            damage = self.min_stat / sqrt(self.weight)

        return damage


class Armour(Equipment):
    """Class to define pieces of armour.

    ### Attributes:
    ----
    name : str
        name of the armour
    weight : float
        weight of the armour
    value : int
        value of piece in gold pieces
    """

    def __init__(self, name: str, min_stat: float, max_stat: float, weight: float, value: int):
        self.name = name
        self.value = value
        super().__init__(min_stat, max_stat, weight)


class Shield(Equipment):
    """Class to define shields.

    ### Attributes:
    ----
    name : str
        name of the shield
    value : int
        value of piece in gold pieces
    """

    def __init__(self, name: str, min_stat: float, max_stat: float, weight: float, value: int):
        self.name = name
        self.value = value
        super().__init__(min_stat, max_stat, weight)


class Weapon(Equipment):
    """Class to define weapons.

    ### Attributes:
    ----
    name : str
        name of the weapon
    value : int
        value of piece in gold pieces
    """

    def __init__(self, name: str, min_stat: float, max_stat: float, weight: float, value: int):
        self.name = name
        self.value = value
        super().__init__(min_stat, max_stat, weight)

    def defend(self) -> float:
        """Provides combined defense stat for the weapon.

        ### Returns:
        ----
        float
            combined defense stat for the weapon
        """

        rand = random()
        defence = 0
        # Critical Hit
        if rand <= 0.1:
            defence = self.max_stat * 1.5 * self.weight / 100

        # Critical Failure
        elif rand >= 0.1:
            defence = self.min_stat * 0.5 * self.weight / 100

        # Standard Hit
        else:
            defence = (self.max_stat - self.min_stat * 0.5) * random() + self.min_stat * 0.5
            defence = defence * self.weight / 100

        return defence

    def attack(self) -> float:
        """Provides combined attack stat for the weapon.

        ### Returns:
        ----
        float
            combined attack stat for the weapon
        """

        rand = random()
        damage = 0
        # Critical Hit
        if rand <= 0.1:
            damage = self.max_stat * 3.5 / sqrt(self.weight)

        # Critical Failure
        elif rand >= 0.1:
            damage = self.min_stat * 1.5 / sqrt(self.weight)

        # Standard Hit
        else:
            damage = (self.max_stat - self.min_stat * 1.5) * random() + self.min_stat * 1.5
            damage /= sqrt(self.weight)

        return damage


class Knight():
    """Class to define a knight fighting in the tournament.

    ### Attributes:
    ----
    name : str
        name of the knight
    gold : int
        amount of gold accumulated by the knight
    weight : float
        total weight of equipment equiped
    equipment : dict
        contains all equipped pieces of equipment
    base_health : int
        starting health pool
    max_health : int
        total health pool
    base_damage : int
        starting base damage
    base_defece : int
        starting base defence
    base_speed : int
        starting base speed
    speed : int
        speed of the knight
    inventory : dict
        contains all extra pieces of equipment awarded by the tournement

    ### Methods:
    ----
    win_string()
        string to display if the knight wins
    equip_item(armour: Armour)
        equips the armour submitted
    attack() -> tuple
        produces a tuple of speed stat and combined attack stat
    defend() -> tuple
        produces a tuple of speed stat and combined defence stat
    take_damage(damage: float) -> tuple
        applies damage inflicted; if it exceeds remaining health return
        items and gold
    win(loot: dict, gold: int)
        distributes loot and gold from winning a round to the inventory
    sell_item(name: str, gold: int, item_type: str)
        removes an item from the inventory in exchange for gold
    display_items(item_type: str)
        displays all items in knight's inventory using a pandas dataframe
        corresponding to the item_type
    """

    item_types = ['weapons', 'shields', 'armours']
    gold = 0
    weight = 0
    equipped = {'weapons': None, 'shields': None, 'armours': None}
    inventory = {'weapons': [], 'shields': [], 'armours': []}

    def __init__(self, name: str):
        self.name = name
        self.base_health = int(75 * random() + 75)
        self.base_damage = int(10 * random() + 10)
        self.base_defence = int(5 * random() + 5)
        self.base_speed = int(7.5 * random() + 7.5)
        self.max_health = self.base_health
        self.speed = self.base_speed

    def win_string(self):
        """String to display if the knight wins."""

        # get equipped items for display
        items = []
        for item_type in self.item_types:
            # Add dictionary of item equipped in item_type slot
            if self.equipped[item_type] is not None:
                item = self.equipped[item_type].__dict__

            # Build empty dictionary if no item is equipped in item_type slot
            else:
                item = {
                    'name': None,
                    'min_stat': None,
                    'max_stat': None,
                    'weight': None,
                    'value': None
                }

            # Add slot name to dictionary
            item['item_type'] = item_type
            items.append(item)

        # Build and print display string containing knight stats
        display = ''
        display += f'Name: {self.name}'
        display += ' ' * (30 - len(self.name))
        display += f'Gold: {self.gold}\n'
        display += f'Base Speed: {self.base_speed}'
        display += ' ' * (23 - len(str(self.base_speed)))
        display += f'Speed: {self.speed}\n'
        display += f'Health: {self.base_health}'
        display += ' ' * (22 - len(str(self.base_health)))
        display += f'Max Health: {self.max_health}\n'
        display += f'Base Damage: {self.base_damage}'
        display += ' ' * (15 - len(str(self.base_damage)))
        display += f'Base Defence: {self.base_defence}\n'
        display += 'Equipped::\n'
        print(display)

        # Build and print display of equipped items
        print(pandas.read_json(json.dumps(items)))

    def unequip_item(self, item_type: str):
        """Unequip an equipped item and store in the knight's inventory.

        ### Parameters:
        ----
        item_type : str
            can be 'weapons', 'shields', or 'armours' - type of item
        """

        self.weight -= self.equipped[item_type].weight
        self.inventory[item_type].append(self.equipped[item_type])
        self.equipped[item_type] = None

    def equip_item(self, item: Equipment, item_type: str):
        """Equips the item submitted.

        ### Parameters:
        ----
        item : Equipment
            can be a Weapon, Shield, or Armour object - item to be equipped
        item_type : str
            can be 'weapons', 'shields', or 'armours' - type of item
        """

        # If an item is equipped, adjust weight and move item to inventory.
        if self.equipped[item_type] is not None:
            self.unequip_item(item_type)

        self.equipped[item_type] = item
        self.weight += item.weight

    def _calculate_speed(self):
        """Calculuate speed stat."""

        if self.weight > 0:
            self.speed = int(self.base_speed ** 2 / sqrt(self.weight))
        else:
            self.speed = self.base_speed

    def attack(self) -> tuple:
        """Produces a tuple of speed stat and combined attack stat.

        ### Returns:
        ----
        tuple
            contains speed stat and attack stat (speed, attack)
        """

        damage = self.base_damage
        self._calculate_speed()

        # Adds attack stat of all equipped items.
        for item_type in self.item_types:
            if self.equipped[item_type] is not None:
                damage += self.equipped[item_type].attack()

        return (self.speed, int(damage))

    def defend(self) -> tuple:
        """Produces a tuple of speed stat and combined defence stat.

        ### Returns:
        ----
        tuple
            contains speed stat and defence stat (speed, defence)
        """

        defence = self.base_defence
        self._calculate_speed()

        # Adds attack stat of all equipped items.
        for item_type in self.item_types:
            if self.equipped[item_type] is not None:
                defence += self.equipped[item_type].defend()

        return (self.speed, int(defence))

    def take_damage(self, damage: float) -> tuple:
        """Applies damage inflicted; if it exceeds remaining health return
        items and gold.

        ### Parameters:
        ----
        damage : float
            damage to be inflicted

        ### Returns:
        ----
        tuple
            if the damage infliced exceeds remaining health, return all items
            and gold as a tuple (items, gold), otherwise returns None
        """

        loot = None
        if damage < self.base_health:
            self.base_health -= damage

        else:
            loot = self._lose()

        return loot

    def _lose(self) -> tuple:
        """Prepares the contents to be submitted when losing the tournament.

        ### Returns:
        ----
        tuple
            returns all items and gold as a tuple (items, gold)
        """

        # Stores gold and all items as tuple
        gold_lost = int(self.gold / 2)
        forfeit = (self.inventory, gold_lost)

        # Reset character health, gold, and inventory
        self.base_health = self.max_health
        self.gold -= gold_lost
        self.inventory['weapons'] = []
        self.inventory['shields'] = []
        self.inventory['armours'] = []

        # Train to improve for the next combat round
        self.base_speed += 2
        self.base_damage += 5
        self.base_defence += 5
        self.max_health += 10

        return forfeit

    def win(self, loot: dict, gold: int):
        """Distributes loot and gold from winning a round to the inventory.

        ### Parameters:
        ----
        loot : dict
            dictionary containing all items from the loser of the round
        gold : int
            gold from the loser of the round
        """

        # If there are any weapons in the loot bag, adds them to the inventory.
        if len(loot['weapons']) > 0:
            self.inventory['weapons'].extend(loot['weapons'])

        # If there are any shields in the loot bag, adds them to the inventory.
        if len(loot['shields']) > 0:
            self.inventory['shields'].extend(loot['shields'])

        # If there are any armours in the loot bag, adds them to the inventory.
        if len(loot['armours']) > 0:
            self.inventory['armours'].extend(loot['armours'])

        self.gold += gold

    def sell_item(self, index: int, item_type: str):
        """Remove an item from the inventory in exchange for gold.

        ### Parameters:
        ----
        index : int
            index of the item to be sold in the inventory
        item_type: str
            type of item, either weapons, shields, or armours
        """

        self.gold += self.inventory[item_type][index].value
        self.inventory[item_type].remove(self.inventory[item_type][index])

    def display_items(self, item_type: str):
        """Displays all items in knight's inventory using a pandas dataframe
        corresponding to the item_type.
        """

        items = []
        # Converts Weapon objects into dictionaries
        for item in self.inventory[item_type]:
            items.append(item.__dict__)

        # Prints title and dataframe for visualization
        print(pandas.read_json(json.dumps(items)))


class Arena():
    """Class for the Arena which manages combat, interactions between entities,
    and generates visuals.

    ### Attributes:
    ----
    level : int
        manages loot level so that knights get stronger as they win
    knights : list
        list of knights in the arena queued up to fight
    gold : int
        amount of gold to reward the winner of each round

    ### Methods:
    ----
    add_knight(name: str)
        builds a Knight object to add to the knights attribute
    fight()
        manages combat between first knight (player) and a random other knight
        (opponent)
    """

    item_types = ['armours', 'shields', 'weapons']

    def __init__(self):
        self.level = 0
        self.knights = []
        self.gold = 5

    def add_knight(self, name: str):
        """Builds a Knight object to add to the knights attribute.

        ### Parameters:
        ----
        name : str
            name of the knight
        """

        # Instance Knight object
        knight = Knight(name)

        # Equip knight
        for item_type in self.item_types:
            knight.equip_item(generate_item(self.level, item_type), item_type)

        # Add knight to arena
        self.knights.append(knight)

    def fight(self):
        """Manages combat between first knight (player) and a random other
        knight (opponent).
        """

        player = self.knights[0]
        # Randomly selects opponent
        opponent = choice(self.knights[1:])

        still_going = True
        # Combat visual header
        print('\n' * 10)
        print('*' * 10)
        print(f'ROUND {self.level + 1}')
        print(f'{self.gold} gold in the pot')
        print('*' * 10)
        timer = 0
        # First display of combat visual
        display_combat(player, opponent, 'Start!')
        while still_going:
            # Alternate between who is attacking and who is defending
            for num in [0, 1]:
                if num == 0:
                    win, message = self._combat(player, opponent)

                elif num == 1:
                    win, message = self._combat(opponent, player)

                # Display combat visual with status change
                display_combat(player, opponent, message)
                if win:
                    still_going = False
                    break

            if timer > 9:
                still_going = False
                print('The duel was a draw. Neither side wins!')

            timer += 1

    def _combat(self, attacker: Knight, defender: Knight) -> tuple:
        """Manages each combat between an attacker and a defender.

        ### Parameters:
        ----
        attacker : Knight
            knight attacking
        defender : Knight
            knight defending

        ### Returns:
        ----
        tuple
            (<win: bool>, <display_message: str>)
        """

        # Get attack and defence speeds and damage/defence respectively
        attack_speed, attack_damage = attacker.attack()
        defend_speed, defend_defence = defender.defend()

        loot = None
        # Account for greater attacker speed
        if attack_speed >= defend_speed * 2:
            loot = defender.take_damage(attack_damage)
            message = f'{defender.name} wasn\'t fast enough and couldn\'t block'
            message += f' {attacker.name}\'s attack! {attack_damage} damage delt.'

        # Account for greater defender speed
        elif defend_speed >= attack_speed * 2:
            message = f'{defender.name} was too fast and successfully'
            message += f' dodged {attacker.name}\'s attack! 0 damage delt.'

        # Standard skirmish - attacker lands a blow
        elif attack_damage > defend_defence:
            loot = defender.take_damage(attack_damage - defend_defence)
            message = f'{defender.name} was able to block {attacker.name}\'s'
            message += f' attack! {attack_damage - defend_defence} damage made it through.'

        # Standard skirmish - attacker blocked successfully
        elif defend_defence >= attack_damage:
            message = f'{defender.name} was able to completely block'
            message += f' {attacker.name}\'s attack! 0 damage delt.'

        if loot is not None:
            # Generate display message
            message = f'{defender.name} was knocked out! {attacker.name} WON!!'

            # Distribute loot from defender to attacker
            attacker.win(loot[0], loot[1])
            attacker.gold += self.gold

            # Increment level
            self.level += 1

            # Re-equip attacker with better equipment
            for item_type in self.item_types:
                attacker.equip_item(generate_item(self.level, item_type), item_type)

            # Move defender to end of list of knights
            if defender != self.knights[0]:
                self.knights.remove(defender)
                self.knights.append(defender)

            # Increment gold pool
            self.gold = int(self.gold + self.gold * 1.25)

        return ((loot is not None), message)


def display_combat(player: Knight, opponent: Knight, message: str):
    """Display for each stage in a combat.

    ### Parameters:
    ----
    player : Knight
        knight representing the player
    opponent : Knight
        knight opposing the player
    """

    print('\n' * 3)

    # Player information
    display_name = f'Player: {player.name}'
    display_name += ' ' * (30 - len(player.name))
    display_name += f'Gold: {player.gold}'
    print(display_name)
    print(f'Health: {player.base_health} / {player.max_health}')

    # Player health bar
    health_bar = int(player.base_health / player.max_health * 50)
    print(' ' * (50 - health_bar) + '=' * health_bar)

    # Combat stage information
    print()
    print(message)
    print()

    # Opponent information
    display_name = f'Opponent: {opponent.name}'
    display_name += ' ' * (30 - len(opponent.name))
    display_name += f'Gold: {opponent.gold}'
    print(display_name)
    print(f'Health: {opponent.base_health} / {opponent.max_health}')

    # Opponent health bar
    health_bar = int(opponent.base_health / opponent.max_health * 50)
    print(' ' * (50 - health_bar) + '=' * health_bar)

    # Keep display fixed on screen for 3 seconds
    sleep(3)

def load_file(file_name: str) -> list:
    """Loads json file to product a list of dictionaries representing
    serialized equipment.

    ### Parameters:
    ----
    file_name : str
        name of file to be loaded

    ### Returns:
    ----
    list
        list of dictionaries representing serialized equipment
    """

    file_path = root_dir + file_name + '.json'
    with open(file_path, mode='r+', encoding='utf-8') as file:
        return json.load(file)

def generate_item(level: int, item_type: str) -> Equipment:
    """Generate a piece of equipment based on the level of the arena and type
    of weapon.

    ### Parameters:
    ----
    level : int
        level of the arena's loot pool
    item_type : str
        type of item to produce

    ### Returns:
    ----
    Equipment
        piece of equipment produced within 1 level of arena level
    """

    keep = []
    # Get all items belonging to item type within 1 level of arena level
    for item in load_file(item_type):
        if item['level'] in [level - 1, level, level + 1]:
            keep.append(item)

    # Randomly choose one of the items selected
    item = choice(keep)
    item.pop('level')

    # Generate weapon
    equipmt = None
    if item_type == 'weapons':
        equipmt = Weapon(**item)

    # Generate shield
    elif item_type == 'shields':
        equipmt = Shield(**item)

    # Generate armour
    elif item_type == 'armours':
        equipmt = Armour(**item)

    return equipmt
