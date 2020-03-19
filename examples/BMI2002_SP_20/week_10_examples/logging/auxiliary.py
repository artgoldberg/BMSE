# in auxiliary.py
import logging

# create logger
auxiliary_module_logger = logging.getLogger('spam_app.auxiliary')

class Auxiliary:
    def __init__(self):
        self.logger = logging.getLogger('spam_app.auxiliary.Auxiliary')
        self.logger.addHandler(logging.FileHandler('/tmp/auxiliary.log'))
        self.logger.info('creating an instance of Auxiliary')

    def do_something(self):
        self.logger.info('doing something')

def some_function():
    auxiliary_module_logger.info('received a call to "some_function"')
