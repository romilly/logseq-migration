import unittest
from unittest.mock import Mock

from logseq.migration.migrater import Migrator
from logseq.migration.monitor import LoggingMonitor

# TODO: Add more unit tests for failure logging of failure conditions.


class FailedDownloadTestCase(unittest.TestCase):
    def test_download_non_existent_url(self):
        migrator = Migrator(monitor=Mock(LoggingMonitor))
        migrator.process_file(None, None, 'no_such_dile.md', '.')
        migrator.monitor.markdown_decode_error.assert_called()



if __name__ == '__main__':
    unittest.main()
