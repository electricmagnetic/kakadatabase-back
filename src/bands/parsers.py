from kakadatabase.parameters import COLOURS, SEPARATORS

def standardise_combo(combo_string):
    """ Returns a string containing only valid characters (colours or separators) as uppercase """

    combo_string = combo_string.upper()
    combo_list = map(lambda combo_character: combo_character if (combo_character in COLOURS) or (combo_character in SEPARATORS.values()) else None, combo_string)
    return ''.join(list(filter(None, combo_list)))

def parse_colours(combo_string):
    """ Return a list of human-readable colours based on combo_string string """

    return list(filter(None, map(lambda combo_character: COLOURS.get(combo_character), combo_string)))

def parse_legs(combo_string):
    """ Return a list of colours for each leg """

    leg_left_string, separator, leg_right_string = combo_string.partition(SEPARATORS['LEG'])
    return parse_colours(leg_left_string), parse_colours(leg_right_string)
