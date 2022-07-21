import os
import re
import sys
import uuid
from typing import List, Tuple
import requests

from logseq.migration.monitor import LoggingMonitor


class DownloadFailedException(Exception):
    pass


class Migrator:
    VERSION ='0.2'

    def __init__(self, debug_level: int = 0, monitor = None):
        if monitor is None:
            monitor = LoggingMonitor(debug_level)
        self.monitor = monitor

    def migrate(self, directory):
        print('version %s' % self.VERSION)
        self.monitor.version(self.VERSION)
        self.monitor.migrating(os.path.abspath(directory))
        relative_assets_dir = 'assets'
        assets_from_page_dir = os.path.join('..', relative_assets_dir)
        assets_dir = os.path.join(directory, relative_assets_dir)
        ensure_assets_dir_exists(assets_dir)
        self.process_files(assets_dir, assets_from_page_dir, directory)
        self.monitor.done()
        print('done')


    def process_files(self, assets_dir, assets_from_page_dir, vault_directory):
        for subdir, dirs, files in os.walk(vault_directory):
            for file in files:
                self.process_file(assets_dir, assets_from_page_dir, file,
                                  subdir)

    def process_file(self, assets_dir, assets_from_page_dir, file, subdir):
        if file.endswith('.md'):
            file_path = os.path.join(subdir, file)
            self.monitor.processing(file_path)
            try:
                with open(file_path, encoding='utf8') as md:
                    numbered_lines = enumerate(line for line in md)
                    lines = find_asset_references(numbered_lines)
            except Exception as e:
                self.monitor.markdown_decode_error(file_path, e)
                return
            if len(lines) > 0:
                self.process_assets(file_path, lines,
                                    assets_dir,
                                    assets_from_page_dir)

    def process_assets(self, file_path: str,
                       lines: List[Tuple[int, str]],
                       asset_dir: str,
                       relative_asset_dir: str):
        content = self.update_markdown_content(asset_dir,
                                               file_path, lines,
                                               relative_asset_dir)
        with open(file_path, 'w') as md:
            md.write(''.join(content))

    def update_markdown_content(self, asset_dir,
                                file_path, lines,
                                relative_asset_dir):
        self.monitor.updating(file_path)
        with open(file_path) as md:
            content = md.readlines()
            for number, line in lines:
                link = link_from(line)
                try:
                    new_location = self.add_url_to_assets(
                        link,
                        asset_dir,
                        relative_asset_dir)
                    content[number] = content[number].replace(link, new_location)
                except DownloadFailedException as e:
                    self.monitor.download_failed(link, e)
                    continue
        return content

    def add_url_to_assets(self, link: str, asset_dir, relative_asset_dir):
        file_name = get_file_name(link)
        file_path = os.path.join(asset_dir, file_name)
        relative_path = os.path.join(relative_asset_dir, file_name)
        if not os.path.exists(file_path):
            self.monitor.downloading(link, relative_path)
            try:
                r = requests.get(link)
                self.monitor.downloaded(link)
                with open(file_path, 'wb') as asset: # can this fail?
                    asset.write(r.content)
            except Exception as e:
                raise DownloadFailedException(e)
        return relative_path


def link_from(line):
    if '{{pdf' in line or '{{video' in line:
        link = re.search(r'https://firebasestorage(.*)\?alt([^}]*)', line)
    else:
        link = re.search(r'https://firebasestorage(.*)\?alt([^/)]*)', line)
    if link is None:
        raise ValueError('unexpected format: %s' % line)
    return link.group(0)


def get_file_name(url: str):
    short_url = url.split('?')[0]
    r = requests.get(short_url)
    json = r.json()
    file_name = json['metadata']['file-name']
    return file_name+'-%s' % uuid.uuid1()


def ensure_assets_dir_exists(assets_dir):
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)


def find_asset_references(numbered_lines):
    return list((number, line) for
                number, line in numbered_lines if 'https://firebasestorage' in line)


def main(*args):
    if len(args) == 0:
        args = sys.argv[1:]
    nargs = len(args)
    if nargs < 1 or nargs > 2:
        print_usage()
    if nargs == 2:
        debug_level = int(args[1])
        if debug_level not in [0,1]:
            print_usage()
    else:
        debug_level = 0
    vault_directory = args[0]
    migrate(vault_directory, debug_level)


def print_usage():
    print('usage localise_assets <vault-directory> [debug]')
    print('where debug is 0 or 1')
    sys.exit(3)


def migrate(vault_directory: str, debug_level=1):
    Migrator(debug_level).migrate(vault_directory)


if __name__ == '__main__':
    main()

