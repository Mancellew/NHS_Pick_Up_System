import json
from collections import namedtuple


def load_from_file(file_name):
    """
    Loads a full file containing valid JSON into a python JSON object
    :param file_name: The file to read the json from
    :return: A python object formed with the JSON data
    """
    with open(file_name, "r") as config_file:
        return json.load(config_file)


def load_from_string(text):
    """
    Loads a string containing valid JSON into a python JSON object
    :param text: The string to read the JSON from
    :return: A python JSON object formed with the JSON data
    """
    return json.loads(text)


def json_to_object(json_str):
    """
    Loads a python JSON string into a simple python object
    :param json_str: The JSON string to load as an object
    :return: A python object from the json provided
    """
    return json.loads(json_str, object_hook=__custom_decoder)


def __custom_decoder(obj_dict):
    """
    A custom function to be used as an object hook when constructing an object from JSON
    :param obj_dict: A python dictionary object to be parsed into an object
    :return: A named tuple working as a python object
    """
    return namedtuple('Obj', obj_dict.keys())(*obj_dict.values())
