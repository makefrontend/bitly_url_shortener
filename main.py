import os
import argparse
import requests
from urllib.parse import urlparse

from dotenv import load_dotenv


def pars_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    return parser.parse_args()


def shorten_link(url, token):
    bitlink_url = 'https://api-ssl.bitly.com/v4/bitlinks/'
    headers = {
      'Authorization': token,
    }
    body = {
      'long_url': url,
    }
    response = requests.post(bitlink_url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()['link']


def get_bitlink_url(url):
    bitlink = urlparse(url)
    return '{}{}'.format(bitlink.netloc, bitlink.path)


def is_bitlink(url, token):
    bitlink_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'
    header = {
        'Authorization': token,
    }
    response = requests.get(bitlink_url.format(url), headers=header)
    return response.ok


def count_clicks(url, token):
    clicks_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary/'
    headers = {
        'Authorization': token,
    }
    response = requests.get(clicks_url.format(url), headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']}'


def main():
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    arguments = pars_arguments()
    url_user = arguments.url
    url_parse = get_bitlink_url(url_user)
    if is_bitlink(url_parse, bitly_token):
        try:
            bitlink_response = count_clicks(url_parse, bitly_token)
        except requests.exceptions.HTTPError:
            print('Не верная ссылка для подсчета кликов')
            return
    else:
        try:
            bitlink_response = shorten_link(url_user, bitly_token)
        except requests.exceptions.HTTPError as error:
            print('Ссылка введена не верно!')
            return
    print(bitlink_response)


if __name__ == '__main__':
    main()
