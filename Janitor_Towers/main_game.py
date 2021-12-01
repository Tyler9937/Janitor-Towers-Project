

output_text = []

# Main object of the game controls all player information
class Game:

    def __init__(self, starting_loc):

        self.curr_location = starting_loc
        self.curr_location.has_been_visited = True
        self.inventory = {}
        # Adds possible moves to output_text
        self.print_commands = True
        # # Refrenced by app.py for visualizing gameplay
        # self.output_text = []

    # Gathers information needed for player to understand location
    def describe(self):

        self.describe_current_location()
        self.describe_exits()
        self.describe_items()

    def describe_current_location(self):
        output_text.append(self.curr_location.description)
        
    def describe_exits(self):
        exits = []
        for exit in self.curr_location.connections.keys():
            exits.append(exit)
       
        output_text.append("Exits: " + ", ".join(["{}"]*len(exits)).format(*exits))

    def describe_items(self):
        if len(self.curr_location.items) > 0:
            for item_name in self.curr_location.items:
                item = self.curr_location.items[item_name]
                output_text.append("You see a {}, it can be described as: {}".format(item.name, item.description))

                if self.print_commands:
                    special_commands = item.get_commands()
                    for cmd in special_commands:
                        output_text.append(cmd)

    def add_to_inventory(self, item):
        self.inventory[item.name] = item
            
    def is_in_inventory(self, item):
        return item.name in self.inventory

    # Shows all items in room and inventory
    def get_items_in_scope(self):
        items_in_scope = []
        for item_name in self.curr_location.items:
            items_in_scope.append(self.curr_location.items[item_name])
        for item_name in self.inventory:
            items_in_scope.append(self.inventory[item_name])
        
        return items_in_scope


# Object stores all data regarding a specific room in the game's graph
class Location:

    def __init__(self, name, description, end_game=False):

        # Text desciptions
        self.name = name
        self.description = description
        self.travel_desc = {}

        self.end_game = end_game
        self.has_been_visited = False

        # Other rooms connected to this one
        self.connections = {}
        # Items that are in room
        self.items = {}
        # Things preventing progression in room
        self.blocks = {}
    
    # Creating all connections in graph
    def add_connection(self, direction, connected_location, travel_desc=''):
        self.connections[direction] = connected_location
        self.travel_desc[direction] = travel_desc
        if direction == "north":
            connected_location.connections["south"] = self
            connected_location.travel_desc["south"] = ''
        elif direction == "east":
            connected_location.connections["west"] = self
            connected_location.travel_desc["west"] = ''
        elif direction == "south":
            connected_location.connections["north"] = self
            connected_location.travel_desc["north"] = ''
        elif direction == "west":
            connected_location.connections["east"] = self
            connected_location.travel_desc["east"] = ''
        elif direction == "up":
            connected_location.connections["down"] = self
            connected_location.travel_desc["down"] = ''
        elif direction == "down":
            connected_location.connections["up"] = self
            connected_location.travel_desc["up"] = ''
        elif direction == "in":
            connected_location.connections["out"] = self
            connected_location.travel_desc["out"] = ''
        elif direction == "out":
            connected_location.connections["in"] = self
            connected_location.travel_desc["in"] = ''

    def add_item(self, name, item):
        self.items[name] = item

    def remove_item(self, item):
        self.items.pop(item.name)
    
    # Checking if a path is blocked
    def is_blocked(self, direction, game):
        if not direction in self.blocks:
            return False
        (block_description, preconditions) = self.blocks[direction]
        if check_preconditions(preconditions, game):
            return False
        else: 
            return True
    
    # Describes why path is blocked
    def get_block_description(self, direction):
        if not direction in self.blocks:
            return ""
        else:
            (block_description, preconditions) = self.blocks[direction]
            return block_description

    # Methode for creating new blocks in the game
    def add_block(self, blocked_direction, block_description, preconditions):
        self.blocks[blocked_direction] = (block_description, preconditions)


# Function to check preconditoins before certain game events can happen
def check_preconditions(preconditions, game, print_failure_reasons=True):
    all_conditions_met = True
    for check in preconditions: 
        if check == "inventory_contains":
            item = preconditions[check]
        if not game.is_in_inventory(item):
            all_conditions_met = False
            if print_failure_reasons:
                output_text.append("You don't have the {}".format(item.name))
        if check == "in_location":
            location = preconditions[check]
        if not game.curr_location == location:
            all_conditions_met = False
            if print_failure_reasons:
                output_text.append("You aren't in the correct location")
        if check == "location_has_item":
            item = preconditions[check]
        if not item.name in game.curr_location.items:
            all_conditions_met = False
            if print_failure_reasons:
                output_text.append("The {} isn't in this location".format(item.name))
    return all_conditions_met


# Stores all information about an item in the game
class Item:

    def __init__(self, name, description, examine_text='', take_text='', start_at=None, gettable=True, end_game=False):

        self.name = name
        self.description = description
        self.examine_text = examine_text
        self.take_text = take_text if take_text else ("You take the {}.".format(self.name))
        self.gettable = gettable
        self.end_game = end_game
        if start_at:
            start_at.add_item(name, self)
        self.commands = {}

    # What to type to use item
    def get_commands(self):
        return self.commands.keys()

    # Adding new actions
    def add_action(self, command_text, function, arguments, preconditions={}):
        self.commands[command_text] = (function, arguments, preconditions)
    
    # Going through with actions
    def do_action(self, command_text, game):
        end_game = False  # Switches to True if this action ends the game.
        if command_text in self.commands:
            function, arguments, preconditions = self.commands[command_text]
            if check_preconditions(preconditions, game):
                end_game = function(game, arguments)
        else:
            output_text.append("Cannot perform the action {}".format(command_text))
        return end_game


# Breaks down user inputs and directs the game what to do
class Parser:

    def __init__(self, game):
        self.command_history = []
        self.game = game


    def parse_command(self, command):
        self.command_history.append(command)
        end_game = False
    
        intent = self.get_player_intent(command)
        if intent == "direction":
            end_game = self.go_in_direction(command)
        elif intent == "redescribe":
            self.game.describe()
        elif intent == "examine":
            self.examine(command)
        elif intent == "take":
            end_game = self.take(command)
        elif intent == "drop":
            self.drop(command)
        elif intent == "inventory":
            self.check_inventory(command)
        elif intent == "special":
            end_game = self.run_special_command(command)
        elif intent == "sequence":
            end_game = self.execute_sequence(command)
        else:
            output_text.append("I'm not sure what you want to do.")
        return end_game


    def get_player_intent(self,command):
        command = command.lower()
        if "," in command:
      
            return "sequence"
        elif self.get_direction(command):
     
            return "direction"
        elif command.lower() == "look" or command.lower() == "l":
      
            return "redescribe"
        elif "examine " in command or command.lower().startswith("x "):
            return "examine"
        elif  "take " in command or "get " in command:
            return "take"
        elif "drop " in command:
            return "drop"
        elif "inventory" in command or command.lower() == "i":
            return "inventory"
        else: 
            for item in self.game.get_items_in_scope():
                special_commands = item.get_commands()
                for special_command in special_commands:
                    if command == special_command.lower():
                        return "special"

    
    def get_direction(self, command):
        command = command.lower()
        if command == "n" or "north" in command:
            return "north" 
        if command == "s" or "south" in command:
            return "south"
        if command == "e" or "east" in command: 
            return "east"
        if command == "w" or "west" in command:
            return "west"
        if command == "up":
            return "up"
        if command == "down":
            return "down"
        if command.startswith("go out"):
            return "out"
        if command.startswith("go in"):
            return "in"
        for exit in self.game.curr_location.connections.keys():
            if command == exit.lower() or command == "go " + exit.lower():
                return exit
        return None


    def go_in_direction(self, command):
    
        direction = self.get_direction(command)

        if direction:
            if direction in self.game.curr_location.connections:
                if self.game.curr_location.is_blocked(direction, self.game):
          
                    output_text.append(self.game.curr_location.get_block_description(direction))
                else:
          
                    self.game.curr_location = self.game.curr_location.connections[direction]

          
                    if self.game.curr_location.end_game:
                        self.game.describe_current_location()
                    else:
                        self.game.describe()
            else:
                output_text.append("You can't go {} from here.".format(direction.capitalize()))
        return self.game.curr_location.end_game

    def check_inventory(self,command):
    
        if len(self.game.inventory) == 0:
            output_text.append("You don't have anything.")
        else:
            descriptions = []
            for item_name in self.game.inventory:
                item = self.game.inventory[item_name]
                descriptions.append(item.description)
            output_text.append("You have: " + ", ".join(["{}"]*len(descriptions)).format(*descriptions))
    
    def examine(self, command):

        command = command.lower()
        matched_item = False

        for item_name in self.game.curr_location.items:
            if item_name in command:
                item = self.game.curr_location.items[item_name]
                if item.examine_text:
                    output_text.append(item.examine_text)
                    matched_item = True
                break

        for item_name in self.game.inventory:
            if item_name in command:
                item = self.game.inventory[item_name]
                if item.examine_text:
                    output_text.append(item.examine_text)
                    matched_item = True

        if not matched_item:
            output_text.append("You don't see anything special.")

    def take(self, command):

        command = command.lower()
        matched_item = False


        end_game = False


        for item_name in self.game.curr_location.items:
            if item_name in command:
                item = self.game.curr_location.items[item_name]
                if item.gettable:
                    self.game.add_to_inventory(item)
                    self.game.curr_location.remove_item(item)
                    output_text.append(item.take_text)
                    end_game = item.end_game
                else:
                    output_text.append("You cannot take the {}.".formate(item_name))
                matched_item = True
                break

        if not matched_item:
            for item_name in self.game.inventory:
                if item_name in command:
                    output_text.append("You already have the {}.".format(item_name))
                    matched_item = True

        if not matched_item:
            output_text.append("You can't find it.")

        return end_game
    
    def drop(self, command):

        command = command.lower()
        matched_item = False

        if not matched_item:
            for item_name in self.game.inventory:
                if item_name in command:
                    matched_item = True
                    item = self.game.inventory[item_name]
                    self.game.curr_location.add_item(item_name, item)
                    self.game.inventory.pop(item_name)
                    output_text.append("You drop the {}.".format(item_name))
                    break

        if not matched_item:
            output_text.append("You don't have that.")

    def run_special_command(self, command):

        for item in self.game.get_items_in_scope():
            special_commands = item.get_commands()
            for special_command in special_commands:
                if command == special_command.lower():
                    return item.do_action(special_command, self.game)

    def execute_sequence(self, command):
        for cmd in command.split(","):
            cmd = cmd.strip()
            self.parse_command(cmd)


# Initial build of the game
def build_game():
    floor_G = Location("Floor G", "You are on the ground floor of a large skyscraper")
    south_parking_lot = Location("Southern Parking Lot", "You are in a parking lot south of tall skyscraper")
    west_ally = Location("Western Ally", "You are in an ally way to the east of a tall skyscraper")
    east_street = Location("Eastern Street", "You are on a street east of a tall skyscraper")

    floor_G.add_connection("south", south_parking_lot)
    floor_G.add_connection("west", west_ally)
    floor_G.add_connection("east", east_street)

    blue_sword = Item("sword", "a sword with a blue tint", "A SHARP BLUE SWORD.", start_at=floor_G)
    dead_duck = Item("dead duck", "a yellow duckling that lays dead", "A VERY DEAD DUCK.", start_at=floor_G)

    return Game(floor_G)


