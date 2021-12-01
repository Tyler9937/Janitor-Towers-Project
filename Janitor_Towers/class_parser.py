from main import output_text


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

