import random
from main import check_preconditions

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
    
    def add_random_connection(self, possible_locations):
        random_num = random.randint(0, len(possible_locations))
        # left off here 12/1/21


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