from typing import TYPE_CHECKING

from BaseClasses import Entrance, Location
from worlds.generic.Rules import add_rule, set_rule
from .Options import DifficultyLogic
from .LevelPrefixes import *
#from .JsonReader import AccessMethod

if TYPE_CHECKING:
    from . import GloverWorld
else:
    GloverWorld = object

move_lookup = [
    "Cartwheel",
    "Crawl",
    "Double Jump",
    "Fist Slam",
    "Ledge Grab",
    "Push",
    "Locate Garib",
    "Locate Ball",
    "Dribble",
    "Quick Swap",
    "Slap",
    "Throw",
    "Ball Toss",
    "Rubber Ball",
    "Bowling Ball",
    "Ball Bearing",
    "Crystal",
    "Beachball Potion",
    "Death Potion",
    "Helicopter Potion",
    "Frog Potion",
    "Boomerang Ball Potion",
    "Speed Potion",
    "Sticky Potion",
    "Hercules Potion",
    "Jump",
    "Not Crystal",
    "Not Bowling",
    "Sinks",
    "Floats",
    "Grab",
    "Ball Up",
    "Power Ball",
    "Not Bowling or Crystal"
]

switches_to_event_items = {
    ATLANTIS_1 + ": Glover Switch"               : ATLANTIS_1 + " Gate",
    ATLANTIS_2 + ": Drain Block"                 : ATLANTIS_2 + " Elevator",
    ATLANTIS_2 + ": Ball Switch"                 : ATLANTIS_2 + " Ballswitch Drain",
    ATLANTIS_2 + ": Glover Switch"               : ATLANTIS_2 + " Gate",
    ATLANTIS_3 + ": Pyramid Ball Switch"         : ATLANTIS_3 + " Waterwheel",
    ATLANTIS_3 + ": Cliff Ball Switch"           : ATLANTIS_3 + " Cave Platforms",
    CARNIVAL_1 + ": Conveyor Target"             : CARNIVAL_1 + " Elevator",
    CARNIVAL_1 + ": Bars Glover Switch"          : CARNIVAL_1 + " Gate",
    CARNIVAL_1 + ": Ramp Ball Switch"            : CARNIVAL_1 + " Door A",
    CARNIVAL_1 + ": Ice Cream Glover Switch"     : CARNIVAL_1 + " Door B",
    CARNIVAL_1 + ": Slide Glover Switch"         : CARNIVAL_1 + " Door C",
    CARNIVAL_1 + ": Whack-A-Mole Glover Switch"  : CARNIVAL_1 + " Rocket",
    CARNIVAL_1 + ": Plinko Glover Switch"        : CARNIVAL_1 + " Rocket",
    CARNIVAL_1 + ": Slots Glover Switch"         : CARNIVAL_1 + " Rocket",
    CARNIVAL_2 + ": Clown Teeth"                 : CARNIVAL_2 + " Drop Garibs",
    CARNIVAL_2 + ": Ball Switch"                 : CARNIVAL_2 + " Fan",
    CARNIVAL_3 + ": Glover Switch"               : CARNIVAL_3 + " Spin Door",
    CARNIVAL_3 + ": Ball Switch"                 : CARNIVAL_3 + " Hands",
    PIRATES_1 + ": Ship Target"                  : PIRATES_1 + " Raise Beach",
    PIRATES_1 + ": Tower Glover Switch"          : PIRATES_1 + " Elevator",
    PIRATES_1 + ": Coast Target"                 : PIRATES_1 + " Chest",
    PIRATES_1 + ": Fan Ball Switch"              : PIRATES_1 + " Sandpile",
    PIRATES_1 + ": Sand Ball Switch"             : PIRATES_1 + " Waterspout",
    PIRATES_1 + ": Lighthouse Target"            : PIRATES_1 + " Lighthouse",
    PIRATES_1 + ": Lighthouse Glover Switch"     : PIRATES_1 + " Raise Ship",
    PIRATES_1 + ": Crate Ball Switch"            : PIRATES_1 + " Bridge",
    PIRATES_2 + ": Glover Switch"                : PIRATES_2 + " Lower Water",
    PIRATES_2 + ": Water Ball Switch"            : PIRATES_2 + " Ramp",
    PIRATES_2 + ": Platform Ball Switch"         : PIRATES_2 + " Gate",
    #PIRATES_3 + ": "                            : PIRATES_3 + " Platform Spin",
    PIRATES_3 + ": Cliff Glover Switch"          : PIRATES_3 + " Trampoline",
    PIRATES_3 + ": Target"                       : PIRATES_3 + " Stairs",
    PIRATES_3 + ": Ball Switch"                  : PIRATES_3 + " Elevator",
    PREHISTORIC_1 + ": Icicles"                  : PREHISTORIC_1 + " Life Drop",
    PREHISTORIC_2 + ": Lavafall Ball Switch"     : PREHISTORIC_2 + " Platform 1",
    PREHISTORIC_2 + ": Switches Ball Switch"     : PREHISTORIC_2 + " Platform 2",
    PREHISTORIC_2 + ": Glover Switch"            : PREHISTORIC_2 + " Lower Ball Switch",
    PREHISTORIC_3 + ": Tracey Tree"              : PREHISTORIC_3 + " Drop Garibs",
    PREHISTORIC_3 + ": Trees Glover Switch"      : PREHISTORIC_3 + " Spin Stones",
    PREHISTORIC_3 + ": Monolith A"               : PREHISTORIC_3 + " Lower Monolith",
    PREHISTORIC_3 + ": Monolith B"               : PREHISTORIC_3 + " Lower Monolith",
    PREHISTORIC_3 + ": Monolith C"               : PREHISTORIC_3 + " Lower Monolith",
    PREHISTORIC_3 + ": Monolith D"               : PREHISTORIC_3 + " Lower Monolith",
    PREHISTORIC_3 + ": Monolith Ball Switch"     : PREHISTORIC_3 + " Floating Platforms",
    PREHISTORIC_3 + ": Flying Lava Ball Switch"  : PREHISTORIC_3 + " Lava Spinning",
    PREHISTORIC_3 + ": Lava Pit Ball Switch"     : PREHISTORIC_3 + " Dirt Elevator",
    FEAR_1 + ": Dead-End Glover Switch"          : FEAR_1 + " Coffin",
    FEAR_1 + ": Left Target"                     : FEAR_1 + " Progressive Doorway",
    FEAR_1 + ": Right Target"                    : FEAR_1 + " Progressive Doorway",
    FEAR_1 + ": Push Blocks"                     : FEAR_1 + " Coffin Lightning",
    FEAR_1 + ": Coffin Glover Switch"            : FEAR_1 + " Drawbridge",
    FEAR_2 + ": Push Target"                     : FEAR_2 + " Garibs Fall",
    FEAR_2 + ": Push Switch"                     : FEAR_2 + " Progressive Gate",
    FEAR_2 + ": Slope Target"                    : FEAR_2 + " Progressive Gate",
    FEAR_2 + ": Mummy"                           : FEAR_2 + " Mummy Gate",
    FEAR_3 + ": Target"                          : FEAR_3 + " Gate",
    FEAR_3 + ": Ball Switch"                     : FEAR_3 + " Spikes",
    # + ": "                                     : SPACE_1 + " Aliens",
    SPACE_1 + ": Sign Glover Switch"             : SPACE_1 + " Fans",
    SPACE_1 + ": Stone Pillar Ball Switch"       : SPACE_1 + " Flying Platforms",
    SPACE_1 + ": Cliff Glover Switch"            : SPACE_1 + " Goo Platforms",
    SPACE_1 + ": Hazard Stripe Ball Switch"      : SPACE_1 + " UFO",
    SPACE_1 + ": UFO Glover Switch"              : SPACE_1 + " Missile",
    SPACE_2 + ": Right Platform Ball Switch"     : SPACE_2 + " Mashers",
    SPACE_2 + ": Cliff Ball Switch"              : SPACE_2 + " Ramp",
    SPACE_3 + ": Duel Switch"                    : SPACE_3 + " Hazard Gate",
    SPACE_3 + ": Conveyor Glover Switch"         : SPACE_3 + " Sign",
    SPACE_3 + ": Above Fan Red Switch"           : SPACE_3 + " Fan",
    SPACE_3 + ": Magnet Ball Switch"             : SPACE_3 + " Bridge",
    SPACE_3 + ": Ball Switch"                    : SPACE_3 + " Glass Gate",
    "Training: Ball Switch"                                  : "Training Sandpit",
    "Training: Glover Switch"                                : "Training Lower Target",
    "Training: Target"                                       : "Training Stairs"
}

def access_methods_to_rules(self, all_methods, spot : Location | Entrance):
    nonblank_methods = []
    for each_method in all_methods:
        if len(each_method.required_items) == 0:
            continue
        nonblank_methods.append(each_method)
    #If there's no nonblank methods at this step, it must be open
    if len(nonblank_methods) == 0:
        return
    #Reorder the access methods to get around the 'or'ing problem
    nonblank_methods.sort(key=sort_access_method)
    #Otherwise, go over each valid method and assign
    for index, each_method in enumerate(nonblank_methods):
        items_list = {}
        for each_req in each_method.required_items:
            if each_req.startswith(tuple([CARNIVAL_1 + " Rocket", PREHISTORIC_3 + " Lower Monolith", FEAR_1 + " Progressive Doorway", FEAR_2 + " Progressive Gate"])):
                prog_switch_name = each_req[:-2]
                prog_switch_count = int(each_req[-1:])
                items_list[prog_switch_name] = prog_switch_count
            else:
                items_list[each_req] = 1
        #Start with the rule set
        if index == 0:
            set_rule(spot, lambda state, required_items = items_list : state.has_all_counts(required_items, self.player))
            continue
        #Otherwise, this is an alternate method
        add_rule(spot, lambda state, required_items = items_list : state.has_all_counts(required_items, self.player), "or")

#Move all methods that require switches to the end of the list
def sort_access_method(in_method):
    for each_requirement in in_method.required_items:
        #Switches
        if not each_requirement in move_lookup:
            return 1
    return 0
