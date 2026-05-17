from typing import NamedTuple, TYPE_CHECKING

from Options import OptionError
from .Options import GaribLogic, GaribSorting
from .LevelPrefixes import *

if TYPE_CHECKING:
    from . import GloverWorld
else:
    GloverWorld = object

class ItemData(NamedTuple):
	glid: int|None = None
	qty: int = 0
	type: str = ""
	default_location: str = ""

def find_item_data(self, name : str) -> ItemData:
	#Garib Groups
	if name in world_garib_table:
		return world_garib_table[name]
	if name in garibsanity_world_table:
		return garibsanity_world_table[name]
	#Decoupled garibs
	if name in decoupled_garib_table:
		#Include bonus level garibs in the count
		if self.options.bonus_levels:
			return decoupled_garib_table[name]
		else:
			#If there's no bonus garib groups with this count, the quantity stays the same
			if not name in decoupled_garib_bonus_count:
				return decoupled_garib_table[name]
			#Otherwise remove bonus level garibs from the count
			modified_item = decoupled_garib_table[name]
			return ItemData(modified_item.glid, modified_item.qty - decoupled_garib_bonus_count[name], modified_item.type, modified_item.default_location)
	if name == "Garibsanity":
		#Include bonus level garibs in the count
		if self.options.bonus_levels:
			return garbinsanity
		else:
			#Remove bonus level garibs from the count
			return ItemData(garbinsanity.glid, garbinsanity.qty - garbinsanity_bonus_count, garbinsanity.type, garbinsanity.default_location)
	#Extra garibs become other items
	if name == "Extra Garibs":
		modified_item = convert_extra_garibs(self)
		#But filler
		return ItemData(modified_item.glid, modified_item.qty, "Filler", modified_item.default_location)

	#Core
	if name in portalsanity_table:
		#As event item?
		if self.options.portalsanity:
			return portalsanity_table[name]
		else:
			modified_item = portalsanity_table[name]
			return ItemData(None, modified_item.qty, modified_item.type, modified_item.default_location)
	if name in level_event_table:
		#As event item?
		if self.options.switches_checks:
			return level_event_table[name]
		else:
			modified_item = level_event_table[name]
			return ItemData(None, modified_item.qty, modified_item.type, modified_item.default_location)
	if name in checkpoint_table:
		if self.options.checkpoint_checks:
			return checkpoint_table[name]
		else:
			modified_item = checkpoint_table[name]
			return ItemData(None, modified_item.qty, modified_item.type, modified_item.default_location)
	if name in potion_table:
		return potion_table[name]
	if name in move_table:
		return move_table[name]
	
	#Filler
	if name in filler_table:
		return filler_table[name]
	if name in trap_table:
		return trap_table[name]
	
	#Golden Garibs
	if name == "Golden Garib":
		out_data : ItemData = misc_table["Golden Garib"]
		return ItemData(out_data.glid, self.options.golden_garib_count.value, out_data.type, out_data.default_location)

	#Fallthrough
	return ItemData()

BASE_ID = 6500000

misc_table = {
	"Golden Garib" :							ItemData(BASE_ID + 99999, -1, "Proguseful", None)
	}

portalsanity_table = {
	ATLANTIS_HUB + " 1 Star" : 			ItemData(BASE_ID + 0, 1, "Star", ATLANTIS_1 + ": All Garibs"),
	ATLANTIS_HUB + " 2 Gate" : 			ItemData(BASE_ID + 1, 1, "Progression", ATLANTIS_1 + ": Goal"),
	ATLANTIS_HUB + " 2 Star" : 			ItemData(BASE_ID + 2, 1, "Star", ATLANTIS_2 + ": All Garibs"),
	ATLANTIS_HUB + " 3 Gate" : 			ItemData(BASE_ID + 3, 1, "Progression", ATLANTIS_2 + ": Goal"),
	ATLANTIS_HUB + " 3 Star" : 			ItemData(BASE_ID + 4, 1, "Star", ATLANTIS_3 + ": All Garibs"),
	ATLANTIS_HUB + " Boss Gate" : 		ItemData(BASE_ID + 5, 1, "Progression", ATLANTIS_3 + ": Goal"),
	ATLANTIS_HUB + " Boss Star" : 		ItemData(BASE_ID + 6, 1, "Star", ATLANTIS_BOSS + ": Goal"),
	ATLANTIS_HUB + " Bonus Gate" : 		ItemData(BASE_ID + 7, 1, "Progression", ATLANTIS_HUB + ": Bonus Unlock"),
	ATLANTIS_HUB + " Bonus Star" : 		ItemData(BASE_ID + 8, 1, "Star", ATLANTIS_BONUS + ": All Garibs"),
	CARNIVAL_HUB + " 1 Star" : 			ItemData(BASE_ID + 15, 1, "Star", CARNIVAL_1 + ": All Garibs"),
	CARNIVAL_HUB + " 2 Gate" : 			ItemData(BASE_ID + 16, 1, "Progression", CARNIVAL_1 + ": Goal"),
	CARNIVAL_HUB + " 2 Star" : 			ItemData(BASE_ID + 17, 1, "Star", CARNIVAL_2 + ": All Garibs"),
	CARNIVAL_HUB + " 3 Gate" : 			ItemData(BASE_ID + 18, 1, "Progression", CARNIVAL_2 + ": Goal"),
	CARNIVAL_HUB + " 3 Star" : 			ItemData(BASE_ID + 19, 1, "Star", CARNIVAL_3 + ": All Garibs"),
	CARNIVAL_HUB + " Boss Gate" : 		ItemData(BASE_ID + 20, 1, "Progression", CARNIVAL_3 + ": Goal"),
	CARNIVAL_HUB + " Boss Star" : 		ItemData(BASE_ID + 21, 1, "Star", CARNIVAL_BOSS + ": Goal"),
	CARNIVAL_HUB + " Bonus Gate" : 		ItemData(BASE_ID + 22, 1, "Progression", CARNIVAL_HUB + ": Bonus Unlock"),
	CARNIVAL_HUB + " Bonus Star" : 		ItemData(BASE_ID + 23, 1, "Star", CARNIVAL_BONUS + ": All Garibs"),
	PIRATES_HUB + " 1 Star" : 			ItemData(BASE_ID + 36, 1, "Star", PIRATES_1 + ": All Garibs"),
	PIRATES_HUB + " 2 Gate" : 			ItemData(BASE_ID + 37, 1, "Progression", PIRATES_1 + ": Goal"),
	PIRATES_HUB + " 2 Star" : 			ItemData(BASE_ID + 38, 1, "Star", PIRATES_2 + ": All Garibs"),
	PIRATES_HUB + " 3 Gate" : 			ItemData(BASE_ID + 39, 1, "Progression", PIRATES_2 + ": Goal"),
	PIRATES_HUB + " 3 Star" : 			ItemData(BASE_ID + 40, 1, "Star", PIRATES_3 + ": All Garibs"),
	PIRATES_HUB + " Boss Gate" : 		ItemData(BASE_ID + 41, 1, "Progression", PIRATES_3 + ": Goal"),
	PIRATES_HUB + " Boss Star" : 		ItemData(BASE_ID + 42, 1, "Star", PIRATES_BOSS + ": Goal"),
	PIRATES_HUB + " Bonus Gate" : 		ItemData(BASE_ID + 43, 1, "Progression", PIRATES_HUB + ": Bonus Unlock"),
	PIRATES_HUB + " Bonus Star" : 		ItemData(BASE_ID + 44, 1, "Star", PIRATES_BONUS + ": All Garibs"),
	PREHISTORIC_HUB + " 1 Star" : 		ItemData(BASE_ID + 60, 1, "Star", PREHISTORIC_1 + ": All Garibs"),
	PREHISTORIC_HUB + " 2 Gate" : 		ItemData(BASE_ID + 61, 1, "Progression", PREHISTORIC_1 + ": Goal"),
	PREHISTORIC_HUB + " 2 Star" : 		ItemData(BASE_ID + 62, 1, "Star", PREHISTORIC_2 + ": All Garibs"),
	PREHISTORIC_HUB + " 3 Gate" : 		ItemData(BASE_ID + 63, 1, "Progression", PREHISTORIC_2 + ": Goal"),
	PREHISTORIC_HUB + " 3 Star" : 		ItemData(BASE_ID + 64, 1, "Star", PREHISTORIC_3 + ": All Garibs"),
	PREHISTORIC_HUB + " Boss Gate" : 	ItemData(BASE_ID + 65, 1, "Progression", PREHISTORIC_3 + ": Goal"),
	PREHISTORIC_HUB + " Boss Star" : 	ItemData(BASE_ID + 66, 1, "Star", PREHISTORIC_BOSS + ": Goal"),
	PREHISTORIC_HUB + " Bonus Gate" : 	ItemData(BASE_ID + 67, 1, "Progression", PREHISTORIC_HUB + ": Bonus Unlock"),
	PREHISTORIC_HUB + " Bonus Star" : 	ItemData(BASE_ID + 68, 1, "Star", PREHISTORIC_BONUS + ": All Garibs"),
	FEAR_HUB + " 1 Star" : 				ItemData(BASE_ID + 82, 1, "Star", FEAR_1 + ": All Garibs"),
	FEAR_HUB + " 2 Gate" : 				ItemData(BASE_ID + 83, 1, "Progression", FEAR_1 + ": Goal"),
	FEAR_HUB + " 2 Star" : 				ItemData(BASE_ID + 84, 1, "Star", FEAR_2 + ": All Garibs"),
	FEAR_HUB + " 3 Gate" : 				ItemData(BASE_ID + 85, 1, "Progression", FEAR_2 + ": Goal"),
	FEAR_HUB + " 3 Star" : 				ItemData(BASE_ID + 86, 1, "Star", FEAR_3 + ": All Garibs"),
	FEAR_HUB + " Boss Gate" : 			ItemData(BASE_ID + 87, 1, "Progression", FEAR_3 + ": Goal"),
	FEAR_HUB + " Boss Star" : 			ItemData(BASE_ID + 88, 1, "Star", FEAR_BOSS + ": Goal"),
	FEAR_HUB + " Bonus Gate" : 			ItemData(BASE_ID + 89, 1, "Progression", FEAR_HUB + ": Bonus Unlock"),
	FEAR_HUB + " Bonus Star" : 			ItemData(BASE_ID + 90, 1, "Star", FEAR_BONUS + ": All Garibs"),
	SPACE_HUB + " 1 Star" : 			ItemData(BASE_ID + 99, 1, "Star", SPACE_1 + ": All Garibs"),
	SPACE_HUB + " 2 Gate" : 			ItemData(BASE_ID + 100, 1, "Progression", SPACE_1 + ": Goal"),
	SPACE_HUB + " 2 Star" : 			ItemData(BASE_ID + 101, 1, "Star", SPACE_2 + ": All Garibs"),
	SPACE_HUB + " 3 Gate" : 			ItemData(BASE_ID + 102, 1, "Progression", SPACE_2 + ": Goal"),
	SPACE_HUB + " 3 Star" : 			ItemData(BASE_ID + 103, 1, "Star", SPACE_3 + ": All Garibs"),
	SPACE_HUB + " Boss Gate" : 			ItemData(BASE_ID + 104, 1, "Progression", SPACE_3 + ": Goal"),
	SPACE_HUB + " Boss Star" : 			ItemData(BASE_ID + 105, 1, "Star", SPACE_BOSS + ": Goal"),
	SPACE_HUB + " Bonus Gate" : 		ItemData(BASE_ID + 106, 1, "Progression", SPACE_HUB + ": Bonus Unlock"),
	SPACE_HUB + " Bonus Star" : 		ItemData(BASE_ID + 107, 1, "Star", SPACE_BONUS + ": All Garibs")
}

level_event_table = {
	ATLANTIS_1 + " Gate" : 					ItemData(BASE_ID + 9, 1, "Progression", ATLANTIS_1 + ": Glover Switch"),
	ATLANTIS_2 + " Elevator" : 				ItemData(BASE_ID + 10, 1, "Progression", ATLANTIS_2 + ": Drain Block"),
	ATLANTIS_2 + " Ball Switch Drain" : 	ItemData(BASE_ID + 11, 1, "Progression", ATLANTIS_2 + ": Ball Switch"),
	ATLANTIS_2 + " Gate" : 					ItemData(BASE_ID + 12, 1, "Progression", ATLANTIS_2 + ": Glover Switch"),
	ATLANTIS_3 + " Waterwheel" : 			ItemData(BASE_ID + 13, 1, "Progression", ATLANTIS_3 + ": Pyramid Ball Switch"),
	ATLANTIS_3 + " Cave Platforms" : 		ItemData(BASE_ID + 14, 1, "Progression", ATLANTIS_3 + ": Cliff Ball Switch"),
	CARNIVAL_1 + " Elevator" : 				ItemData(BASE_ID + 24, 1, "Progression", CARNIVAL_1 + ": Conveyor Target"),
	CARNIVAL_1 + " Gate" : 					ItemData(BASE_ID + 25, 1, "Progression", CARNIVAL_1 + ": Bars Glover Switch"),
	CARNIVAL_1 + " Door A" : 				ItemData(BASE_ID + 26, 1, "Progression", CARNIVAL_1 + ": Ramp Ball Switch"),
	CARNIVAL_1 + " Door B" : 				ItemData(BASE_ID + 27, 1, "Progression", CARNIVAL_1 + ": Ice Cream Glover Switch"),
	CARNIVAL_1 + " Door C" : 				ItemData(BASE_ID + 28, 1, "Progression", CARNIVAL_1 + ": Slide Glover Switch"),
	CARNIVAL_1 + " Rocket" : 				ItemData(BASE_ID + 29, 3, "Progression"),
	CARNIVAL_2 + " Drop Garibs" : 			ItemData(BASE_ID + 32, 1, "Progression", CARNIVAL_2 + ": Clown Teeth"),
	CARNIVAL_2 + " Fan" : 					ItemData(BASE_ID + 33, 1, "Progression", CARNIVAL_2 + ": Ball Switch"),
	CARNIVAL_3 + " Spin Door" : 			ItemData(BASE_ID + 34, 1, "Progression", CARNIVAL_3 + ": Glover Switch"),
	CARNIVAL_3 + " Hands" : 				ItemData(BASE_ID + 35, 1, "Progression", CARNIVAL_3 + ": Ball Switch"),
	PIRATES_1 + " Raise Beach" : 			ItemData(BASE_ID + 45, 1, "Progression", PIRATES_1 + ": Ship Target"),
	PIRATES_1 + " Elevator" : 				ItemData(BASE_ID + 46, 1, "Progression", PIRATES_1 + ": Tower Glover Switch"),
	PIRATES_1 + " Chest" : 					ItemData(BASE_ID + 47, 1, "Progression", PIRATES_1 + ": Coast Target"),
	PIRATES_1 + " Sandpile" : 				ItemData(BASE_ID + 48, 1, "Progression", PIRATES_1 + ": Fan Ball Switch"),
	PIRATES_1 + " Waterspout" : 			ItemData(BASE_ID + 49, 1, "Progression", PIRATES_1 + ": Sand Ball Switch"),
	PIRATES_1 + " Lighthouse" : 			ItemData(BASE_ID + 50, 1, "Progression", PIRATES_1 + ": Lighthouse Target"),
	PIRATES_1 + " Raise Ship" : 			ItemData(BASE_ID + 51, 1, "Progression", PIRATES_1 + ": Lighthouse Glover Switch"),
	PIRATES_1 + " Bridge" : 				ItemData(BASE_ID + 52, 1, "Progression", PIRATES_1 + ": Crate Ball Switch"),
	PIRATES_2 + " Lower Water" : 			ItemData(BASE_ID + 53, 1, "Progression", PIRATES_2 + ": Glover Switch"),
	PIRATES_2 + " Ramp" : 					ItemData(BASE_ID + 54, 1, "Progression", PIRATES_2 + ": Water Ball Switch"),
	PIRATES_2 + " Gate" : 					ItemData(BASE_ID + 55, 1, "Progression", PIRATES_2 + ": Platform Ball Switch"),
	#PIRATES_3 + " Platform Spin" : 		ItemData(BASE_ID + 56, 1, "Progression", ),
	PIRATES_3 + " Trampoline" : 			ItemData(BASE_ID + 57, 1, "Progression", PIRATES_3 + ": Cliff Glover Switch"),
	PIRATES_3 + " Stairs" : 				ItemData(BASE_ID + 58, 1, "Progression", PIRATES_3 + ": Target"),
	PIRATES_3 + " Elevator" : 				ItemData(BASE_ID + 59, 1, "Progression", PIRATES_3 + ": Ball Switch"),
	PREHISTORIC_1 + " Life Drop" : 			ItemData(BASE_ID + 69, 1, "Progression", PREHISTORIC_1 + ": Icicles"),
	PREHISTORIC_2 + " Platform 1" : 		ItemData(BASE_ID + 70, 1, "Progression", PREHISTORIC_2 + ": Lavafall Ball Switch"),
	PREHISTORIC_2 + " Platform 2" : 		ItemData(BASE_ID + 71, 1, "Progression", PREHISTORIC_2 + ": Switches Ball Switch"),
	PREHISTORIC_2 + " Lower Ball Switch" : 	ItemData(BASE_ID + 72, 1, "Progression", PREHISTORIC_2 + ": Glover Switch"),
	PREHISTORIC_3 + " Drop Garibs" : 		ItemData(BASE_ID + 73, 1, "Progression", PREHISTORIC_3 + ": Tracey Tree"),
	PREHISTORIC_3 + " Spin Stones" : 		ItemData(BASE_ID + 74, 1, "Progression", PREHISTORIC_3 + ": Trees Glover Switch"),
	PREHISTORIC_3 + " Lower Monolith" : 	ItemData(BASE_ID + 75, 4, "Progression", ""),
	PREHISTORIC_3 + " Floating Platforms" : ItemData(BASE_ID + 79, 1, "Progression", PREHISTORIC_3 + ": Monolith Ball Switch"),
	PREHISTORIC_3 + " Lava Spinning" : 		ItemData(BASE_ID + 80, 1, "Progression", PREHISTORIC_3 + ": Flying Lava Ball Switch"),
	PREHISTORIC_3 + " Dirt Elevator" : 		ItemData(BASE_ID + 81, 1, "Progression", PREHISTORIC_3 + ": Lava Pit Ball Switch"),
	FEAR_1 + " Coffin" : 					ItemData(BASE_ID + 91, 1, "Progression", FEAR_1 + ": Dead-End Glover Switch"),
	FEAR_1 + " Progressive Doorway" : 		ItemData(BASE_ID + 76, 2, "Progression", ""),
	FEAR_1 + " Coffin Lightning" : 			ItemData(BASE_ID + 92, 1, "Progression", FEAR_1 + ": Push Blocks"),
	FEAR_1 + " Drawbridge" : 				ItemData(BASE_ID + 93, 1, "Progression", FEAR_1 + ": Coffin Glover Switch"),
	FEAR_2 + " Garibs Fall" : 				ItemData(BASE_ID + 94, 1, "Progression", FEAR_2 + ": Push Target"),
	FEAR_2 + " Progressive Gate" : 			ItemData(BASE_ID + 95, 2, "Progression", ""),
	FEAR_2 + " Mummy Gate" : 				ItemData(BASE_ID + 96, 1, "Progression", FEAR_2 + ": Mummy"),
	FEAR_3 + " Gate" : 						ItemData(BASE_ID + 97, 1, "Progression", FEAR_3 + ": Target"),
	FEAR_3 + " Spikes" : 					ItemData(BASE_ID + 98, 1, "Progression", FEAR_3 + ": Ball Switch"),
	#SPACE_1 + " Aliens" : 					ItemData(BASE_ID + 108, 1, "Progression", ),
	SPACE_1 + " Fans" : 					ItemData(BASE_ID + 109, 1, "Progression", SPACE_1 + ": Sign Glover Switch"),
	SPACE_1 + " Flying Platforms" : 		ItemData(BASE_ID + 110, 1, "Progression", SPACE_1 + ": Stone Pillar Ball Switch"),
	SPACE_1 + " Goo Platforms" : 			ItemData(BASE_ID + 111, 1, "Progression", SPACE_1 + ": Cliff Glover Switch"),
	SPACE_1 + " UFO" : 						ItemData(BASE_ID + 112, 1, "Progression", SPACE_1 + ": Hazard Stripe Ball Switch"),
	SPACE_1 + " Missile" : 					ItemData(BASE_ID + 113, 1, "Progression", SPACE_1 + ": UFO Glover Switch"),
	SPACE_2 + " Mashers" : 					ItemData(BASE_ID + 114, 1, "Progression", SPACE_2 + ": Right Platform Ball Switch"),
	SPACE_2 + " Ramp" : 					ItemData(BASE_ID + 115, 1, "Progression", SPACE_2 + ": Cliff Ball Switch"),
	SPACE_3 + " Hazard Gate" : 				ItemData(BASE_ID + 116, 1, "Progression", SPACE_3 + ": Duel Switch"),
	SPACE_3 + " Sign" : 					ItemData(BASE_ID + 117, 1, "Progression", SPACE_3 + ": Conveyor Glover Switch"),
	SPACE_3 + " Fan" : 						ItemData(BASE_ID + 118, 1, "Progression", SPACE_3 + ": Above Fan Red Switch"),
	SPACE_3 + " Bridge" : 					ItemData(BASE_ID + 119, 1, "Progression", SPACE_3 + ": Magnet Ball Switch"),
	SPACE_3 + " Glass Gate" : 				ItemData(BASE_ID + 120, 1, "Progression", SPACE_3 + ": Ball Switch"),
	"Training Sandpit" : 								ItemData(BASE_ID + 127, 1, "Progression", "Training: Ball Switch"),
	"Training Lower Target" : 							ItemData(BASE_ID + 128, 1, "Progression", "Training: Glover Switch"),
	"Training Stairs" : 								ItemData(BASE_ID + 129, 1, "Progression", "Training: Target")
	}

checkpoint_table = {
	ATLANTIS_1 + " Checkpoint 1" : 		ItemData(BASE_ID + 130, 1, "Progression", ATLANTIS_1 + ": Checkpoint 1"),
	ATLANTIS_1 + " Checkpoint 2" : 		ItemData(BASE_ID + 131, 1, "Progression", ATLANTIS_1 + ": Checkpoint 2"),
	ATLANTIS_2 + " Checkpoint 1" : 		ItemData(BASE_ID + 132, 1, "Progression", ATLANTIS_2 + ": Checkpoint 1"),
	ATLANTIS_2 + " Checkpoint 2" : 		ItemData(BASE_ID + 133, 1, "Progression", ATLANTIS_2 + ": Checkpoint 2"),
	ATLANTIS_2 + " Checkpoint 3" : 		ItemData(BASE_ID + 134, 1, "Progression", ATLANTIS_2 + ": Checkpoint 3"),
	ATLANTIS_3 + " Checkpoint 1" : 		ItemData(BASE_ID + 135, 1, "Progression", ATLANTIS_3 + ": Checkpoint 1"),
	ATLANTIS_3 + " Checkpoint 2" : 		ItemData(BASE_ID + 136, 1, "Progression", ATLANTIS_3 + ": Checkpoint 2"),
	ATLANTIS_3 + " Checkpoint 3" : 		ItemData(BASE_ID + 137, 1, "Progression", ATLANTIS_3 + ": Checkpoint 3"),
	CARNIVAL_1 + " Checkpoint 1" : 		ItemData(BASE_ID + 138, 1, "Progression", CARNIVAL_1 + ": Checkpoint 1"),
	CARNIVAL_1 + " Checkpoint 2" : 		ItemData(BASE_ID + 139, 1, "Progression", CARNIVAL_1 + ": Checkpoint 2"),
	CARNIVAL_1 + " Checkpoint 3" : 		ItemData(BASE_ID + 140, 1, "Progression", CARNIVAL_1 + ": Checkpoint 3"),
	CARNIVAL_1 + " Checkpoint 4" : 		ItemData(BASE_ID + 141, 1, "Progression", CARNIVAL_1 + ": Checkpoint 4"),
	CARNIVAL_2 + " Checkpoint 1" : 		ItemData(BASE_ID + 142, 1, "Progression", CARNIVAL_2 + ": Checkpoint 1"),
	CARNIVAL_2 + " Checkpoint 2" : 		ItemData(BASE_ID + 143, 1, "Progression", CARNIVAL_2 + ": Checkpoint 2"),
	CARNIVAL_2 + " Checkpoint 3" : 		ItemData(BASE_ID + 144, 1, "Progression", CARNIVAL_2 + ": Checkpoint 3"),
	CARNIVAL_2 + " Checkpoint 4" : 		ItemData(BASE_ID + 145, 1, "Progression", CARNIVAL_2 + ": Checkpoint 4"),
	CARNIVAL_2 + " Checkpoint 5" : 		ItemData(BASE_ID + 146, 1, "Progression", CARNIVAL_2 + ": Checkpoint 5"),
	CARNIVAL_3 + " Checkpoint 1" : 		ItemData(BASE_ID + 147, 1, "Progression", CARNIVAL_3 + ": Checkpoint 1"),
	CARNIVAL_3 + " Checkpoint 2" : 		ItemData(BASE_ID + 148, 1, "Progression", CARNIVAL_3 + ": Checkpoint 2"),
	CARNIVAL_3 + " Checkpoint 3" : 		ItemData(BASE_ID + 149, 1, "Progression", CARNIVAL_3 + ": Checkpoint 3"),
	CARNIVAL_3 + " Checkpoint 4" : 		ItemData(BASE_ID + 150, 1, "Progression", CARNIVAL_3 + ": Checkpoint 4"),
	PIRATES_1 + " Checkpoint 1" : 		ItemData(BASE_ID + 151, 1, "Progression", PIRATES_1 + ": Checkpoint 1"),
	PIRATES_1 + " Checkpoint 2" : 		ItemData(BASE_ID + 152, 1, "Progression", PIRATES_1 + ": Checkpoint 2"),
	PIRATES_1 + " Checkpoint 3" : 		ItemData(BASE_ID + 153, 1, "Progression", PIRATES_1 + ": Checkpoint 3"),
	PIRATES_2 + " Checkpoint 1" : 		ItemData(BASE_ID + 154, 1, "Progression", PIRATES_2 + ": Checkpoint 1"),
	PIRATES_2 + " Checkpoint 2" : 		ItemData(BASE_ID + 155, 1, "Progression", PIRATES_2 + ": Checkpoint 2"),
	PIRATES_2 + " Checkpoint 3" : 		ItemData(BASE_ID + 156, 1, "Progression", PIRATES_2 + ": Checkpoint 3"),
	PIRATES_3 + " Checkpoint 1" : 		ItemData(BASE_ID + 157, 1, "Progression", PIRATES_3 + ": Checkpoint 1"),
	PIRATES_3 + " Checkpoint 2" : 		ItemData(BASE_ID + 158, 1, "Progression", PIRATES_3 + ": Checkpoint 2"),
	PIRATES_3 + " Checkpoint 3" : 		ItemData(BASE_ID + 159, 1, "Progression", PIRATES_3 + ": Checkpoint 3"),
	PIRATES_3 + " Checkpoint 4" : 		ItemData(BASE_ID + 160, 1, "Progression", PIRATES_3 + ": Checkpoint 4"),
	PREHISTORIC_1 + " Checkpoint 1" : 	ItemData(BASE_ID + 161, 1, "Progression", PREHISTORIC_1 + ": Checkpoint 1"),
	PREHISTORIC_1 + " Checkpoint 2" : 	ItemData(BASE_ID + 162, 1, "Progression", PREHISTORIC_1 + ": Checkpoint 2"),
	PREHISTORIC_1 + " Checkpoint 3" : 	ItemData(BASE_ID + 163, 1, "Progression", PREHISTORIC_1 + ": Checkpoint 3"),
	PREHISTORIC_2 + " Checkpoint 1" : 	ItemData(BASE_ID + 164, 1, "Progression", PREHISTORIC_2 + ": Checkpoint 1"),
	PREHISTORIC_2 + " Checkpoint 2" : 	ItemData(BASE_ID + 165, 1, "Progression", PREHISTORIC_2 + ": Checkpoint 2"),
	PREHISTORIC_2 + " Checkpoint 3" : 	ItemData(BASE_ID + 166, 1, "Progression", PREHISTORIC_2 + ": Checkpoint 3"),
	PREHISTORIC_2 + " Checkpoint 4" : 	ItemData(BASE_ID + 167, 1, "Progression", PREHISTORIC_2 + ": Checkpoint 4"),
	PREHISTORIC_3 + " Checkpoint 1" : 	ItemData(BASE_ID + 168, 1, "Progression", PREHISTORIC_3 + ": Checkpoint 1"),
	PREHISTORIC_3 + " Checkpoint 2" : 	ItemData(BASE_ID + 169, 1, "Progression", PREHISTORIC_3 + ": Checkpoint 2"),
	PREHISTORIC_3 + " Checkpoint 3" : 	ItemData(BASE_ID + 170, 1, "Progression", PREHISTORIC_3 + ": Checkpoint 3"),
	PREHISTORIC_3 + " Checkpoint 4" : 	ItemData(BASE_ID + 171, 1, "Progression", PREHISTORIC_3 + ": Checkpoint 4"),
	FEAR_1 + " Checkpoint 1" : 			ItemData(BASE_ID + 172, 1, "Progression", FEAR_1 + ": Checkpoint 1"),
	FEAR_1 + " Checkpoint 2" : 			ItemData(BASE_ID + 173, 1, "Progression", FEAR_1 + ": Checkpoint 2"),
	FEAR_1 + " Checkpoint 3" : 			ItemData(BASE_ID + 174, 1, "Progression", FEAR_1 + ": Checkpoint 3"),
	FEAR_2 + " Checkpoint 1" : 			ItemData(BASE_ID + 175, 1, "Progression", FEAR_2 + ": Checkpoint 1"),
	FEAR_2 + " Checkpoint 2" : 			ItemData(BASE_ID + 176, 1, "Progression", FEAR_2 + ": Checkpoint 2"),
	FEAR_2 + " Checkpoint 3" : 			ItemData(BASE_ID + 177, 1, "Progression", FEAR_2 + ": Checkpoint 3"),
	FEAR_3 + " Checkpoint 1" : 			ItemData(BASE_ID + 178, 1, "Progression", FEAR_3 + ": Checkpoint 1"),
	FEAR_3 + " Checkpoint 2" : 			ItemData(BASE_ID + 179, 1, "Progression", FEAR_3 + ": Checkpoint 2"),
	FEAR_3 + " Checkpoint 3" : 			ItemData(BASE_ID + 180, 1, "Progression", FEAR_3 + ": Checkpoint 3"),
	FEAR_3 + " Checkpoint 4" : 			ItemData(BASE_ID + 181, 1, "Progression", FEAR_3 + ": Checkpoint 4"),
	FEAR_3 + " Checkpoint 5" : 			ItemData(BASE_ID + 182, 1, "Progression", FEAR_3 + ": Checkpoint 5"),
	SPACE_1 + " Checkpoint 1" : 		ItemData(BASE_ID + 183, 1, "Progression", SPACE_1 + ": Checkpoint 1"),
	SPACE_1 + " Checkpoint 2" : 		ItemData(BASE_ID + 184, 1, "Progression", SPACE_1 + ": Checkpoint 2"),
	SPACE_2 + " Checkpoint 1" : 		ItemData(BASE_ID + 185, 1, "Progression", SPACE_2 + ": Checkpoint 1"),
	SPACE_3 + " Checkpoint 1" : 		ItemData(BASE_ID + 186, 1, "Progression", SPACE_3 + ": Checkpoint 1"),
	SPACE_3 + " Checkpoint 2" : 		ItemData(BASE_ID + 187, 1, "Progression", SPACE_3 + ": Checkpoint 2"),
	SPACE_3 + " Checkpoint 3" : 		ItemData(BASE_ID + 188, 1, "Progression", SPACE_3 + ": Checkpoint 3"),
	SPACE_3 + " Checkpoint 4" : 		ItemData(BASE_ID + 189, 1, "Progression", SPACE_3 + ": Checkpoint 4")
	}

world_garib_table = {
	ATLANTIS_1 + " 1 Garib" : 			ItemData(BASE_ID + 30101, 1, "Garib", None),
	ATLANTIS_1 + " 2 Garibs" : 			ItemData(BASE_ID + 30102, 3, "Garib", None),
	ATLANTIS_1 + " 3 Garibs" : 			ItemData(BASE_ID + 30103, 1, "Garib", None),
	ATLANTIS_1 + " 4 Garibs" : 			ItemData(BASE_ID + 30104, 5, "Garib", None),
	ATLANTIS_1 + " 5 Garibs" : 			ItemData(BASE_ID + 30105, 1, "Garib", None),
	ATLANTIS_1 + " 6 Garibs" : 			ItemData(BASE_ID + 30106, 1, "Garib", None),
	ATLANTIS_1 + " 9 Garibs" : 			ItemData(BASE_ID + 30109, 1, "Garib", None),
	ATLANTIS_2 + " 1 Garib" : 			ItemData(BASE_ID + 30201, 1, "Garib", None),
	ATLANTIS_2 + " 2 Garibs" : 			ItemData(BASE_ID + 30202, 2, "Garib", None),
	ATLANTIS_2 + " 3 Garibs" : 			ItemData(BASE_ID + 30203, 3, "Garib", None),
	ATLANTIS_2 + " 4 Garibs" : 			ItemData(BASE_ID + 30204, 1, "Garib", None),
	ATLANTIS_2 + " 5 Garibs" : 			ItemData(BASE_ID + 30205, 5, "Garib", None),
	ATLANTIS_2 + " 7 Garibs" : 			ItemData(BASE_ID + 30207, 1, "Garib", None),
	ATLANTIS_2 + " 10 Garibs" : 		ItemData(BASE_ID + 30210, 1, "Garib", None),
	ATLANTIS_3 + " 1 Garib" : 			ItemData(BASE_ID + 30301, 2, "Garib", None),
	ATLANTIS_3 + " 2 Garibs" : 			ItemData(BASE_ID + 30302, 1, "Garib", None),
	ATLANTIS_3 + " 3 Garibs" : 			ItemData(BASE_ID + 30303, 2, "Garib", None),
	ATLANTIS_3 + " 4 Garibs" : 			ItemData(BASE_ID + 30304, 4, "Garib", None),
	ATLANTIS_3 + " 5 Garibs" : 			ItemData(BASE_ID + 30305, 3, "Garib", None),
	ATLANTIS_3 + " 6 Garibs" : 			ItemData(BASE_ID + 30306, 1, "Garib", None),
	ATLANTIS_3 + " 8 Garibs" : 			ItemData(BASE_ID + 30308, 3, "Garib", None),
	ATLANTIS_3 + " 9 Garibs" : 			ItemData(BASE_ID + 30309, 1, "Garib", None),
	ATLANTIS_BONUS + " 5 Garibs" : 		ItemData(BASE_ID + 30505, 5, "Garib", None),
	CARNIVAL_1 + " 1 Garib" : 			ItemData(BASE_ID + 31101, 1, "Garib", None),
	CARNIVAL_1 + " 4 Garibs" : 			ItemData(BASE_ID + 31104, 3, "Garib", None),
	CARNIVAL_1 + " 7 Garibs" : 			ItemData(BASE_ID + 31107, 1, "Garib", None),
	CARNIVAL_1 + " 8 Garibs" : 			ItemData(BASE_ID + 31108, 3, "Garib", None),
	CARNIVAL_1 + " 10 Garibs" : 		ItemData(BASE_ID + 31110, 1, "Garib", None),
	CARNIVAL_1 + " 11 Garibs" : 		ItemData(BASE_ID + 31111, 1, "Garib", None),
	CARNIVAL_2 + " 1 Garib" : 			ItemData(BASE_ID + 31201, 3, "Garib", None),
	CARNIVAL_2 + " 2 Garibs" : 			ItemData(BASE_ID + 31202, 1, "Garib", None),
	CARNIVAL_2 + " 3 Garibs" : 			ItemData(BASE_ID + 31203, 1, "Garib", None),
	CARNIVAL_2 + " 4 Garibs" : 			ItemData(BASE_ID + 31204, 4, "Garib", None),
	CARNIVAL_2 + " 6 Garibs" : 			ItemData(BASE_ID + 31206, 3, "Garib", None),
	CARNIVAL_2 + " 8 Garibs" : 			ItemData(BASE_ID + 31208, 2, "Garib", None),
	CARNIVAL_2 + " 10 Garibs" : 		ItemData(BASE_ID + 31210, 1, "Garib", None),
	CARNIVAL_2 + " 12 Garibs" : 		ItemData(BASE_ID + 31212, 1, "Garib", None),
	CARNIVAL_3 + " 1 Garib" : 			ItemData(BASE_ID + 31301, 1, "Garib", None),
	CARNIVAL_3 + " 2 Garibs" : 			ItemData(BASE_ID + 31302, 1, "Garib", None),
	CARNIVAL_3 + " 3 Garibs" : 			ItemData(BASE_ID + 31303, 6, "Garib", None),
	CARNIVAL_3 + " 4 Garibs" : 			ItemData(BASE_ID + 31304, 6, "Garib", None),
	CARNIVAL_3 + " 6 Garibs" : 			ItemData(BASE_ID + 31306, 1, "Garib", None),
	CARNIVAL_3 + " 8 Garibs" : 			ItemData(BASE_ID + 31308, 1, "Garib", None),
	CARNIVAL_3 + " 9 Garibs" : 			ItemData(BASE_ID + 31309, 1, "Garib", None),
	CARNIVAL_3 + " 12 Garibs" : 		ItemData(BASE_ID + 31312, 1, "Garib", None),
	CARNIVAL_BONUS + " 8 Garibs" : 		ItemData(BASE_ID + 31508, 1, "Garib", None),
	CARNIVAL_BONUS + " 12 Garibs" : 	ItemData(BASE_ID + 31512, 1, "Garib", None),
	PIRATES_1 + " 1 Garib" : 			ItemData(BASE_ID + 32101, 4, "Garib", None),
	PIRATES_1 + " 4 Garibs" : 			ItemData(BASE_ID + 32104, 7, "Garib", None),
	PIRATES_1 + " 5 Garibs" : 			ItemData(BASE_ID + 32105, 1, "Garib", None),
	PIRATES_1 + " 6 Garibs" : 			ItemData(BASE_ID + 32106, 3, "Garib", None),
	PIRATES_1 + " 7 Garibs" : 			ItemData(BASE_ID + 32107, 1, "Garib", None),
	PIRATES_1 + " 8 Garibs" : 			ItemData(BASE_ID + 32108, 1, "Garib", None),
	PIRATES_2 + " 1 Garib" : 			ItemData(BASE_ID + 32201, 6, "Garib", None),
	PIRATES_2 + " 2 Garibs" : 			ItemData(BASE_ID + 32202, 1, "Garib", None),
	PIRATES_2 + " 3 Garibs" : 			ItemData(BASE_ID + 32203, 1, "Garib", None),
	PIRATES_2 + " 4 Garibs" : 			ItemData(BASE_ID + 32204, 5, "Garib", None),
	PIRATES_2 + " 8 Garibs" : 			ItemData(BASE_ID + 32208, 1, "Garib", None),
	PIRATES_2 + " 9 Garibs" : 			ItemData(BASE_ID + 32209, 1, "Garib", None),
	PIRATES_2 + " 12 Garibs" : 			ItemData(BASE_ID + 32212, 1, "Garib", None),
	PIRATES_3 + " 1 Garib" : 			ItemData(BASE_ID + 32301, 3, "Garib", None),
	PIRATES_3 + " 2 Garibs" : 			ItemData(BASE_ID + 32302, 5, "Garib", None),
	PIRATES_3 + " 3 Garibs" : 			ItemData(BASE_ID + 32303, 3, "Garib", None),
	PIRATES_3 + " 4 Garibs" : 			ItemData(BASE_ID + 32304, 7, "Garib", None),
	PIRATES_3 + " 6 Garibs" : 			ItemData(BASE_ID + 32306, 1, "Garib", None),
	PIRATES_3 + " 8 Garibs" : 			ItemData(BASE_ID + 32308, 1, "Garib", None),
	PIRATES_3 + " 16 Garibs" : 			ItemData(BASE_ID + 32316, 1, "Garib", None),
	PIRATES_BONUS + " 3 Garibs" : 		ItemData(BASE_ID + 32503, 15, "Garib", None),
	PIRATES_BONUS + " 5 Garibs" : 		ItemData(BASE_ID + 32505, 1, "Garib", None),
	PREHISTORIC_1 + " 1 Garib" : 		ItemData(BASE_ID + 33101, 1, "Garib", None),
	PREHISTORIC_1 + " 2 Garibs" : 		ItemData(BASE_ID + 33102, 5, "Garib", None),
	PREHISTORIC_1 + " 3 Garibs" : 		ItemData(BASE_ID + 33103, 6, "Garib", None),
	PREHISTORIC_1 + " 4 Garibs" : 		ItemData(BASE_ID + 33104, 1, "Garib", None),
	PREHISTORIC_1 + " 5 Garibs" : 		ItemData(BASE_ID + 33105, 1, "Garib", None),
	PREHISTORIC_1 + " 6 Garibs" : 		ItemData(BASE_ID + 33106, 1, "Garib", None),
	PREHISTORIC_1 + " 8 Garibs" : 		ItemData(BASE_ID + 33108, 3, "Garib", None),
	PREHISTORIC_1 + " 12 Garibs" : 		ItemData(BASE_ID + 33112, 1, "Garib", None),
	PREHISTORIC_2 + " 1 Garib" : 		ItemData(BASE_ID + 33201, 6, "Garib", None),
	PREHISTORIC_2 + " 2 Garibs" : 		ItemData(BASE_ID + 33202, 1, "Garib", None),
	PREHISTORIC_2 + " 3 Garibs" : 		ItemData(BASE_ID + 33203, 3, "Garib", None),
	PREHISTORIC_2 + " 4 Garibs" : 		ItemData(BASE_ID + 33204, 6, "Garib", None),
	PREHISTORIC_2 + " 5 Garibs" : 		ItemData(BASE_ID + 33205, 4, "Garib", None),
	PREHISTORIC_2 + " 8 Garibs" : 		ItemData(BASE_ID + 33208, 1, "Garib", None),
	PREHISTORIC_2 + " 11 Garibs" : 		ItemData(BASE_ID + 33211, 1, "Garib", None),
	PREHISTORIC_3 + " 1 Garib" : 		ItemData(BASE_ID + 33301, 1, "Garib", None),
	PREHISTORIC_3 + " 2 Garibs" : 		ItemData(BASE_ID + 33302, 2, "Garib", None),
	PREHISTORIC_3 + " 3 Garibs" : 		ItemData(BASE_ID + 33303, 2, "Garib", None),
	PREHISTORIC_3 + " 5 Garibs" : 		ItemData(BASE_ID + 33305, 1, "Garib", None),
	PREHISTORIC_3 + " 7 Garibs" : 		ItemData(BASE_ID + 33307, 1, "Garib", None),
	PREHISTORIC_3 + " 8 Garibs" : 		ItemData(BASE_ID + 33308, 2, "Garib", None),
	PREHISTORIC_3 + " 10 Garibs" : 		ItemData(BASE_ID + 33310, 1, "Garib", None),
	PREHISTORIC_3 + " 15 Garibs" : 		ItemData(BASE_ID + 33315, 1, "Garib", None),
	PREHISTORIC_3 + " 16 Garibs" : 		ItemData(BASE_ID + 33316, 1, "Garib", None),
	PREHISTORIC_BONUS + " 10 Garibs" : 	ItemData(BASE_ID + 33510, 6, "Garib", None),
	FEAR_1 + " 1 Garib" : 				ItemData(BASE_ID + 34101, 4, "Garib", None),
	FEAR_1 + " 2 Garibs" : 				ItemData(BASE_ID + 34102, 1, "Garib", None),
	FEAR_1 + " 3 Garibs" : 				ItemData(BASE_ID + 34103, 4, "Garib", None),
	FEAR_1 + " 4 Garibs" : 				ItemData(BASE_ID + 34104, 3, "Garib", None),
	FEAR_1 + " 5 Garibs" : 				ItemData(BASE_ID + 34105, 2, "Garib", None),
	FEAR_1 + " 6 Garibs" : 				ItemData(BASE_ID + 34106, 2, "Garib", None),
	FEAR_1 + " 8 Garibs" : 				ItemData(BASE_ID + 34108, 1, "Garib", None),
	FEAR_2 + " 1 Garib" : 				ItemData(BASE_ID + 34201, 1, "Garib", None),
	FEAR_2 + " 2 Garibs" : 				ItemData(BASE_ID + 34202, 1, "Garib", None),
	FEAR_2 + " 3 Garibs" : 				ItemData(BASE_ID + 34203, 3, "Garib", None),
	FEAR_2 + " 5 Garibs" : 				ItemData(BASE_ID + 34205, 5, "Garib", None),
	FEAR_2 + " 6 Garibs" : 				ItemData(BASE_ID + 34206, 1, "Garib", None),
	FEAR_2 + " 7 Garibs" : 				ItemData(BASE_ID + 34207, 1, "Garib", None),
	FEAR_2 + " 10 Garibs" : 			ItemData(BASE_ID + 34210, 1, "Garib", None),
	FEAR_3 + " 1 Garib" : 				ItemData(BASE_ID + 34301, 1, "Garib", None),
	FEAR_3 + " 2 Garibs" : 				ItemData(BASE_ID + 34302, 4, "Garib", None),
	FEAR_3 + " 3 Garibs" : 				ItemData(BASE_ID + 34303, 4, "Garib", None),
	FEAR_3 + " 4 Garibs" : 				ItemData(BASE_ID + 34304, 3, "Garib", None),
	FEAR_3 + " 5 Garibs" : 				ItemData(BASE_ID + 34305, 1, "Garib", None),
	FEAR_3 + " 6 Garibs" : 				ItemData(BASE_ID + 34306, 1, "Garib", None),
	FEAR_3 + " 8 Garibs" : 				ItemData(BASE_ID + 34308, 2, "Garib", None),
	FEAR_3 + " 10 Garibs" : 			ItemData(BASE_ID + 34310, 1, "Garib", None),
	FEAR_BONUS + " 4 Garibs" : 			ItemData(BASE_ID + 34504, 2, "Garib", None),
	FEAR_BONUS + " 5 Garibs" : 			ItemData(BASE_ID + 34505, 4, "Garib", None),
	FEAR_BONUS + " 7 Garibs" : 			ItemData(BASE_ID + 34507, 4, "Garib", None),
	SPACE_1 + " 1 Garib" : 				ItemData(BASE_ID + 35101, 6, "Garib", None),
	SPACE_1 + " 2 Garibs" : 			ItemData(BASE_ID + 35102, 1, "Garib", None),
	SPACE_1 + " 3 Garibs" : 			ItemData(BASE_ID + 35103, 4, "Garib", None),
	SPACE_1 + " 4 Garibs" : 			ItemData(BASE_ID + 35104, 1, "Garib", None),
	SPACE_1 + " 10 Garibs" : 			ItemData(BASE_ID + 35110, 1, "Garib", None),
	SPACE_1 + " 16 Garibs" : 			ItemData(BASE_ID + 35116, 1, "Garib", None),
	SPACE_2 + " 2 Garibs" : 			ItemData(BASE_ID + 35202, 2, "Garib", None),
	SPACE_2 + " 3 Garibs" : 			ItemData(BASE_ID + 35203, 2, "Garib", None),
	SPACE_2 + " 4 Garibs" : 			ItemData(BASE_ID + 35204, 3, "Garib", None),
	SPACE_2 + " 5 Garibs" : 			ItemData(BASE_ID + 35205, 2, "Garib", None),
	SPACE_2 + " 6 Garibs" : 			ItemData(BASE_ID + 35206, 1, "Garib", None),
	SPACE_2 + " 12 Garibs" : 			ItemData(BASE_ID + 35212, 1, "Garib", None),
	SPACE_3 + " 3 Garibs" : 			ItemData(BASE_ID + 35303, 1, "Garib", None),
	SPACE_3 + " 4 Garibs" : 			ItemData(BASE_ID + 35304, 3, "Garib", None),
	SPACE_3 + " 5 Garibs" : 			ItemData(BASE_ID + 35305, 2, "Garib", None),
	SPACE_3 + " 6 Garibs" : 			ItemData(BASE_ID + 35306, 2, "Garib", None),
	SPACE_3 + " 7 Garibs" : 			ItemData(BASE_ID + 35307, 2, "Garib", None),
	SPACE_3 + " 8 Garibs" : 			ItemData(BASE_ID + 35308, 1, "Garib", None),
	SPACE_3 + " 9 Garibs" : 			ItemData(BASE_ID + 35309, 1, "Garib", None),
	SPACE_3 + " 12 Garibs" : 			ItemData(BASE_ID + 35312, 1, "Garib", None),
	SPACE_BONUS + " 6 Garibs" : 		ItemData(BASE_ID + 35506, 3, "Garib", None),
	SPACE_BONUS + " 8 Garibs" : 		ItemData(BASE_ID + 35508, 4, "Garib", None)
	}

def construct_blank_world_garibs():
	output_table : dict[str, ItemData] = {}
	levels_with_garibs = []

	#World/Level prefix constructor
	for world_prefix in WORLD_PREFIXES:
		for level_prefix in LEVEL_PREFIXES:
			if level_prefix != "H" and level_prefix != "!":
				levels_with_garibs.append(world_prefix + level_prefix)

	#Go over all the garibs
	for garib_level in levels_with_garibs:
		for garib_count in range(1, 17):
			#Get the text prefix for all garib counts
			garib_suffix : str = " 1 Garib"
			if garib_count > 1:
				garib_suffix : str = " " + str(garib_count) + " Garibs"
			#If a level doesn't have that count of garibs
			if not (garib_level + garib_suffix in world_garib_table.keys()):
				world_offset = 1000 * WORLD_PREFIXES.index(garib_level[:3])
				level_offset = 100 * LEVEL_PREFIXES.index(garib_level[3:4])
				item_id = BASE_ID + 30000 + world_offset + level_offset + garib_count
				output_table[garib_level + garib_suffix] = ItemData(item_id, 0, "Filler", None)
	return output_table

move_table = {
	"Jump" : 									ItemData(BASE_ID + 329, 1, "Proguseful", None),
	"Fist Slam" : 								ItemData(BASE_ID + 333, 1, "Proguseful", None),
	"Dribble" : 								ItemData(BASE_ID + 338, 1, "Proguseful", None),
	"Power Ball" : 								ItemData(BASE_ID + 356, 1, "Proguseful", None),
	"Rubber Ball" : 							ItemData(BASE_ID + 352, 1, "Proguseful", None),
	"Ball Bearing" : 							ItemData(BASE_ID + 354, 1, "Proguseful", None),
	"Bowling Ball" : 							ItemData(BASE_ID + 353, 1, "Proguseful", None),
	"Crystal" : 								ItemData(BASE_ID + 355, 1, "Proguseful", None),
	"Slap" : 									ItemData(BASE_ID + 340, 1, "Proguseful", None),
	"Throw" : 									ItemData(BASE_ID + 341, 1, "Proguseful", None),
	"Ball Toss" : 								ItemData(BASE_ID + 342, 1, "Proguseful", None),
	"Double Jump" : 							ItemData(BASE_ID + 332, 1, "Progression", None),
	"Ledge Grab" : 								ItemData(BASE_ID + 334, 1, "Progression", None),
	"Cartwheel" : 								ItemData(BASE_ID + 330, 1, "Progression", None),
	"Crawl" : 									ItemData(BASE_ID + 331, 1, "Progression", None),
	"Push" : 									ItemData(BASE_ID + 335, 1, "Progression", None),
	"Grab" : 									ItemData(BASE_ID + 351, 1, "Progression", None),
	"Quick Swap" : 								ItemData(BASE_ID + 339, 1, "Progression", None),
	"Locate Ball" : 							ItemData(BASE_ID + 337, 1, "Progression", None),
	"Locate Garibs" : 							ItemData(BASE_ID + 336, 1, "Useful", None),
}
potion_table = {
	"Helicopter Potion" : 						ItemData(BASE_ID + 345, 1, "Progression", None),
	"Sticky Potion" : 							ItemData(BASE_ID + 349, 1, "Progression", None),
	"Beachball Potion" : 						ItemData(BASE_ID + 343, 1, "Progression", None),
	"Boomerang Ball Potion" : 					ItemData(BASE_ID + 347, 1, "Progression", None),
	"Frog Potion" : 							ItemData(BASE_ID + 346, 1, "Progression", None),
	"Speed Potion" : 							ItemData(BASE_ID + 348, 1, "Progression", None),
	"Hercules Potion" : 						ItemData(BASE_ID + 350, 1, "Progression", None),
	"Death Potion" : 							ItemData(BASE_ID + 344, 1, "Progression", None)
	}

filler_table = {
	"Extra Garibs" : 							ItemData(BASE_ID + 357, -1, "Useful", None),
	"Chicken Sound" : 							ItemData(BASE_ID + 358, -1, "Filler", None),
	"Life" : 									ItemData(BASE_ID + 359, -1, "Filler", None),
	"Boomerang Spell" : 						ItemData(BASE_ID + 360, -1, "Filler", None),
	"Beachball Spell" : 						ItemData(BASE_ID + 361, -1, "Filler", None),
	"Hercules Spell" : 							ItemData(BASE_ID + 362, -1, "Filler", None),
	"Helicopter Spell" : 						ItemData(BASE_ID + 363, -1, "Filler", None),
	"Speed Spell" : 							ItemData(BASE_ID + 364, -1, "Filler", None),
	"Frog Spell" : 								ItemData(BASE_ID + 365, -1, "Filler", None),
	"Death Spell" : 							ItemData(BASE_ID + 366, -1, "Filler", None),
	"Sticky Spell" : 							ItemData(BASE_ID + 367, -1, "Filler", None),
	"Big Ball" : 								ItemData(BASE_ID + 368, -1, "Filler", None),
	"Low Gravity" : 							ItemData(BASE_ID + 369, -1, "Filler", None)
	}

trap_table = {
	"Frog Trap" : 								ItemData(BASE_ID + 370, -1, "Trap", None),
	"Cursed Ball Trap" :						ItemData(BASE_ID + 371, -1, "Trap", None),
	"Instant Crystal Trap" :					ItemData(BASE_ID + 372, -1, "Trap", None),
	"Camera Rotate Trap" :						ItemData(BASE_ID + 373, -1, "Trap", None),
	"Tip Trap" :								ItemData(BASE_ID + 374, -1, "Trap", None),
	"Fish Eye Trap" :	 						ItemData(BASE_ID + 375, -1, "Trap", None),
	"Enemy Ball Trap" :	 						ItemData(BASE_ID + 376, -1, "Trap", None),
	"Control Ball Trap" :						ItemData(BASE_ID + 377, -1, "Trap", None),
	"Invisiball Trap" : 						ItemData(BASE_ID + 378, -1, "Trap", None)
	}

garibsanity_world_table = {
	ATLANTIS_1 + " Garib" : 		ItemData(BASE_ID + 20001, 50, "Garib", None),
	ATLANTIS_2 + " Garib" : 		ItemData(BASE_ID + 20002, 60, "Garib", None),
	ATLANTIS_3 + " Garib" : 		ItemData(BASE_ID + 20003, 80, "Garib", None),
	ATLANTIS_BONUS + " Garib" :	 	ItemData(BASE_ID + 20005, 25, "Garib", None),
	CARNIVAL_1 + " Garib" : 		ItemData(BASE_ID + 20011, 65, "Garib", None),
	CARNIVAL_2 + " Garib" : 		ItemData(BASE_ID + 20012, 80, "Garib", None),
	CARNIVAL_3 + " Garib" : 		ItemData(BASE_ID + 20013, 80, "Garib", None),
	CARNIVAL_BONUS + " Garib" : 	ItemData(BASE_ID + 20015, 20, "Garib", None),
	PIRATES_1 + " Garib" : 			ItemData(BASE_ID + 20021, 70, "Garib", None),
	PIRATES_2 + " Garib" : 			ItemData(BASE_ID + 20022, 60, "Garib", None),
	PIRATES_3 + " Garib" : 			ItemData(BASE_ID + 20023, 80, "Garib", None),
	PIRATES_BONUS + " Garib" : 		ItemData(BASE_ID + 20025, 50, "Garib", None),
	PREHISTORIC_1 + " Garib" : 		ItemData(BASE_ID + 20031, 80, "Garib", None),
	PREHISTORIC_2 + " Garib" : 		ItemData(BASE_ID + 20032, 80, "Garib", None),
	PREHISTORIC_3 + " Garib" : 		ItemData(BASE_ID + 20033, 80, "Garib", None),
	PREHISTORIC_BONUS + " Garib" : 	ItemData(BASE_ID + 20035, 60, "Garib", None),
	FEAR_1 + " Garib" : 			ItemData(BASE_ID + 20041, 60, "Garib", None),
	FEAR_2 + " Garib" : 			ItemData(BASE_ID + 20042, 60, "Garib", None),
	FEAR_3 + " Garib" : 			ItemData(BASE_ID + 20043, 70, "Garib", None),
	FEAR_BONUS + " Garib" : 		ItemData(BASE_ID + 20045, 56, "Garib", None),
	SPACE_1 + " Garib" : 			ItemData(BASE_ID + 20051, 50, "Garib", None),
	SPACE_2 + " Garib" : 			ItemData(BASE_ID + 20052, 50, "Garib", None),
	SPACE_3 + " Garib" : 			ItemData(BASE_ID + 20053, 80, "Garib", None),
	SPACE_BONUS + " Garib" : 		ItemData(BASE_ID + 20055, 50, "Garib", None)
	}

garbinsanity = ItemData(BASE_ID + 10001, 1496, "Garib", None)

decoupled_garib_table = {
	"Garib" : 		ItemData(BASE_ID + 10001, 42, "Garib", None),
	"2 Garibs" : 	ItemData(BASE_ID + 10002, 31, "Garib", None),
	"3 Garibs" : 	ItemData(BASE_ID + 10003, 61, "Garib", None),
	"4 Garibs" : 	ItemData(BASE_ID + 10004, 64, "Garib", None),
	"5 Garibs" : 	ItemData(BASE_ID + 10005, 38, "Garib", None),
	"6 Garibs" : 	ItemData(BASE_ID + 10006, 21, "Garib", None),
	"7 Garibs" : 	ItemData(BASE_ID + 10007, 11, "Garib", None),
	"8 Garibs" : 	ItemData(BASE_ID + 10008, 27, "Garib", None),
	"9 Garibs" : 	ItemData(BASE_ID + 10009, 5, "Garib", None),
	"10 Garibs" : 	ItemData(BASE_ID + 10010, 13, "Garib", None),
	"11 Garibs" : 	ItemData(BASE_ID + 10011, 2, "Garib", None),
	"12 Garibs" : 	ItemData(BASE_ID + 10012, 7, "Garib", None),
	"13 Garibs" : 	ItemData(BASE_ID + 10013, 0, "Garib", None),
	"14 Garibs" : 	ItemData(BASE_ID + 10014, 0, "Garib", None),
	"15 Garibs" : 	ItemData(BASE_ID + 10015, 1, "Garib", None),
	"16 Garibs" : 	ItemData(BASE_ID + 10016, 3, "Garib", None)
} 

decoupled_garib_bonus_count = {
	"3 Garibs" : 		15,
	"4 Garibs" : 		2,
	"5 Garibs" : 		10,
	"7 Garibs" : 		4,
	"8 Garibs" :		1,
	"10 Garibs" :		6,
	"12 Garibs" :		1#,
}

garbinsanity_bonus_count = 261


all_items = {
	**portalsanity_table,
	**level_event_table, 
	**checkpoint_table, 
	**move_table, 
	**potion_table, 
	**filler_table, 
	**trap_table, 
	**world_garib_table, 
	**garibsanity_world_table,
	**{"Garib" : garbinsanity},
	**decoupled_garib_table,
	**misc_table
}

def generate_item_name_to_id() -> dict:
	output : dict = {}
	all_items.update(construct_blank_world_garibs())
	for name, data in all_items.items():
		output[name] = data.glid
	return output

def generate_item_name_groups() -> dict:
	output : dict = {
		"Level Events" :				level_event_table.keys(),
		"Checkpoints" :					checkpoint_table.keys(),
		"Not Crystal" :					["Rubber Ball", "Bowling Ball", "Ball Bearing", "Power Ball"],
		"Not Bowling" :					["Rubber Ball", "Ball Bearing", "Crystal", "Power Ball"],
		"Not Bowling or Crystal" :		["Rubber Ball", "Ball Bearing", "Power Ball"],
		"Sinks" :						["Bowling Ball", "Ball Bearing"],
		"Floats" :						["Rubber Ball", "Crystal", "Power Ball"],
		"Ball Up" :						["Throw", "Dribble", "Ball Toss"],
		"Balls" :						["Rubber Ball", "Bowling Ball", "Ball Bearing", "Crystal", "Power Ball"],
		"Potions" :						potion_table.keys(),
		"Garibs" :						list(garibsanity_world_table.keys())+list(decoupled_garib_table.keys())+list(world_garib_table.keys()),
		"Moves" :						move_table.keys(),
		"Spells" : 						["Boomerang Spell", "Beachball Spell", "Hercules Spell", "Helicopter Spell", "Speed Spell", "Frog Spell", "Death Spell", "Sticky Spell"]
	}
	return output

def convert_extra_garibs(self) -> ItemData:
	#Get the garib count
	extra_garibs_value : int = self.options.extra_garibs_value.value
	if self.options.garib_sorting != GaribSorting.option_by_level:
		#"Garibs" or "Garib"?
		garib_name = " Garibs"
		if extra_garibs_value == 1:
			return decoupled_garib_table["Garib"]
		#Index to name
		return decoupled_garib_table[str(extra_garibs_value) + garib_name]
	#Level Garib Groups
	else:
		#"Garibs" or "Garib"?
		garib_name = " Garibs"
		if extra_garibs_value == 1:
			garib_name = " Garib"
		#Pick the next valid garib level
		level_name = self.next_garib_level()
		return world_garib_table[level_name + " " + str(extra_garibs_value) + garib_name]