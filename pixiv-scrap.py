#!/usr/bin/python3

import argparse
import math
import os
import pathlib
import requests
import time
import sys

from glob import glob
from http.cookiejar import MozillaCookieJar
from urllib.parse import quote as url_encode

parser = argparse.ArgumentParser(description='Scrap images from pixiv')
parser.add_argument('keyword', metavar='keyword', type=str, help='Search/tags keyword')
parser.add_argument('--depth', type=int, help='Maximum number of page')
args = parser.parse_args()

key = args.keyword
encoded_key = url_encode(key)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'referer': '',
}

pathlib.Path(key).mkdir(exist_ok=True)

def file_exists(dir, image_id, page_count):
    file_list = glob(f'{dir}/*')
    file_found = [s for s in file_list if image_id in s]
    if len(file_found) != page_count:
        return False
    if file_found:
        return True
    else:
        return False

cookies_file = str(pathlib.Path(__file__).parent.absolute() / 'cookies.txt')
cookies = MozillaCookieJar(cookies_file)
cookies.load()
session = requests.Session()
session.cookies = MozillaCookieJar('cookies.txt')
session.cookies.load()

base_url = f'https://www.pixiv.net/ajax/search/illustrations/{key}?word={key}&order=date_d&mode=all&p=1&s_mode=s_tag_full&type=illust_and_ugoira'

headers.update({'referer': f'https://www.pixiv.net/en/tags/{encoded_key}/illustrations?p=1'})
search_result = session.get(base_url, cookies=cookies, headers=headers).json()
illust_total = search_result['body']['illust']['total']
total_page = math.ceil(illust_total/60)
if total_page == 0:
    print('No image found')
    sys.exit()
if args.depth:
    total_page = args.depth
for page in range(1, total_page+1):
    print(f'Downloading page {page}...')
    time.sleep(5)
    url = f'https://www.pixiv.net/ajax/search/illustrations/{key}?word={key}&order=date_d&mode=all&p={page}&s_mode=s_tag_full&type=illust_and_ugoira'
    json_data = session.get(url, cookies=cookies, headers=headers).json()
    illust_data = json_data['body']['illust']['data']
    for illust in illust_data:
        illust_id = illust['id']
        illust_title = illust['title']
        page_count = illust['pageCount']
        headers.update({"referer": f"https://www.pixiv.net/member_illust.php?mode=medium&illust_id={illust_id}"})
        if file_exists(key, illust_id, page_count):
            print(f'Image {illust_id}: {illust_title} already downloaded')
            continue
        time.sleep(2)
        if illust['illustType'] == 2:
            ugiora_data = session.get(f"https://www.pixiv.net/ajax/illust/{illust_id}/ugoira_meta", cookies=cookies, headers=headers).json()
            img_urls = [ugiora_data['body']['originalSrc']]
        elif page_count == 1:
            illust_url = session.get(f"https://www.pixiv.net/ajax/illust/{illust_id}", cookies=cookies, headers=headers).json()
            img_urls = [illust_url['body']['urls']['original']]
        else:
            img_urls = []
            illust_url = session.get(f"https://www.pixiv.net/ajax/illust/{illust_id}/pages", cookies=cookies, headers=headers).json()
            body_content = illust_url['body']
            for content in body_content:
                img_urls.append(content['urls']['original'])
        page_index = 0
        for img_url in img_urls:
            time.sleep(2)
            if page_index == 0:
                page_num = ''
            else:
                page_num = f'_p{page_index}'
            file_ext = os.path.splitext(img_url)[1]
            title_clean = illust_title.replace('/', '_')
            file_name = f'{title_clean}_{illust_id}{page_num}{file_ext}'
            res = session.get(img_url, cookies=cookies, headers=headers, stream=True)
            with open(os.path.join(key, file_name), "wb") as file:
                for chunk in res.iter_content(chunk_size=1048576):
                    file.write(chunk)
            print(f'Downloaded: {illust_title} as {file_name}')
            page_index += 1
