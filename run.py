#!/usr/bin/python3

"""
    run the server
"""

import sys

from app import app as application

import config

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].isdigit() and int(sys.argv[1]) < 65536:
        config.port = int(sys.argv[1])
    application.run(host=config.host, port=config.port, debug=config.debug)
