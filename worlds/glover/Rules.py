from typing import TYPE_CHECKING

from BaseClasses import Entrance, Location
from worlds.generic.Rules import add_rule, set_rule
from .Options import DifficultyLogic
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
    GloverWorld.ATLANTIS_1 + ": Glover Switch"               : GloverWorld.ATLANTIS_1 + " Gate",
    GloverWorld.ATLANTIS_2 + ": Drain Block"                 : GloverWorld.ATLANTIS_2 + " Elevator",
    GloverWorld.ATLANTIS_2 + ": Ball Switch"                 : GloverWorld.ATLANTIS_2 + " Ballswitch Drain",
    GloverWorld.ATLANTIS_2 + ": Glover Switch"               : GloverWorld.ATLANTIS_2 + " Gate",
    GloverWorld.ATLANTIS_3 + ": Pyramid Ball Switch"         : GloverWorld.ATLANTIS_3 + " Waterwheel",
    GloverWorld.ATLANTIS_3 + ": Cliff Ball Switch"           : GloverWorld.ATLANTIS_3 + " Cave Platforms",
    GloverWorld.CARNIVAL_1 + ": Conveyor Target"             : GloverWorld.CARNIVAL_1 + " Elevator",
    GloverWorld.CARNIVAL_1 + ": Bars Glover Switch"          : GloverWorld.CARNIVAL_1 + " Gate",
    GloverWorld.CARNIVAL_1 + ": Ramp Ball Switch"            : GloverWorld.CARNIVAL_1 + " Door A",
    GloverWorld.CARNIVAL_1 + ": Ice Cream Glover Switch"     : GloverWorld.CARNIVAL_1 + " Door B",
    GloverWorld.CARNIVAL_1 + ": Slide Glover Switch"         : GloverWorld.CARNIVAL_1 + " Door C",
    GloverWorld.CARNIVAL_1 + ": Whack-A-Mole Glover Switch"  : GloverWorld.CARNIVAL_1 + " Rocket",
    GloverWorld.CARNIVAL_1 + ": Plinko Glover Switch"        : GloverWorld.CARNIVAL_1 + " Rocket",
    GloverWorld.CARNIVAL_1 + ": Slots Glover Switch"         : GloverWorld.CARNIVAL_1 + " Rocket",
    GloverWorld.CARNIVAL_2 + ": Clown Teeth"                 : GloverWorld.CARNIVAL_2 + " Drop Garibs",
    GloverWorld.CARNIVAL_2 + ": Ball Switch"                 : GloverWorld.CARNIVAL_2 + " Fan",
    GloverWorld.CARNIVAL_3 + ": Glover Switch"               : GloverWorld.CARNIVAL_3 + " Spin Door",
    GloverWorld.CARNIVAL_3 + ": Ball Switch"                 : GloverWorld.CARNIVAL_3 + " Hands",
    GloverWorld.PIRATES_1 + ": Ship Target"                  : GloverWorld.PIRATES_1 + " Raise Beach",
    GloverWorld.PIRATES_1 + ": Tower Glover Switch"          : GloverWorld.PIRATES_1 + " Elevator",
    GloverWorld.PIRATES_1 + ": Coast Target"                 : GloverWorld.PIRATES_1 + " Chest",
    GloverWorld.PIRATES_1 + ": Fan Ball Switch"              : GloverWorld.PIRATES_1 + " Sandpile",
    GloverWorld.PIRATES_1 + ": Sand Ball Switch"             : GloverWorld.PIRATES_1 + " Waterspout",
    GloverWorld.PIRATES_1 + ": Lighthouse Target"            : GloverWorld.PIRATES_1 + " Lighthouse",
    GloverWorld.PIRATES_1 + ": Lighthouse Glover Switch"     : GloverWorld.PIRATES_1 + " Raise Ship",
    GloverWorld.PIRATES_1 + ": Crate Ball Switch"            : GloverWorld.PIRATES_1 + " Bridge",
    GloverWorld.PIRATES_2 + ": Glover Switch"                : GloverWorld.PIRATES_2 + " Lower Water",
    GloverWorld.PIRATES_2 + ": Water Ball Switch"            : GloverWorld.PIRATES_2 + " Ramp",
    GloverWorld.PIRATES_2 + ": Platform Ball Switch"         : GloverWorld.PIRATES_2 + " Gate",
    #GloverWorld.PIRATES_3 + ": "                            : GloverWorld.PIRATES_3 + " Platform Spin",
    GloverWorld.PIRATES_3 + ": Cliff Glover Switch"          : GloverWorld.PIRATES_3 + " Trampoline",
    GloverWorld.PIRATES_3 + ": Target"                       : GloverWorld.PIRATES_3 + " Stairs",
    GloverWorld.PIRATES_3 + ": Ball Switch"                  : GloverWorld.PIRATES_3 + " Elevator",
    GloverWorld.PREHISTORIC_1 + ": Icicles"                  : GloverWorld.PREHISTORIC_1 + " Life Drop",
    GloverWorld.PREHISTORIC_2 + ": Lavafall Ball Switch"     : GloverWorld.PREHISTORIC_2 + " Platform 1",
    GloverWorld.PREHISTORIC_2 + ": Switches Ball Switch"     : GloverWorld.PREHISTORIC_2 + " Platform 2",
    GloverWorld.PREHISTORIC_2 + ": Glover Switch"            : GloverWorld.PREHISTORIC_2 + " Lower Ball Switch",
    GloverWorld.PREHISTORIC_3 + ": Tracey Tree"              : GloverWorld.PREHISTORIC_3 + " Drop Garibs",
    GloverWorld.PREHISTORIC_3 + ": Trees Glover Switch"      : GloverWorld.PREHISTORIC_3 + " Spin Stones",
    GloverWorld.PREHISTORIC_3 + ": Monolith A"               : GloverWorld.PREHISTORIC_3 + " Lower Monolith",
    GloverWorld.PREHISTORIC_3 + ": Monolith B"               : GloverWorld.PREHISTORIC_3 + " Lower Monolith",
    GloverWorld.PREHISTORIC_3 + ": Monolith C"               : GloverWorld.PREHISTORIC_3 + " Lower Monolith",
    GloverWorld.PREHISTORIC_3 + ": Monolith D"               : GloverWorld.PREHISTORIC_3 + " Lower Monolith",
    GloverWorld.PREHISTORIC_3 + ": Monolith Ball Switch"     : GloverWorld.PREHISTORIC_3 + " Floating Platforms",
    GloverWorld.PREHISTORIC_3 + ": Flying Lava Ball Switch"  : GloverWorld.PREHISTORIC_3 + " Lava Spinning",
    GloverWorld.PREHISTORIC_3 + ": Lava Pit Ball Switch"     : GloverWorld.PREHISTORIC_3 + " Dirt Elevator",
    GloverWorld.FEAR_1 + ": Dead-End Glover Switch"          : GloverWorld.FEAR_1 + " Coffin",
    GloverWorld.FEAR_1 + ": Left Target"                     : GloverWorld.FEAR_1 + " Progressive Doorway",
    GloverWorld.FEAR_1 + ": Right Target"                    : GloverWorld.FEAR_1 + " Progressive Doorway",
    GloverWorld.FEAR_1 + ": Push Blocks"                     : GloverWorld.FEAR_1 + " Coffin Lightning",
    GloverWorld.FEAR_1 + ": Coffin Glover Switch"            : GloverWorld.FEAR_1 + " Drawbridge",
    GloverWorld.FEAR_2 + ": Push Target"                     : GloverWorld.FEAR_2 + " Garibs Fall",
    GloverWorld.FEAR_2 + ": Push Switch"                     : GloverWorld.FEAR_2 + " Progressive Gate",
    GloverWorld.FEAR_2 + ": Slope Target"                    : GloverWorld.FEAR_2 + " Progressive Gate",
    GloverWorld.FEAR_2 + ": Mummy"                           : GloverWorld.FEAR_2 + " Mummy Gate",
    GloverWorld.FEAR_3 + ": Target"                          : GloverWorld.FEAR_3 + " Gate",
    GloverWorld.FEAR_3 + ": Ball Switch"                     : GloverWorld.FEAR_3 + " Spikes",
    #GloverWorld. + ": "                                     : GloverWorld.SPACE_1 + " Aliens",
    GloverWorld.SPACE_1 + ": Sign Glover Switch"             : GloverWorld.SPACE_1 + " Fans",
    GloverWorld.SPACE_1 + ": Stone Pillar Ball Switch"       : GloverWorld.SPACE_1 + " Flying Platforms",
    GloverWorld.SPACE_1 + ": Cliff Glover Switch"            : GloverWorld.SPACE_1 + " Goo Platforms",
    GloverWorld.SPACE_1 + ": Hazard Stripe Ball Switch"      : GloverWorld.SPACE_1 + " UFO",
    GloverWorld.SPACE_1 + ": UFO Glover Switch"              : GloverWorld.SPACE_1 + " Missile",
    GloverWorld.SPACE_2 + ": Right Platform Ball Switch"     : GloverWorld.SPACE_2 + " Mashers",
    GloverWorld.SPACE_2 + ": Cliff Ball Switch"              : GloverWorld.SPACE_2 + " Ramp",
    GloverWorld.SPACE_3 + ": Duel Switch"                    : GloverWorld.SPACE_3 + " Hazard Gate",
    GloverWorld.SPACE_3 + ": Conveyor Glover Switch"         : GloverWorld.SPACE_3 + " Sign",
    GloverWorld.SPACE_3 + ": Above Fan Red Switch"           : GloverWorld.SPACE_3 + " Fan",
    GloverWorld.SPACE_3 + ": Magnet Ball Switch"             : GloverWorld.SPACE_3 + " Bridge",
    GloverWorld.SPACE_3 + ": Ball Switch"                    : GloverWorld.SPACE_3 + " Glass Gate",
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
            if each_req.startswith(tuple([GloverWorld.CARNIVAL_1 + " Rocket", GloverWorld.PREHISTORIC_3 + " Lower Monolith", GloverWorld.FEAR_1 + " Progressive Doorway", GloverWorld.FEAR_2 + " Progressive Gate"])):
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
