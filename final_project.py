import zelda_functions as utl
from app import app
import os
import json

CACHE_FILEPATH = './CACHE.json'
NONE_VALUES = ('', 'n/a', 'none', 'unknown')
HYRULE_ENDPOINT = 'https://botw-compendium.herokuapp.com/api/v3/compendium'
HYRULE_CATEGORIES = f"{HYRULE_ENDPOINT}/category/"
HYRULE_ENTRY = f"{HYRULE_ENDPOINT}/entry/"
HYRULE_ALL = f"{HYRULE_ENDPOINT}/all/"
HYRULE_IMAGE = f"{HYRULE_ENDPOINT}/entry/{{}}/image"

# Initialize or retrieve cache
cache = utl.create_cache(CACHE_FILEPATH)
# item_data = utl.fetch_item_details('moblin', cache, CACHE_FILEPATH)


class TreeNode:
    def __init__(self, name, type, data=None, children=None):
        self.name = name
        self.type = type
        self.data = data
        self.children = children or []

    def add_child(self, child_node):
        self.children.append(child_node)

def build_tree():
    root_nodes = {
        'Monsters': TreeNode('Monsters', 'Category'),
        'Equipment': TreeNode('Equipment', 'Category'),
        'Materials': TreeNode('Materials', 'Category'),
        'Creatures': TreeNode('Creatures', 'Category'),
        'Treasure': TreeNode('Treasure', 'Category')
    }

    # Add child nodes for Monsters
    monsters_data = utl.request_data(f"{HYRULE_CATEGORIES}monsters")
    if monsters_data and 'data' in monsters_data:
        for monster in monsters_data['data']:
            monster_node = TreeNode(monster['name'], 'Monster')
            root_nodes['Monsters'].add_child(monster_node)

    # Add child nodes for Equipment
    equipment_data = utl.request_data(f"{HYRULE_CATEGORIES}equipment")
    if equipment_data and 'data' in equipment_data:
        for equipment in equipment_data['data']:
            equipment_node = TreeNode(equipment['name'], 'Equipment')
            root_nodes['Equipment'].add_child(equipment_node)

    # Add child nodes for Materials
    materials_data = utl.request_data(f"{HYRULE_CATEGORIES}materials")
    if materials_data and 'data' in materials_data:
        for material in materials_data['data']:
            material_node = TreeNode(material['name'], 'Material')
            root_nodes['Materials'].add_child(material_node)

    # Add child nodes for Creatures
    creatures_data = utl.request_data(f"{HYRULE_CATEGORIES}creatures")
    if creatures_data and 'data' in creatures_data:
        for creature in creatures_data['data']:
            creature_node = TreeNode(creature['name'], 'Creature')
            root_nodes['Creatures'].add_child(creature_node)

    # Add child nodes for Treasure
    treasure_data = utl.request_data(f"{HYRULE_CATEGORIES}treasure")
    if treasure_data and 'data' in treasure_data:
        for treasure in treasure_data['data']:
            treasure_node = TreeNode(treasure['name'], 'Treasure')
            root_nodes['Treasure'].add_child(treasure_node)

    return root_nodes

def serialize_tree(node):
    node_dict = {'name': node.name, 'type': node.type, 'children': []}
    for child in node.children:
        node_dict['children'].append(serialize_tree(child))
    return node_dict

def read_tree_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    def construct_tree(node_data):
        node = TreeNode(node_data['name'], node_data['type'])
        for child_data in node_data.get('children', []):
            child_node = construct_tree(child_data)
            node.add_child(child_node)
        return node

    root_nodes = {}
    for key, value in data.items():
        root_nodes[key] = construct_tree(value)
    return root_nodes

def get_image_url(entry_name_or_id):
    """
    Generates the URL for an entry's image.

    Parameters:
        entry_name_or_id (str/int): The entry's name or ID.

    Returns:
        str: The URL for the entry's image.
    """
    return HYRULE_IMAGE.format(entry_name_or_id)

def fetch_and_display_creatures():
    """
    Fetches and displays creatures data from the API.
    """
    url = f"{HYRULE_CATEGORIES}creatures"
    creatures_data = utl.request_data(url)

    if creatures_data and 'data' in creatures_data:
        for creature in creatures_data['data']:
            print(creature['name'])

def process_entries(input_filepath, output_filepath):
    with open(input_filepath, 'r') as file:
        data = json.load(file)

    hearts_recovered_entries = {}
    for key, entry in data.items():
        if 'hearts_recovered' in entry:
            hearts_recovered_entries[key] = {
                'name': entry['name'],
                'common_locations': entry.get('common_locations', []),
                'hearts_recovered': entry['hearts_recovered'],
                'image': entry['image']
            }

    with open(output_filepath, 'w') as file:
        json.dump(hearts_recovered_entries, file, indent=4)



def main():

#Retrieve Tree
    json_filename = 'hyrule_tree.json'

    if not os.path.exists(json_filename):
        root_nodes = build_tree()
        tree_json = {name: serialize_tree(node) for name, node in root_nodes.items()}
        with open(json_filename, 'w') as file:
            json.dump(tree_json, file, indent=4)
        print(f"Created new tree JSON file: {json_filename}")
    else:
        print(f"Tree JSON file already exists: {json_filename}")

#Retrieve JSON
    filename = 'hyrule_retrieved.json'

    if not os.path.exists(filename):
        data = utl.fetch_data_until_invalid(1)
        utl.save_data_to_json(data, filename)
    else:
        print(f"'{filename}' already exists. Fetching data skipped.")

    input_filepath = 'hyrule_retrieved.json'
    output_filepath = 'hearts_recovered_entries.json'

# Process the entries
    process_entries(input_filepath, output_filepath)
    # fetch_and_display_creatures()

    # lynel_image_url = get_image_url("lynel")
    # print(f"Image URL for Lynel: {lynel_image_url}")

    # try:
    #     json_data = utl.read_json("path_to_your_json_file.json")
    #     # Process json_data as needed
    # except FileNotFoundError:
    #     print("JSON file not found. Please check the file path.")

    # Build the tree
    hyrule_tree = build_tree()



if __name__ == "__main__":
    main()
    app.run(debug=True)
