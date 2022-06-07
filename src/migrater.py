import os
import re
import sys
from typing import List, Tuple
import requests


def link_from(line):
    if '{{pdf' in line or '{{video' in line:
        link = re.search(r'https://firebasestorage(.*)\?alt([^\}]*)', line)
    else:
        link = re.search(r'https://firebasestorage(.*)\?alt([^/)]*)', line)
    if link is None:
        raise ValueError('unexpected format: %s' % line)
    return link.group(0)


def add_url_to_assets(link: str, asset_dir, relative_asset_dir):
    file_name = get_file_name(link)
    file_path = os.path.join(asset_dir, file_name)
    relative_path = os.path.join(relative_asset_dir, file_name)
    if not os.path.exists(file_path):
        r = requests.get(link)
        print('downloaded %s to %s' % (link, relative_path))
        with open(file_path, 'wb') as asset:
            asset.write(r.content)
    return relative_path


def get_file_name(url: str):
    short_url = url.split('?')[0]
    r = requests.get(short_url)
    json = r.json()
    file_name = json['metadata']['file-name']
    return file_name


def process(file_path: str, lines: List[Tuple[int, str]], asset_dir: str, relative_asset_dir: str):
    with open(file_path) as md:
        content = md.readlines()
        for number, line in lines:
            link = link_from(line)
            new_location = add_url_to_assets(link, asset_dir, relative_asset_dir)
            content[number] = content[number].replace(link, new_location)
    with open(file_path, 'w') as md:
        md.write(''.join(content))


def migrate(vault_directory):
    relative_assets_dir = 'assets'
    assets_from_page_dir = os.path.join('..', relative_assets_dir)
    assets_dir = os.path.join(vault_directory, relative_assets_dir)
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    for subdir, dirs, files in os.walk(vault_directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(subdir, file)
                with open(file_path) as md:
                    numbered_lines = enumerate(line for line in md)
                    lines = list((number, line) for
                                 number, line in numbered_lines if 'https://firebasestorage' in line)
                if len(lines) > 0:
                    process(file_path, lines, assets_dir, assets_from_page_dir)


if __name__ == '__main__':
    if 2 != len(sys.argv):
        print('usage python3 run.py <vault-directory')
        sys.exit(1)
    vault_directory = sys.argv[1]
    print('migrating %s' % vault_directory)
    migrate(vault_directory)