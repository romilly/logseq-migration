import logging


class LoggingMonitor:
    def __init__(self, debug_level: int):
        levels = [logging.INFO, logging.DEBUG]

        logging.basicConfig(level=levels[debug_level],
                            filename='migration.log',
                            filemode='a')

    def version(self, version):
        logging.info('migrator version %s' % version)

    def migrating(self, directory):
        logging.info('migrating directory %s' % directory)

    def processing(self, file_path):
        logging.debug('processing %s' % file_path)

    def markdown_decode_error(self, file_path, exception: Exception):
        logging.error('could not decode %s - %s' % (file_path, str(exception)))

    def updating(self, file_path):
        logging.debug('updating markdown file %s' % file_path)

    def downloading(self, link, relative_path):
        logging.debug('downloading %s as %s' % (link, relative_path))

    def downloaded(self, link):
        logging.debug('successfully downloaded %s' % link)

    def download_failed(self, link, exception: Exception):
        logging.error('could not download %s - %s' % (link, str(exception)))

    def done(self):
        logging.info('run completed')














