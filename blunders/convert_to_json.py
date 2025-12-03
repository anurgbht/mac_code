import json
import string
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).parent

gender_color_map = {"M": 1, "F": 5, "X": 3}


def add_a_to_consonant_ending(name_string):
    """Adds "a" to the end of a string if the last letter is a consonant.

    Args:
      name_string: The string to be checked.

    Returns:
      The string with "a" added to the end if the last letter is a consonant, or the
      original string if the last letter is a vowel.
    """

    # Get the last letter of the string.
    last_letter = name_string[-1]

    # Check if the last letter is a consonant.
    if not last_letter.isalpha():
        return name_string

    consonants = set("bcdfghjklmnpqrstvwxyz0123456789")
    if last_letter in consonants:
        return name_string + "a"
    else:
        return name_string


def remove_whitespace_and_special_characters(name_string: str):
    """Removes all white spaces and special characters from the beginning and end of a string.

    Args:
      name_string: The string to be cleaned.

    Returns:
      The cleaned string.
    """

    # Remove all leading and trailing whitespace.
    name_string = name_string.strip()

    # Remove all special characters.
    special_characters = set(string.punctuation)
    name_string = "".join(ch for ch in name_string if ch not in special_characters)

    return name_string


def process_data_field(
    node_list: list,
    link_list: list,
    character_list: list,
    character_name: str,
    field_names: str,
    group_value: int,
    known_gender: str,
    relation_dict_gender_check: dict,
):
    """Processes a data field and adds it to the node list, link list, and character list.

    Args:
        node_list: The list of nodes.
        link_list: The list of links.
        character_list: The list of characters.
        character_name: The name of the character.
        field_names: The names of the fields.
        group_value: The group value.

    Returns:
        The updated node list, link list, and character list.
    """

    for field_name in field_names.split(","):
        field_name = standard_name(field_name)
        if known_gender in ["M", "F"]:
            gender_value = gender_color_map[known_gender]
        else:
            try:
                ## find field gender
                gender_value = gender_color_map[
                    relation_dict_gender_check[field_name]["Gender"]
                ]
            except Exception as e:
                gender_value = gender_color_map["X"]

        # Check if the field name is already in the character list.
        if field_name not in character_list and field_name != "nana":
            # Add the field name to the character list.
            character_list.append(field_name)

            # Create a node for the field name.
            temp_node = {"id": field_name, "group": gender_value}
            node_list.append(temp_node)

        # Check if the field name is not equal to nan.
        if field_name != "nana":
            # Create a link for the field name.
            if group_value == 3:
                temp_link = {
                    "source": character_name,
                    "target": field_name,
                    "value": gender_value,
                }
            else:
                temp_link = {
                    "source": field_name,
                    "target": character_name,
                    "value": gender_value,
                }
            link_list.append(temp_link)

    return node_list, link_list, character_list


def standard_name(name_str):
    return add_a_to_consonant_ending(remove_whitespace_and_special_characters(name_str))


if __name__ == "__main__":
    excel_path = Path(ROOT_DIR, "Character Map.xlsx")

    character_df = pd.read_excel(excel_path, index_col=0)
    character_df.index = character_df.index.map(standard_name)

    character_dict = character_df.T.to_dict()

    character_dict_path = Path(ROOT_DIR, "Character Dict.json")
    with open(character_dict_path, "w") as file:
        json.dump(character_dict, file, indent=4)

    node_list = {"nan": {"key": -99, "s": "M"}}
    character_list = []

    # key, the unique ID of the person
    # n, the person's name
    # s, the person's sex
    # m, the person's mother's key
    # f, the person's father's key
    # ux, the person's wife
    # vir, the person's husband
    # a, an Array of the attributes or markers that the person has

    count = 0
    for character_name, relation_dict in character_dict.items():
        if character_name not in character_list:
            count += 1
            character_list.append(character_name)
            if relation_dict["Gender"] == "M":
                temp_node = {
                    character_name: {
                        "key": count,
                        "s": relation_dict["Gender"],
                        "m": relation_dict["Mother"],
                        "f": relation_dict["Father"],
                        "ux": relation_dict["Spouse"],
                    }
                }
            else:
                temp_node = {
                    character_name: {
                        "key": count,
                        "s": relation_dict["Gender"],
                        "m": relation_dict["Mother"],
                        "f": relation_dict["Father"],
                        "vir": relation_dict["Spouse"],
                    }
                }
            node_list.update(temp_node)

    for character_name, relation_dict in character_dict.items():
        if str(relation_dict["Sons"]) != "nan":
            for son in str(relation_dict["Sons"]).split(","):
                son = son.strip()
                if son not in character_list:
                    count += 1
                    character_list.append(son)
                    temp_dict = {
                        son: {
                            "key": count,
                            "s": "M",
                            "m": relation_dict["Mother"],
                            "f": relation_dict["Father"],
                        }
                    }
                    node_list.update(temp_dict)

    for character_name, relation_dict in character_dict.items():
        if str(relation_dict["Daughters"]) != "nan":
            for dau in str(relation_dict["Daughters"]).split(","):
                dau = dau.strip()
                if dau not in character_list:
                    count += 1
                    character_list.append(dau)
                    temp_dict = {
                        dau: {
                            "key": count,
                            "s": "F",
                            "m": relation_dict["Mother"],
                            "f": relation_dict["Father"],
                        }
                    }
                    node_list.update(temp_dict)

    character_map_path = Path(ROOT_DIR, "Character Map.json")
    with open(character_map_path, "w") as file:
        json.dump(node_list, file, indent=4)

    node_index_list = []
    for character_name, relation_dict in node_list.items():
        try:
            if relation_dict["key"] > 0:
                if relation_dict["s"] == "M":
                    temp_node = {
                        "key": relation_dict["key"],
                        "n": character_name,
                        "s": relation_dict["s"],
                        "m": node_list[str(relation_dict["m"])]["key"],
                        "f": node_list[str(relation_dict["f"])]["key"],
                        "ux": node_list[str(relation_dict["ux"])]["key"],
                    }
                else:
                    temp_node = {
                        "key": relation_dict["key"],
                        "n": character_name,
                        "s": relation_dict["s"],
                        "m": node_list[str(relation_dict["m"])]["key"],
                        "f": node_list[str(relation_dict["f"])]["key"],
                        "vir": node_list[str(relation_dict["vir"])]["key"],
                    }
                node_index_list.append(temp_node)
        except Exception as e:
            # print(character_name, relation_dict)
            # print(e)
            # break
            pass

    character_map_path = Path(ROOT_DIR, "Character Map D3.json")
    with open(character_map_path, "w") as file:
        json.dump(node_index_list, file, indent=4)
