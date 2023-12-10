import json
import requests
from etl.src.utilities.read_api_key import read_api_key
class GetData():
    pass

def explore_noaa_datasets():
    api_key = read_api_key()
    url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/datasets'
