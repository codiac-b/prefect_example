import json

def read_api_key(source_name:str, file_path='../data_source/api_key.json') -> str:
    """
    Read apu key from a local file
    :param source_name: The name of the top level key to read
    :param file_path: The path to the file. Default is '../data_source/api_key.json'
    :return:
    """
    with open(file_path) as f:
        data = json.load(f)
    return data[source_name]['apiKey'
    ]