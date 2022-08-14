__author__ = "NimaFakoor"
__version__ = '1.1.1'


"""
This script runs the DoctorsSchedule application using a development server.
"""

from os import environ
import logging
from DoctorsSchedule import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    logging.basicConfig(filename='serverlog.log',format='[%(funcName)s] - %(levelname)s [%(asctime)s] %(message)s' , level=logging.DEBUG) 
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT)
