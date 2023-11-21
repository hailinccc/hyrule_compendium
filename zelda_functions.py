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

def fetch_item_details(item_name, cache, cache_filepath):
    # Check if the item is in the cache
    if item_name in cache:
        return cache[item_name]

    # If not in cache, make the API request
    url = f"{HYRULE_ENTRY}{item_name}"
    response = request_data(url)
    if response and 'data' in response:
        # Store the new data in the cache and save it
        cache[item_name] = response['data']
        save_cache(cache_filepath, cache)
        return response['data']
    return None