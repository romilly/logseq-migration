import os
import re
from typing import List, Tuple
import requests

PIP_ROOT = '/home/romilly/git/active/logseq-migration/test/data/graphs/pip'


def link_from(line):
    if '{{pdf' in line:
        link = re.search(r'https://firebasestorage(.*)\?alt([^\}]*)', line)
    else:
        link = re.search(r'https://firebasestorage(.*)\?alt([^/)]*)', line)
    if link is None:
        raise ValueError('unexpected format: %s' % line )
    return link.group(0)


def add_url_to_assets(link: str, asset_dir):
    get_file_name(link)


def get_file_name(url: str):
    short_url = url.split('?')[0]
    r = requests.get(short_url)
    json = r.json()
    file_name = json['metadata']['file-name']
    return file_name


def process(file_path: str, lines: List[Tuple[int, str]], asset_dir: str):
    with open(file_path) as md:
        content = md.readlines()
        for number, line in lines:
            link = link_from(line)
            new_location = add_url_to_assets(link, asset_dir)
            # content[number] = replace_url(url, new_location, content[number])
    with open(file_path,'w') as md:
        md.write(''.join(content))




def migrate(vault_directory):
    assets_dir = vault_directory + '/assets'
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    for subdir, dirs, files in os.walk(vault_directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(subdir, file)
                with open(file_path) as md:
                    numbered_lines = enumerate(line for line in md)
                    lines = list((number, line) for number, line in numbered_lines if 'https://firebasestorage' in
                                 line)
                if len(lines) > 0:
                    process(file_path, lines, assets_dir)


if __name__ == '__main__':
    migrate(PIP_ROOT)