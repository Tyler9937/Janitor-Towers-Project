from main import output_text

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

