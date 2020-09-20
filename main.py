import os
import requests
from lxml import html
import argparse
import json


parser = argparse.ArgumentParser(description="Use cache (default) or Update It")

parser.add_argument(
    "--update",
    dest="do_update",
    default=False,
    help="Do you want to update the cache ? ",
)

parser.add_argument(
    "--cache",
    dest="cache_file",
    default=f"{os.environ['HOME']}/.cache/git-emoji/cache-emoji.json",
    help="Path to the cache file",
)

args = parser.parse_args()

cache_file = args.cache_file
do_update = args.do_update if os.path.exists(cache_file) else True


def init():
    if not os.path.exists(cache_file):
        _temp = cache_file.rsplit("/", 1)
        dir = _temp[0] if len(_temp) > 1 else None
        if dir:
            os.makedirs(dir)


def scraper():
    init()
    URL = "https://gitmoji.carloscuesta.me/"

    resp = requests.get(URL)

    root = html.fromstring(resp.text)

    icons_xpath = "//div[@class='emoji-card']/header/span/text()"
    codes_xpath = "//div[@class='emoji-card']/div[@class='emoji-info']/div[@class='gitmoji-code']/code/text()"
    desc_xpath = "//div[@class='emoji-card']/div[@class='emoji-info']/p/text()"

    emojis = root.xpath(f"{icons_xpath} | {codes_xpath} | {desc_xpath} ")

    data = [
        {
            "icon": emojis[x].strip(),
            "code": emojis[x + 1].strip(),
            "desc": emojis[x + 2].strip(),
        }
        for x in range(0, len(emojis), 3)
    ]

    with open(cache_file, "wt") as file:
        json.dump(data, file, indent=2)

    pprintData(data)


def pprintData(data):
    for item in data:
        print(f"{item['icon']:>3} \t {item['desc']} \t {item['code']}")

if do_update:
    scraper()
else:
    with open(cache_file, "rt") as file:
        data = json.load(file)
    pprintData(data);
