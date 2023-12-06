import csv
import json
import requests

from urllib.parse import quote, urlencode, urljoin

CACHE_FILEPATH = './cache.json'


NONE_VALUES = ('', 'n/a', 'none', 'unknown')
HYRULE_ENDPOINT = 'https://botw-compendium.herokuapp.com/api/v3/compendium'
HYRULE_CATEGORIES = f"{HYRULE_ENDPOINT}/category/"
HYRULE_ENTRY = f"{HYRULE_ENDPOINT}/entry/"
HYRULE_ALL = f"{HYRULE_ENDPOINT}/all/"
HYRULE_IMAGE = f"{HYRULE_ENDPOINT}/entry/{{}}/image"

def save_data_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def create_cache(filepath):
    """Attempts to retrieve cache contents written to the file system. If successful the
    cache contents from the previous script run are returned to the caller as the new
    cache. If unsuccessful an empty cache is returned to the caller.

    Parameters:
        filepath (str): path to the cache file

    Returns:
        dict: cache either empty or populated with resources from the previous script run
    """

    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}



def create_cache_key(url, params=None):
    """Returns a lowercase string key comprising the passed in < url >, and, if < params >
    is not None, the "?" separator, and any URL encoded querystring fields and values.
    Passes to the function < urllib.parse.urljoin > the optional < quote_via=quote >
    argument to override the default behavior and encode spaces with '%20' rather
    than "+".

    Example:
       url = https://swapi.py4e.com/api/people/
       params = {'search': 'Anakin Skywalker'}
       returns 'https://swapi.py4e.com/api/people/?search=anakin%20skywalker'

    Parameters:
        url (str): string representing a Uniform Resource Locator (URL)
        params (dict): one or more key-value pairs representing querystring fields and values

    Returns:
        str: Lowercase "key" comprising the URL and accompanying querystring fields and values
    """

    if params:
        return urljoin(url, f"?{urlencode(params, quote_via=quote)}").lower() # space replaced with '%20'
    else:
        return url.lower()

def convert_to_numeric(value):
    if value is None or isinstance(value, (int, float)):
        return value
    try:
        return float(value) if '.' in str(value) else int(value)
    except ValueError:
        return value

def request_data(url, params=None, timeout=30):
    """
    Makes a GET request to the specified URL with optional parameters and a timeout.

    Parameters:
        url (str): The URL to make the request to.
        params (dict): Optional dictionary of query string parameters.
        timeout (int): Timeout for the request in seconds.

    Returns:
        dict: The JSON response from the API converted into a Python dictionary.
    """

    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None

def get_nested_dict(data, key, filter):
    """Attempts to retrieve a nested dictionary in < data > using the passed in < filter >
    value. The passed in < key > name is used to identify the key-value pair to evaluate.
    The value mapped to the < key > is compared to the passed in < filter > value. Any
    object type can serve as the < filter >. If an exact match is obtained (i.e., test for
    equality) the nested dictionary is returned to the caller; otherwise None is returned.

    Parameters:
        data (list): List of nested dictionaries
        key (str): key that identifies the value that the < filter > must match
        filter (any): object provided for the equality test.

    Returns
        dict|None: nested data dictionary if case insensitive match on the < filter > is
                   obtained; otherwise < None > is returned
    """
    for item in data:
        if item[key] == filter:
            return item




def get_resource(url, params=None, timeout=10):
    """Returns a response object decoded into a dictionary. If query string < params > are
    provided the response object body is returned in the form on an "envelope" with the data
    payload of one or more entities to be found in ['results'] list; otherwise, response
    object body is returned as a single dictionary representation of the entity.

    Parameters:
        url (str): a uniform resource locator that specifies the resource.
        params (dict): optional dictionary of querystring arguments.
        timeout (int): timeout value in seconds

    Returns:
        dict: dictionary representation of the decoded JSON.
    """

    if params:
        return requests.get(url, params, timeout=timeout).json()
    else:
        return requests.get(url, timeout=timeout).json()


def read_csv_to_dicts(filepath, encoding='utf-8', newline='', delimiter=','):
    """Accepts a file path, creates a file object, and returns a list of dictionaries that
    represent the row values using the cvs.DictReader().

    WARN: This function must be implemented using a list comprehension in order to earn points.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: nested dictionaries representing the file contents
     """

    with open(filepath, 'r', newline=newline, encoding=encoding) as file_obj:
        # data = []
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        # for line in reader:
        #     data.append(line) # OrderedDict() | alternative: data.append(dict(line))
        return [line for line in reader]


def read_json(filepath, encoding='utf-8'):
    """Reads a JSON document, decodes the file content, and returns a list or dictionary if
    provided with a valid filepath.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """

    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)

def save_cache(filepath, cache):
    with open(filepath, 'w') as file:
        json.dump(cache, file)

def fetch_data_until_invalid(start_id, max_invalid=10):
    all_data = {}
    consecutive_invalid = 0

    current_id = start_id
    while consecutive_invalid < max_invalid:
        url = f"{HYRULE_ENTRY}{current_id}"
        response = request_data(url)
        if response and 'data' in response:
            all_data[current_id] = response['data']
            consecutive_invalid = 0  # Reset counter on valid response
        else:
            consecutive_invalid += 1  # Increment counter on invalid response

        current_id += 1

    return all_data


def fetch_item_details(item_name, cache, cache_filepath):
    if item_name in cache:
        return cache[item_name]

    url = f"{HYRULE_ENTRY}{item_name}"
    response = request_data(url)
    if response and 'data' in response:
        item_data = response['data']

        if item_data['category'] == 'materials':
            # Convert 'hearts_recovered' to numeric if present
            if 'hearts_recovered' in item_data and item_data['hearts_recovered'] is not None:
                item_data['hearts_recovered'] = convert_to_numeric(item_data['hearts_recovered'])

            # Convert 'fuse_attack_power' to numeric only if present
            if 'fuse_attack_power' in item_data and item_data['fuse_attack_power'] is not None:
                item_data['fuse_attack_power'] = convert_to_numeric(item_data['fuse_attack_power'])

        elif item_data['category'] == 'equipment':
            properties = item_data.get('properties', {})
            properties['attack'] = convert_to_numeric(properties.get('attack', 0))
            properties['defense'] = convert_to_numeric(properties.get('defense', 0))
            item_data['properties'] = properties

        elif item_data['category'] == 'creatures':
            item_data['hearts_recovered'] = convert_to_numeric(item_data.get('hearts_recovered', 0))

        cache[item_name] = response['data']
        save_cache(cache_filepath, cache)
        return response['data']
    return None

def find_minimal_heart_recovery(hearts_needed, materials_data):
    # Convert materials_data to a list of (material_name, hearts_recovered)
    materials = [(mat['name'], mat['hearts_recovered']) for mat in materials_data]

    # Initialize DP array, where dp[i] will be the minimal number of materials to recover i hearts
    dp = [float('inf')] * (hearts_needed + 1)
    dp[0] = 0  # Base case: 0 materials needed to recover 0 hearts

    # Store the combination of materials
    combination = [None] * (hearts_needed + 1)

    for i in range(1, hearts_needed + 1):
        for material, hearts in materials:
            if hearts <= i and dp[i - hearts] + 1 < dp[i]:
                dp[i] = dp[i - hearts] + 1
                combination[i] = material

    # Reconstruct the combination of materials
    if dp[hearts_needed] == float('inf'):
        return "No combination found"

    result_combination = []
    while hearts_needed > 0:
        material = combination[hearts_needed]
        result_combination.append(material)
        hearts_needed -= next(mat[1] for mat in materials if mat[0] == material)

    return ', '.join(result_combination)

def fetch_data_by_category(category):
    """
    Fetch data from the API for a given category.
    """
    api_url = f"https://your-api-endpoint.com/{category}"  # Replace with your actual API endpoint
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        return data  # Assuming the API returns the data in JSON format
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def fetch_all_entries():
    # Replace with the actual endpoint to fetch all entries
    api_url = "https://your-api-endpoint.com/all_entries"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def find_minimal_heart_combination(hearts_needed, items):
    # Sort items by their heart recovery value
    items.sort(key=lambda x: x['hearts_recovered'])

    # Initialize a list to store the best combination for each heart value up to hearts_needed
    best_combinations = [None] * (int(hearts_needed * 10) + 1)  # Multiplied by 10 to handle decimal values
    best_combinations[0] = []

    # Iterate through each possible heart value
    for heart_value in range(len(best_combinations)):
        for item in items:
            if item['hearts_recovered'] * 10 <= heart_value:
                prev_value = heart_value - int(item['hearts_recovered'] * 10)
                if best_combinations[prev_value] is not None:
                    if best_combinations[heart_value] is None or len(best_combinations[prev_value]) + 1 < len(best_combinations[heart_value]):
                        best_combinations[heart_value] = best_combinations[prev_value] + [item]

    # Find the combination closest to but not exceeding hearts_needed
    for heart_value in range(int(hearts_needed * 10), -1, -1):
        if best_combinations[heart_value] is not None:
            return best_combinations[heart_value]

    return None

def perform_local_analysis(hearts_needed):
    with open('hearts_recovered_entries.json', 'r') as file:
        items_data = json.load(file)
    items = list(items_data.values())
    best_combo = find_minimal_heart_combination(hearts_needed, items)

    if best_combo:
        combo_str = ' + '.join(f"{item['name']}({item['hearts_recovered']})" for item in best_combo)
        total_hearts = sum(item['hearts_recovered'] for item in best_combo)
        combo_str += f" = {total_hearts} hearts"
        return combo_str, best_combo
    else:
        return "No combination found", None

# Example usage
hearts_needed = 5  # You can change this value for testing
combo_str, combo_items = perform_local_analysis(hearts_needed)
print(combo_str)