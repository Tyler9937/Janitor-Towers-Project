class Game:

    def __init__(self, starting_loc):

        self.current_loc = starting_loc
        self.current_loc.has_been_visited = True
        self.inventory = {}
        self.print_commands = True
        self.output_text = []

    def describe(self):
        self.describe_current_location()
        self.describe_exits()

    def describe_current_location(self):
        self.output_text.append(self.current_loc.description)
        
    def describe_exits(self)
        exits = []


class Location:

    def __init__(self, name, description, end_game=False):

        self.name = name
        self.description = description
        self.end_game = end_game
        self.has_been_visited = False


def build_game():
    floor_G = Location("floor_G", "You are on the ground floor of a large skyscraper")

    

    return Game(floor_G)


