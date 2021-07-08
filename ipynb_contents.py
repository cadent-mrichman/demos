#!/usr/bin/env python3

from argparse import ArgumentParser
import json
import os
import re


def process(filename, min_depth, max_depth):
    min_depth = min(min_depth, max_depth)
    with open(filename) as f:
        cells = json.load(f)['cells']
    headers = []
    for cell in cells:
        if cell['cell_type'] == 'markdown':
            sources = cell['source']
            for source in sources:
                if re.search('^#+ ', source):
                    headers.append(source)
    for head in headers:
        head = head.split('\n')[0].strip()
        depth = len(re.search('^#+', head).group(0))
        if min_depth <= depth <= max_depth:
            d = depth - min_depth
            text = re.sub('^#+ *', '', head)
            link = re.sub(r'[ ]', '-', text)
            link = re.sub(r'[`~]', '', link)
            print(d * ' ' + f'* [{text}](#{link})')


def main():
    parser = ArgumentParser()
    parser.add_argument('-i', '--min-depth', type=int, default=2)
    parser.add_argument('-d', '--max-depth', type=int, default=2)
    parser.add_argument('filename')
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        parser.error(f'"{args.filename}" not found')
    process(args.filename, args.min_depth, args.max_depth)

if __name__ == '__main__':
    main()
