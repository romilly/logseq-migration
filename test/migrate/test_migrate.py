import unittest

from logseq.migration.migrater import link_from, get_file_name
from test.migrate.samples import PDF, CRAB, PDF_URL, CRAB_URL


class MigrateTestCase(unittest.TestCase):
    def test_extracts_link_for_pdf(self):
        self.assertEqual(PDF_URL, link_from(PDF))

    def test_extracts_link_for_image(self):
        self.assertEqual(CRAB_URL, link_from(CRAB))

    def test_finds_original_filename(self):
        filename = get_file_name(CRAB_URL)
        self.assertEqual('IMG20201019182950.jpg', filename)
        filename = get_file_name(PDF_URL)
        self.assertEqual('RB 2021-10-15 11.58.11.pdf', filename)


if __name__ == '__main__':
    unittest.main()
