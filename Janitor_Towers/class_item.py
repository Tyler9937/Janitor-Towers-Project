from main import output_text, check_preconditions

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

