from class_location import Location
from class_item import Item
from class_game import Game

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

