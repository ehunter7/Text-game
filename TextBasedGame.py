# Eric Hunter

# Global variables that control the game settings

# Starting location
starting_location = 'Great Hall'

# Exit condition
exit_condition = 'exit'

# Rooms with villain
villain_room = 'Snapes Office'

# Number of items to win
number_of_items = 6


# Class that contains the players stats
class Player:
    # constructor
    def __init__(self, room=starting_location):  # Sets the starting position to great Hall unless specified otherwise
        self._current_room = room
        self._inventory = []  # List containing all collected items

    # Modifiers

    def set_current_room(self, room):
        self._current_room = room

    def add_inventory(self, item):
        self._inventory.append(item)

    def remove_inventory(self):
        self._inventory[:] = []

    # Accessors

    def get_current_room(self):
        return self._current_room

    def get_inventory(self):
        return self._inventory

    def inventory_count(self):
        return len(self._inventory)


def show_instructions():
    # print a main menu and the commands
    border()
    print("{}Provoking the Wizard Game".format(' ' * 4))
    print("Commandeer 6 items to win the game, or be caught by the groundskeeper.")
    print("Move commands: go South, go North, go East, go West")
    print("Add to Inventory: get 'item name'")
    print('Enter help to repeat the instructions')
    border()


def move_between_rooms(user_input, rooms, current_room):
    # new line for readability
    print()

    # takes the direction the user would like to travel and trims white space and capitalizes the word.
    direction = user_input.strip().title()

    # Checks if direction of travel is available in current room
    if rooms[current_room].get(direction):
        return rooms[current_room].get(direction)

    else:
        print('Invalid direction')
        return None


# Checks if the item the user is trying to get is in the current room
def get_item(user_input, rooms, current_room):
    # Capitalizes the item
    item = user_input.title()

    if rooms[current_room].get('item') == item:
        return item
    else:
        print('The {} is not in this room'.format(item))
        return None


# Displays the losing game prompt and exits
def villain_prompt(player):
    print('You\'ve been caught in {}'.format(villain_room))
    player.set_current_room('exit')


def help_prompt():
    print("Move commands: go South, go North, go East, go West")
    print("Add to Inventory: get 'item name'")


def play_again_prompt():
    # Endless loop that will run until a return statement is met.
    while True:
        try_again_input = input('Would you like to play again?: (y or n)')

        # if user enter 'y' or 'n' exits loop otherwise prompts user to input again
        if try_again_input.lower() == 'y':
            # New line for readability
            print()
            return True

        elif try_again_input.lower() == 'n':
            return False

        else:
            print('invalid input, must be (y or n)')


# Function to add a border
def border():
    print('  {}'.format('-' * 19))


def main():
    # initializes try_again to tru to start the game
    try_again = True

    while try_again:
        # A dictionary linking a room to other rooms
        # and linking one item for each room except the Start room (Great Hall) and the room containing the villain
        rooms = {
            'Great Hall': {'South': 'Room of Requirement', 'East': 'Alnwick Castle', },
            'Alnwick Castle': {'South': 'Slughorns Office', 'West': 'Great Hall', 'item': 'Elder Wand'},
            'Room of Requirement': {'East': 'Astronomy Tower', 'North': 'Great Hall', 'item': 'Pensieve'},
            'Slughorns Office': {'South': 'Astronomy Tower', 'North': 'Alnwick Castle', 'item': 'Tom Riddles Diary'},
            'Astronomy Tower': {'West': 'Room of Requirement', 'North': 'Slughorns Office', 'East': 'Snapes Office',
                                'South': 'Boathouse', 'item': 'Sorting Hat'},
            'Snapes Office': {'West': 'Astronomy Tower', 'South': 'Common Room'},  # Villain
            'Common Room': {'West': 'Boathouse', 'North': 'Snapes Office', 'item': 'Resurrection Stone'},
            'Boathouse': {'North': 'Astronomy Tower', 'East': 'Common Room', 'item': 'Marvolo Gaunts Ring'}
        }

        show_instructions()

        # Initializes the Player class object as Bandit
        Bandit = Player()

        # Loop will run until exit condition is entered, the player is caught, or all items have been met
        while Bandit.get_current_room() != exit_condition:

            print('You are in the {}'.format(Bandit.get_current_room()))

            # Adds available room directions to a list, excludes the item
            directions = []
            for direction in rooms[Bandit.get_current_room()].keys():
                directions.append(direction) if direction != 'item' else None

            print('Available directions: {}'.format(directions))

            # prints the rooms item, if no items does not print
            print('There is a {} in this room'.format(rooms[Bandit.get_current_room()].get('item'))) \
                if rooms[Bandit.get_current_room()].get('item') is not None else None

            # prints the payers inventory unless empty which it then prints that the stash is empty
            print('Your stash{}'.format(': ' + str(Bandit.get_inventory()) if
                                          Bandit.inventory_count() > 0 else ' Is Empty'))

            # used to hold the response from the user after prompting for command and validating
            response = None
            # User has not been prompted at this point so its set too none to run through the loop
            while response is None:
                border()
                user_input = input('Enter Command: >')
                if user_input.lower().strip() == 'help':
                    help_prompt()
                    continue

                if user_input.lower() == exit_condition:
                    Bandit.set_current_room(user_input.lower())
                    break
                elif len(user_input.split()) <= 1:
                    print('Invalid command')
                    continue

                # Separates the users input and checks first command
                if user_input.split()[0].lower() == 'go':

                    # If go was entered sends second command, which should be the direction to the move function
                    # the move function validates direction
                    response = move_between_rooms(user_input.split()[1], rooms, Bandit.get_current_room())

                    if response is not None:

                        # Checks if new current room is the villain room
                        Bandit.set_current_room(response) if response is not villain_room else villain_prompt(Bandit)
                        border()
                    else:
                        continue

                elif user_input.split()[0].lower() == 'get':
                    # shuttle used to hold the item the user would like to get
                    shuttle = ""

                    # If item is multiple words this combines them into one string
                    for word in user_input.split()[1:]:
                        shuttle += word + " "

                    # sends item user would like to get to the get item function where validation will take place
                    response = get_item(shuttle.strip(), rooms, Bandit.get_current_room())

                    if response is not None:
                        # if response is not none the input has passed validation and the item is add to players stash
                        Bandit.add_inventory(response)

                        # Prompt informing player the item has been collected
                        print('{} received!'.format(rooms[Bandit.get_current_room()]['item']))
                        print('  {}'.format('-' * 19))

                        # Deletes the collected item from room to eliminate being displayed again
                        del (rooms[Bandit.get_current_room()]['item'])

                        # Checks if winning number of items has been collected
                        if Bandit.inventory_count() == number_of_items:
                            print('Winner winner chicken dinner!')
                            print('You have successfully robbed the wizard!')
                            Bandit.set_current_room(exit_condition)
                    else:
                        continue
                else:
                    print('Invalid command')

        # once game ends the players inventory is removed
        Bandit.remove_inventory()

        # function that asks the player if they would like to play again
        try_again = play_again_prompt()


if __name__ == "__main__":
    main()
