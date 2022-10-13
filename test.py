#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Scrap images from pixiv')
parser.add_argument('keyword', metavar='keyword', type=str, help='Search/tags keyword')
parser.add_argument('--depth', type=int, help='Maximum number of page')
args = parser.parse_args()
print(args.keyword)
if args.depth:
    print(f'Depth: {args.depth}')
else:
    print('Depth: 0')