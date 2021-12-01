

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


