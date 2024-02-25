import json
import pprint
import logging
import datetime as dt
import requests
from etl.src.utilities.read_api_key import read_api_key
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_daily_currency_exchange_rate(version: str = '1',
                               date: str = 'latest',
                               base_currency: str = 'usd',
                               target_currency: str = None) -> dict:
    """
    Get the currency exchange rate

    :param version: api version. Default is '1'
    :param date: The date of the exchange rate. Default is 'latest'. Specify a date in the format 'YYYY-MM-DD' to get the exchange rate for that date.
    :param base_currency: The base currency. Default is 'USD'
    :param target_currency: Optional. The target currency. Default is None. If None, all currencies are returned.
    :return:
    """
    main_url_end = '.json'
    min_url_end = '.min.json'

    def get_currency_codes() -> dict:
        """
        Get the currency codes
        :return:
        """
        url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies'
        long_url: str = f'{url}{main_url_end}'
        min_url: str = f'{url}{min_url_end}'

        code_response = None

        try:
            code_response = requests.get(long_url)
        except requests.exceptions.RequestException as e:
            logger.info(f'Error getting currency codes from {long_url}. Falling back to minified url. \n{e}')
            try:
                code_response = requests.get(min_url)
            except requests.exceptions.RequestException as e:
                logger.error(f'Error getting currency codes from primary and secondary urls. \n{e}')

        if code_response is None:
            logger.error(f'Error getting currency codes. Response is None')
            raise Exception(f'Error getting currency codes. Response is None')

        if code_response.status_code != 200:
            logger.error(f'Error getting currency codes. Status code: {code_response.status_code}')
            raise Exception(f'Error getting currency codes. Status code: {code_response.status_code}')

        return json.loads(code_response.content)

    def hit_api(url:str = None) -> requests.Response:
        """
        Try the main url. If it fails, try the minified url, else raise an exception
        :return:
        """
        try:
            _response = requests.get(url + main_url_end)
        except requests.exceptions.RequestException as e:
            logger.error(f'Error getting data from {url+main_url_end}. Trying fallback \n{e}')
            try:
                _response = requests.get(url + min_url_end)
            except requests.exceptions.RequestException as e:
                logger.error(f'Error getting data from {url+min_url_end}. \n{e}')
                raise Exception(f'Error getting data from {url+min_url_end}. \n{e}')
        if _response.status_code != 200:
            logger.error(f'Error getting data from {url+main_url_end}. Status code: {_response.status_code}')
            raise Exception(f'Error getting data from {url+main_url_end}. Status code: {_response.status_code}')
        return _response

    def create_url() -> str:
        """
        Create the url
        :return:
        """
        url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@{version}/{date}/currencies/{base_currency}'
        if target_currency is not None:
            url += f'/{target_currency}'
        return url

    response = hit_api(url=create_url())
    out = json.loads(response.content)
    return out

def get_currency_exchange_rate(date: str|list|set|tuple = 'latest', base_currency: str ='usd', target_currency: str = None) -> dict[dict]|dict:
    """
    Get the currency exchange rate. If date is a list, return the exchange rate for each date in the list
    :return:
    """
    if isinstance(date, str):
        date = [date]
    df = pd.DataFrame([i for i in date])
    new = df.apply(lambda x: get_daily_currency_exchange_rate(date=x[0],
                                                            base_currency=base_currency,
                                                            target_currency=target_currency),
                                                            axis=1)
    print(new)
    new = new.to_dict()

    return new




if __name__ == '__main__':

    # data = get_noaa_ghcnd_data(url='https://www.ncei.noaa.gov/cdo-web/api/v2/data', start_date='2020-01-31', end_date='2020-03-31')
    # print(len(data))
    # pprint.pprint(data)
    out = get_currency_exchange_rate(date=['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-06', '2024-01-07', '2024-01-08', '2024-01-09', '2024-01-10'])
    pprint.pprint(out)