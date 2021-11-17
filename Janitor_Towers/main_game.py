

player_location = (0, 0, 0)

verb_state = " "

world = {(0, 0, 0): {"name": "F1", "desc": "You are on the ground floor of a skyscraper", "north": {"valid_move": False, "move_desc": "You approach a wall"}, "east": {"valid_move": True, "move_desc": "you see a street"}, "south": {"valid_move": True, "move_desc": "you see a parking lot"}, "west": {"valid_move": True, "move_desc": "you see an ally way"}, "up": {"valid_move": False, "move_desc": "You stare at a celling"}, "down": {"valid_move": False, "move_desc": "You stare at the floor"}},
         (-1, 0, 0): {"name": "WA", "desc": "You are in the west ally", "north": {"valid_move": False, "move_desc": "you are blocked by scary mist"}, "east": {"valid_move": True, "move_desc": "you see the west exit of a tall tower"}, "south": {"valid_move": False, "move_desc": "you are blocked by scary mist"}, "west": {"valid_move": False, "move_desc": "You are blocked by a wall"}, "up": {"valid_move": False, "move_desc": "You stare at the sky"}, "down": {"valid_move": False, "move_desc": "You stare at the ground"}},
         (0, -1, 0): {"name": "SP", "desc": "You are in the south parking lot", "north": {"valid_move": True, "move_desc": "you see the side entrance of a tower"}, "east": {"valid_move": False, "move_desc": "You are approach a locked gate"}, "south": {"valid_move": False, "move_desc": "you are blocked by a wall"}, "west": {"valid_move": False, "move_desc": "You are blocked by a wall"}, "up": {"valid_move": False, "move_desc": "You stare at the sky"}, "down": {"valid_move": False, "move_desc": "You stare at the ground"}},
         (1, 0, 0): {"name": "ES", "desc": "You are in the East Street", "north": {"valid_move": False, "move_desc": "you are blocked by scary mist"}, "east": {"valid_move": False, "move_desc": "You are blocked by mist"}, "south": {"valid_move": False, "move_desc": "you are blocked by scary mist"}, "west": {"valid_move": True, "move_desc": "you see the main entrance of a tower"}, "up": {"valid_move": False, "move_desc": "You stare at the sky"}, "down": {"valid_move": False, "move_desc": "You stare at the ground"}}
         }

game_items = {"sword": {"location": "F1", "desc": "long silver blade lays on the floor"}}

game_characters = {"zombie": {"location": "F1", "desc": "zombie crawls along floor"}}

word_input_dict = {"north": {"word_type": "direction", "type": "direction"},
                   "east": {"word_type": "direction", "type": "direction"},
                   "south": {"word_type": "direction", "type": "direction"},
                   "west": {"word_type": "direction", "type": "direction"},
                   "up": {"word_type": "direction", "type": "direction"},
                   "down": {"word_type": "direction", "type": "direction"},

                   "go": {"word_type": "verb", "type": "movement"},

                   "look": {"word_type": "verb", "type": "describe"},

                   "grab": {"word_type": "verb", "type": "take"},
                   "hit": {"word_type": "verb", "type": "attack"},
                   "sword": {"word_type": "object", "type": "item"}}



movement_word_dict = {"north": (0, 1, 0),
                      "east": (1, 0, 0),
                      "south": (0, -1, 0),
                      "west": (-1, 0, 0),
                      "up": (0, 0, 1),
                      "down": (0, 0, -1)
                      }


def game_reset():
    global player_location
    global verb_state
    verb_state = " "
    player_location = (0, 0, 0)


def player_movement_func(player_input_word):

    global player_location

    #Checking if player can move in this direction
    if world[player_location][player_input_word]["valid_move"]:
        player_location = list(player_location)

        # Changing player location
        for i, val in enumerate(player_location):
            player_location[i] = player_location[i] + movement_word_dict[player_input_word][i]

        player_location = tuple(player_location)

        return world[player_location]['name']

    else:
        return world[player_location][player_input_word]["move_desc"]



# game progression function to be called by app
def game_progression(player_input):


    global verb_state
    output_text = []
    game_on = True

    # could say didn't understand, needs more, gives commands

    parser_result = {"parser_passed": True, 
                    "command_list": {"move": False,
                                     "look": {"room": False, "room_desc": False, "item": False}, 
                                     "attack": False, "take": False}, 
                    "error_list": {"live_states": False, "error_output_text": False}}
                    
    # "attack": {"object": "zombie", "tool": "sword"}
    # "look": {"room": F1, "room_desc": it is dark "item: False"}


    # The parser
    player_input_list = player_input.split(" ")

    for index, word in enumerate(player_input_list):

        # Step One: Checking if full sentence is understood
        if word in word_input_dict:
            
            # Step Two: Setting the inital state based on first word in sentence
            if index == 0:
                
                # Can move in a direction with one word if lenght is one
                if word_input_dict[word]["type"] == "direction":
                    if len(player_input_list) == 1:

                        parser_result["parser_passed"] = True
                        parser_result["command_list"]["move"] = word #output_text.append(player_movement_func(word)) 
                        
                    else:

                        parser_result["parser_passed"] = False
                        parser_result["error_list"]["live_states"] = False
                        parser_result["error_list"]["error_output_text"] = "verb not recognized" #output_text.append("verb not reconized")
                        break

                # Identifing the verb, changing verb state
                elif word_input_dict[word]["word_type"] == "verb":

                    if len(player_input_list) == 1:

                        # Special verb cases where length can be one
                        if word_input_dict[word]["type"] == "describe":

                            parser_result["parser_passed"] = True
                            parser_result["command_list"]["look"]["room"] = world[player_location]['name'] #output_text.append(world[player_location]['name'])  output_text.append(world[player_location]['desc'])
                            parser_result["command_list"]["look"]["room_desc"] = world[player_location]['desc']
                            break

                        else:
                            verb_state = word

                            parser_result["parser_passed"] = False
                            parser_result["error_list"]["live_states"] = True
                            parser_result["error_list"]["error_output_text"] = "where do you want to " + word #output_text.append("where do you want to " + word)
                            
                    else:
                        verb_state = word

                # We need index 0 it to be a verb or a few specilty cases
                else:

                    parser_result["parser_passed"] = False
                    parser_result["error_list"]["error_output_text"] = "verb not reconized" #output_text.append("verb not reconized")
                    break
            
            # Step Three: verb state has already been set need to identify objects
            else:
                # These indexs cannot be verbs
                if word_input_dict[word]["word_type"] != "verb":

                    if word_input_dict[verb_state]['type'] == "movement":
                        if word_input_dict[word]["type"] == "direction":

                            # can't be any words after this object
                            if word == player_input_list[-1]:
                                
                                parser_result["parser_passed"] = True
                                parser_result["command_list"]["move"] = word #output_text.append(player_movement_func(word))

                            else:

                                parser_result["parser_passed"] = False
                                parser_result["error_list"]["live_states"] = True
                                parser_result["error_list"]["error_output_text"] = "I understood as far as wanting to " + verb_state  #output_text.append("I understood as far as wanting to " + verb_state)
                                

                    elif word_input_dict[verb_state]['type'] == "describe":
                        if word_input_dict[word]['type'] == "direction":
                             # only works if object is a direction !!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # will also have to accout for mutiple items in a room (look at which sword)

                            parser_result["parser_passed"] = True
                            parser_result["command_list"]["look"]["room_desc"] = world[player_location][word]["move_desc"] #output_text.append(world[player_location][word]["move_desc"])
                            
                        else:

                            parser_result["parser_passed"] = False
                            parser_result["error_list"]["live_states"] = True
                            parser_result["error_list"]["error_output_text"] = "I understood as far as wanting to " + verb_state #output_text.append("I understood as far as wanting to " + verb_state)
                            
                    else:
                        parser_result["parser_passed"] = False
                        parser_result["error_list"]["live_states"] = True
                        parser_result["error_list"]["error_output_text"] = "I understood as far as wanting to " + verb_state #output_text.append("I understood as far as wanting to " + verb_state)
                            
                else:
                    parser_result["parser_passed"] = False
                    parser_result["error_list"]["live_states"] = True
                    parser_result["error_list"]["error_output_text"] = "I understood as far as wanting to " + verb_state #output_text.append("I understood as far as wanting to " + verb_state)
                            
        # Describes what was not understood in sentence     
        else:

            if len(player_input_list) == 1:

                parser_result["parser_passed"] = False
                parser_result["error_list"]["live_states"] = False
                parser_result["error_list"]["error_output_text"] = "verb not reconized" #output_text.append("verb not reconized")
                
            else:
                parser_result["parser_passed"] = False
                parser_result["error_list"]["live_states"] = True
                parser_result["error_list"]["error_output_text"] = "I understood as far as wanting to " + verb_state #output_text.append("I understood as far as wanting to " + verb_state)
                      



    # Beginning of actual game processing

    # parser passed
    if parser_result["parser_passed"] == True:
        if parser_result["command_list"]["move"] != False:
            output_text.append(player_movement_func(parser_result["command_list"]["move"]))

        if parser_result["command_list"]["look"]["room"] != False:
            output_text.append(parser_result["command_list"]["look"]["room"])
        
        if parser_result["command_list"]["look"]["room_desc"] != False:
            output_text.append(parser_result["command_list"]["look"]["room_desc"])

    # parser did not pass
    else:
        if parser_result["error_list"]["live_states"] == False:
            verb_state = " "
        
        output_text.append(parser_result["error_list"]["error_output_text"])

    return output_text, world[player_location]['name'], game_on






    # if player_input in word_input_dict:
    #     word_info_dict = word_input_dict[player_input]
        
    #     if word_info_dict["game_on"]:
    #          # Checking for neswud inputs
    #         if player_input == "north" or player_input == "east" or player_input == "south" or player_input == "west" or player_input == "up" or player_input == "down":
    #             # Checking if player can move in this direction
    #             if world[player_location][player_input]["valid_move"]:
    #                 player_location = list(player_location)

    #                 # Changing player location
    #                 for i, val in enumerate(player_location):
    #                     player_location[i] = player_location[i] + word_info_dict["position"][i]

    #                 player_location = tuple(player_location)
    #                 output_text.append(world[player_location]['name'])
    #             else:
    #                 output_text.append(world[player_location][player_input]["move_desc"])
    #         else:
    #             pass
    #     else:
    #         game_reset()
    #         game_on = False

    #     for item in game_items:
    #         if game_items[item]["location"] == world[player_location]["name"]:
    #             output_text.append(game_items[item]['desc'])
        
    # else:
    #     output_text.append('verb not reconized')

    # return output_text, world[player_location]['name'], game_on



