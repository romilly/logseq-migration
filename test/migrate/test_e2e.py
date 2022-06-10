import os
import shutil
import unittest

from hamcrest import assert_that, contains_string

from migration.migrater import migrate

IMPORTED_GRAPH_NAME = 'test-vault'
IMPORTED_VAULT = os.path.join('test/data/test/', IMPORTED_GRAPH_NAME)
TEST_GRAPH_DIRECTORY = 'test/data/graphs/'
TEST_GRAPH = os.path.join(TEST_GRAPH_DIRECTORY, IMPORTED_GRAPH_NAME)
TEST_PAGES = os.path.join(TEST_GRAPH, 'pages')
TEST_ASSETS = os.path.join(TEST_GRAPH, 'assets')

PATH1 = os.path.join(TEST_PAGES, 'page with some text.md')
IMAGE = os.path.join(TEST_ASSETS, 'autocode.png')
PATH2 = os.path.join(TEST_PAGES, 'another with an mp4.md')
MP4   = os.path.join(TEST_ASSETS, 'adc.mp4')
PATH3 = os.path.join(TEST_PAGES, 'page with a pdf.md')
PDF   = os.path.join(TEST_ASSETS, 'README.pdf')

def read(path):
    with open(path) as f:
        return f.read()


class E2ETestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if os.path.exists(TEST_GRAPH):
            shutil.rmtree(TEST_GRAPH)
        shutil.copytree(IMPORTED_VAULT, TEST_GRAPH)
        migrate(TEST_GRAPH)

    def test_copies_image(self):
        md = read(PATH1)
        assert_that(md, contains_string('../assets/autocode.png'))
        assert_that(os.path.exists(IMAGE))

    def test_copies_mp4(self):
        md = read(PATH2)
        assert_that(md, contains_string('../assets/adc.mp4'))
        assert_that(os.path.exists(MP4))

    def test_copies_pdf(self):
        md = read(PATH3)
        assert_that(md, contains_string('../assets/README.pdf'))
        assert_that(os.path.exists(PDF))


if __name__ == '__main__':
    unittest.main()
