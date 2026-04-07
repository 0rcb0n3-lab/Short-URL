import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    link_to_short = {"url": url}
    api_url = "https://clc.li/api/url/add"
    response = requests.post(api_url, headers=headers, json=link_to_short)
    response.raise_for_status()
    short_link = response.json()['shorturl']
    return short_link


def count_clicks(token, url):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    get_url_list = "https://clc.li/api/urls"
    response = requests.get(get_url_list, headers=headers)
    response.raise_for_status()
    full_info = response.json()

    for click in full_info['data']['urls']:
        if click['shorturl'] == url:
            text = f"URL: {click['shorturl']} - clicks: {click['clicks']}"
    return text


def is_bitlink(url):
    sample = 'clc.li'
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    return netloc == sample or netloc.endswith('.' + sample)


def main():
    load_dotenv()
    token = os.environ['CLC_TOKEN']
    url = input("Введите ссылку: ")

    if is_bitlink(url):
        try:
            clicks_count = count_clicks(token, url)
            print(clicks_count)
        except requests.exceptions.HTTPError:
            print("Ошибка HTTPError: Проверьте короткую ссылку")
    else:
        try:
            short_link = shorten_link(token, url)
            print("Короткая ссылка", short_link)
        except requests.exceptions.HTTPError:
            print("Ошибка HTTPError: Проверьте ссылку")


if __name__ == "__main__":
    main()
