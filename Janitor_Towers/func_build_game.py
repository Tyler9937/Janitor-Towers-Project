
from class_location import Location
from class_item import Item
from class_game import Game
from main import end_game

# Initial build of the game
def build_game():
    # rooms of the main tower
    floor_B = Location("Floor B", "You are in the Janitor's closet in the basement of a tall tower")
    floor_G = Location("Floor G", "You are on the ground floor of a tall tower")
    floor_2 = Location("Floor 2", "You are on the second floor of a tall tower")
    floor_3 = Location("Floor 3", "You are on the third floor of a tall tower")
    floor_4 = Location("Floor 4", "You are on the fourth floor of a tall tower")
    floor_5 = Location("Floor 5", "You are on the fifth floor of a tall tower")
    floor_6 = Location("Floor 6", "You are on the sixth floor of a tall tower")
    floor_7 = Location("Floor 7", "You are on the seventh floor of a tall tower")
    floor_8 = Location("Floor 8", "You are on the eigth floor of a tall tower")
    floor_9 = Location("Floor 9", "You are on the ninth floor of a tall tower")
    floor_10 = Location("Floor 10", "You are on the 10th floor of a tall tower")
    floor_11 = Location("Floor 11", "You are on the 11th floor of a tall tower")
    roof = Location("Roof", "You are on the rooth of a tall tower")
    # Amazing idea!!! need a key for each floor of the elevator




    elevator = Location("Elevator", "You are inside an elevator within a large tower")

    floor_B.add_connection("in", elevator)


    key = Item("key", "key for elevator", "GOLDEN KEY", start_at=floor_B)

    floor_B.add_block("in", "the elevator needs a key", {"inventory_contains": key})
    ######
    # for the sewers randomly generate a permenat layout each time (use old text adventure game code)

    south_parking_lot = Location("Southern Parking Lot", "You are in a parking lot south of tall skyscraper")
    west_ally = Location("Western Ally", "You are in an ally way to the east of a tall skyscraper")
    east_street = Location("Eastern Street", "You are on a street east of a tall skyscraper")

    floor_G.add_connection("south", south_parking_lot)
    floor_G.add_connection("west", west_ally)
    floor_G.add_connection("east", east_street)

    blue_sword = Item("sword", "a sword with a blue tint", "A SHARP BLUE SWORD.", start_at=floor_G)
    dead_duck = Item("dead duck", "a yellow duckling that lays dead", "A VERY DEAD DUCK.", start_at=floor_G)
    

    # Can not be picked up
    barrel_of_blood = Item("barrel of blood", "A barrel of blood that sits on floor", "A VERY RED BARREL OF BLOOD", start_at=floor_G, gettable=False)

    barrel_of_blood.add_action("drink from barrel", end_game, ("that is kinda gross, and I think you just died. THE END"))
    # if we keep the extra command system like this we don't get overwelled by all possible verbs in the parser we stick to the basics like iventory north examine. and then we just have our special commands given each item.
    # furthermore when adding more sophiticated nlp procesing it will be easy to have a function that compares with each objects action command
    return Game(floor_B)

