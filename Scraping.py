import requests
import urllib.error
from bs4 import BeautifulSoup
from os import listdir
from multiprocessing import Pool
from urllib.parse import urlparse
from random import choice
from functools import partial


def find_urls(path):
    urls = list()
    for file_html in listdir(path):
        with open(path + '/' + file_html, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:  # href empty tag
                continue
            if not (urlparse(href).netloc and urlparse(href).scheme):
                continue
            urls.append(href)
    return urls


def settings():
    with open('proxy.txt', 'r') as f:
        proxies = f.read().split('\n')
    with open('user-agent.txt', 'r') as f:
        useragents = f.read().split('\n')
    return proxies, useragents


def check_url(urls, proxies, useragents, link):
    proxy = {'http': 'http://' + choice(proxies)}
    useragent = {'User-Agent': choice(useragents)}
    try:
        req = requests.get(link, headers=useragent, proxies=proxy, timeout=5)
        status = req.status_code
    except urllib.error.HTTPError as e:
        print(f'HTTPError: {e.code} - {link}')  # (e.g. 404, 501, etc)
    except urllib.error.URLError as e:
        print(f'URLError: {e.reason} - {link}')  # (e.g. conn. refused)
    except ValueError as e:
        print(f'ValueError {e} - {link}')  # (e.g. missing protocol http)
    except TimeoutError as e:
        print(f'TimeoutError {e} - {link}')
    except Exception as e:
        print(f'Error {e} - {link}')
    else:
        print(f'{status} - {link}')


def main():
    path = "undead_pages"
    proxies, useragents = settings()
    urls = find_urls(path)
    func = partial(check_url, urls, proxies, useragents)
    with Pool(50) as p:
        p.map(func, urls)


if __name__ == '__main__':
    main()
