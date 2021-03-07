from yaml import safe_load


def load_from_file(file_name):
    """
    Reads a full YAML file into a dictionary
    :param file_name: The file to read the yaml values from
    :return: A python dictionary with those values
    """
    with open(file_name, "r") as config_file:
        return safe_load(config_file)
