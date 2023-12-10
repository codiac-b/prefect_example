import json

def read_api_key(file_path='etl/src/data_source/api_key.json', ):
    """
    Read a key from a local file
    :param file_path:
    :return:
    """
    with open(file_path) as f:
        data = json.load(f)
    return data['apiKey']