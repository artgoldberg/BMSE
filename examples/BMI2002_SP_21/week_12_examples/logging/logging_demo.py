# logging_demo.py
import logging

# create logger called 'spam_app'
spam_app_logger = logging.getLogger('spam_app')
spam_app_logger.setLevel(logging.DEBUG)

# create file handler which logs DEBUG messages
file_handler = logging.FileHandler('spam.log')
file_handler.setLevel(logging.DEBUG)

# create console handler with a higher log level, ERROR
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

# create formatter and add it to the handlers
# prints the current time, the logger's name, a log record's level, and the log message
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# add the handlers to the logger spam_app
spam_app_logger.addHandler(file_handler)
spam_app_logger.addHandler(console_handler)

spam_app_logger.info('creating an instance of Auxiliary')
spam_app_logger.error('OMG!')

import auxiliary
a = auxiliary.Auxiliary()

spam_app_logger.info('calling Auxiliary.do_something')
a.do_something()
print('logging_demo.py done')
