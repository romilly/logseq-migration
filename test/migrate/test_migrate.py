import unittest

from migrate.migrater import match_from, get_file_name
from test.migrate.samples import PDF, CRAB, PDF_URL, CRAB_URL


class MigrateTestCase(unittest.TestCase):
    def test_extracts_match_for_pdf(self):
        match = match_from(PDF)
        expected = PDF_URL
        self.assertEqual(expected, match.group(0))

    def test_extracts_match_for_image(self):
        match = match_from(CRAB)
        expected = CRAB_URL
        self.assertEqual(expected, match.group(0))

    def test_finds_original_filename(self):
        filename = get_file_name(CRAB_URL)
        self.assertEqual('IMG20201019182950.jpg', filename)
        filename = get_file_name(PDF_URL)
        self.assertEqual('RB 2021-10-15 11.58.11.pdf', filename)




if __name__ == '__main__':
    unittest.main()
