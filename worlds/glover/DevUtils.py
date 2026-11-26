import json

from LevelPrefixes import WORLD_PREFIXES, LEVEL_PREFIXES

# note: this is duplicated from Rules.py because importing it caused circular imports
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

def translate_method(method_data: dict[str, any], method_index: int, region_names: dict[int, str]) -> dict[str, any]:
    translated_method = {}
    if method_index == 0:
        for key, value in method_data.items():
            translated_method[key] = value
        translated_method["REGION"] = region_names[method_data["REGION"]]
    else:
        for key, value in method_data.items():
            if key == "regionIndex":
                translated_method["region"] = region_names[value]
            elif key.startswith("mv"):
                translated_method[key] = move_lookup[value]
            else:
                translated_method[key] = value
    return translated_method

def translate_indices_to_names(logic_data_to_translate) -> list[dict[str, any]]:
    translated_logic_data = []
    for world_index, world_data in enumerate(logic_data_to_translate):
        translated_world_data = {}
        for level_label, level_data in world_data.items():
            translated_level_data = {}
            region_names: dict[int, str] = {}
            # for the first pass, just get all region names
            for point_of_interest, point_data in level_data.items():
                if type(point_data) is dict:
                    # this is a region, save off the region name
                    region_names[point_data["I"]] = point_of_interest
            # for the second pass, translate move indices and region indices to names
            for point_of_interest, point_data in level_data.items():
                if type(point_data) is dict:
                    translated_ball_data = []
                    for method_index, method in enumerate(point_data["B"]):
                        translated_method = translate_method(method, method_index, region_names)
                        translated_ball_data.append(translated_method)
                    translated_no_ball_data = []
                    for method_index, method in enumerate(point_data["D"]):
                        translated_method = translate_method(method, method_index, region_names)
                        translated_no_ball_data.append(translated_method)
                    translated_region_data = {"B": translated_ball_data, "D": translated_no_ball_data, "I": point_data["I"]}
                    translated_level_data[point_of_interest] = translated_region_data
                elif type(point_data) is list:
                    translated_location_data = []
                    for method_index, method in enumerate(point_data):
                        translated_method = translate_method(method, method_index, region_names)
                        translated_location_data.append(translated_method)
                    translated_level_data[point_of_interest] = translated_location_data
            level_name: str = ""
            if world_index < 6:
                level_index = int(level_label[1])
                level_name = WORLD_PREFIXES[world_index] + LEVEL_PREFIXES[level_index]
            else:
                # special handling for hub world
                if level_label == "l0":
                    level_name = "Overworld"
                elif level_label == "l1":
                    level_name = "Crystal Turn-In"
                elif level_label == "l2":
                    level_name = "Training"
            translated_world_data[level_name] = translated_level_data
        translated_logic_data.append(translated_world_data)
    return translated_logic_data

if __name__ == "__main__":
    logic_data = {}
    with open("Logic.json", "r", encoding="utf-8") as fin:
        logic_data = json.loads(fin.read())
    translated_logic = translate_indices_to_names(logic_data)
    json_dump = json.dumps(translated_logic, indent=4)
    with open("TranslatedLogic.json", "wt", encoding="utf-8") as fout:
        fout.write(json_dump)