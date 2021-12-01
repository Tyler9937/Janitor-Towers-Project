

output_text = []


# Function to check preconditoins before certain game events can happen
def check_preconditions(preconditions, game, print_failure_reasons=True):
    global output_text

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


def add_item_to_inventory(game, *args):
    (item, action_description, already_done_description) = args[0]
    if(not game.is_in_inventory(item)):
        output_text.append(action_description)
        game.add_to_inventory(item)
    else:
        output_text.append(already_done_description)
    return False

def describe_something(game, *args):
    (description) = args[0]
    output_text.append(description)
    return False

def destroy_item(game, *args):
    (item, action_description, already_done_description) = args[0]
    if game.is_in_inventory(item):
        game.inventory.pop(item.name)
        output_text.append(action_description)
    elif item.name in game.curr_location.items:
        game.curr_location.remove_item(item)
        output_text.append(action_description)
    else:
        output_text.append(already_done_description)
    return False

def end_game(game, *args):
    end_message = args[0]
    output_text.append(end_message)
    return True

