import zelda_functions as utl
from app import app

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
    def __init__(self, name, type, children=None):
        self.name = name
        self.type = type
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



def main():
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
