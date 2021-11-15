player_location = (0, 0, 0)

world = {(0, 0, 0): {"name": "F1", "desc": "You are on the ground floor of a skyscraper", "north": {"valid_move": False, "move_desc": "You approach a wall"}, "east": {"valid_move": True, "move_desc": ""}, "south": {"valid_move": True, "move_desc": ""}, "west": {"valid_move": True, "move_desc": ""}, "up": {"valid_move": False, "move_desc": "You stare at a celling"}, "down": {"valid_move": False, "move_desc": "You stare at the floor"}},
         (-1, 0, 0): {"name": "WA", "desc": "You are in the west ally", "north": {"valid_move": False, "move_desc": "you are blocked by scary mist"}, "east": {"valid_move": True, "move_desc": ""}, "south": {"valid_move": False, "move_desc": "you are blocked by scary mist"}, "west": {"valid_move": False, "move_desc": "You are blocked by a wall"}, "up": {"valid_move": False, "move_desc": "You stare at the sky"}, "down": {"valid_move": False, "move_desc": "You stare at the ground"}},
         (0, -1, 0): {"name": "SP", "desc": "You are in the south parking lot", "north": {"valid_move": True, "move_desc": ""}, "east": {"valid_move": False, "move_desc": "You are approach a locked gate"}, "south": {"valid_move": False, "move_desc": "you are blocked by a wall"}, "west": {"valid_move": False, "move_desc": "You are blocked by a wall"}, "up": {"valid_move": False, "move_desc": "You stare at the sky"}, "down": {"valid_move": False, "move_desc": "You stare at the ground"}},
         (1, 0, 0): {"name": "ES", "desc": "You are in the East Street", "north": {"valid_move": False, "move_desc": "you are blocked by scary mist"}, "east": {"valid_move": False, "move_desc": "You are blocked by mist"}, "south": {"valid_move": False, "move_desc": "you are blocked by scary mist"}, "west": {"valid_move": True, "move_desc": ""}, "up": {"valid_move": False, "move_desc": "You stare at the sky"}, "down": {"valid_move": False, "move_desc": "You stare at the ground"}}
         }

items = {"sword": {"location": "F1", "desc": "long silver blade lays on the floor"}}

word_input_dict = {"north": {"position": (0, 1, 0), "game_on": True},
                   "east": {"position": (1, 0, 0), "game_on": True},
                   "south": {"position": (0, -1, 0), "game_on": True},
                   "west": {"position": (-1, 0, 0), "game_on": True},
                   "up": {"position": (0, 0, 1), "game_on": True},
                   "down": {"position": (0, 0, -1), "game_on": True},
                   "quit": {"position": (0, 0, 0), "game_on": False}
                   }


# game progression function to be called by app
def game_progression(player_input):

    global player_location
    output_text = []

    if player_input in word_input_dict:
        word_info_dict = word_input_dict[player_input]
        
        game_on = word_info_dict["game_on"]
        
        # Checking for neswud inputs
        if player_input == "north" or player_input == "east" or player_input == "south" or player_input == "west" or player_input == "up" or player_input == "down":
            # Checking if player can move in this direction
            if world[player_location][player_input]["valid_move"]:
                player_location = list(player_location)

                # Changing player location
                for i, val in enumerate(player_location):
                    player_location[i] = player_location[i] + word_info_dict["position"][i]

                player_location = tuple(player_location)
                output_text.append(world[player_location]['name'])
            else:
                output_text.append(world[player_location][player_input]["move_desc"])


        # for item in items:
        #     if items[item]["location"] == world[player_location]["name"]:
        #         print(items[item]['desc'])
        
    else:
        output_text.append('verb not reconized')

    return output_text, world[player_location]['name']



