import json
import os
import sys

from application import Application

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.js')


def main():
    if not os.path.isfile(CONFIG_FILE):
        sys.stderr.write(f'File "{CONFIG_FILE}" - missing')
        exit(1)

    with open(CONFIG_FILE) as fin:
        config = json.load(fin)

    # logger.create(config['log_file'], logging.INFO)

    application = Application(config)
    application.run()


if __name__ == '__main__':
    main()
