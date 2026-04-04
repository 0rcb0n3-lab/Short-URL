import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    user_input = requests.get(url)
    user_input.raise_for_status()
    if user_input.ok:
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        link_to_short = {"url": url}
        api_url = "https://clc.li/api/url/add"
        response = requests.post(api_url, headers=headers, json=link_to_short)
        response.raise_for_status()
        short_link = response.json()['shorturl']
        return short_link
    else:
        raise requests.exceptions.HTTPError(response=user_input)


def count_clicks(token, url):
    edited_link = requests.get(url)
    edited_link.raise_for_status()
    if edited_link.ok:
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        get_url_list = "https://clc.li/api/urls"
        response = requests.get(get_url_list, headers=headers)
        response.raise_for_status()
        full_info = response.json()
        for click in full_info['data']['urls']:
            if click['shorturl'] == url:
                text_template = f"URL: {click['shorturl']} total clicks: {click['clicks']}"
        return text_template

    else:
        raise requests.exceptions.HTTPError(response=edited_link)


def is_bitlink(url):
    sample = 'clc.li'
    parsed = urlparse(url)
    netloc = parsed.netloc
    return netloc == sample or netloc.endswith('.' + sample)


def main():
    load_dotenv()
    token = os.getenv("TOKEN")
    url = input("Введите ссылку: ")

    if not is_bitlink(url):
        try:
            short_link = shorten_link(token, url)
            print("Короткая ссылка", short_link)
        except requests.exceptions.HTTPError:
            print("Ошибка HTTPError: Проверьте ссылку")
    else:
        try:
            clicks_count = count_clicks(token, url)
            print(clicks_count)
        except requests.exceptions.HTTPError:
            print("Ошибка HTTPError: Проверьте короткую ссылку")


if __name__ == "__main__":
    main()
