
# -*- coding: utf-8 -*-


"""Script to configure log system."""

import uuid
import logging
from logging.handlers import TimedRotatingFileHandler
import logging.config
from os import path


log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.ini')

logger = logging.getLogger("MLaaS")
logging.config.fileConfig(
    log_file_path,
    disable_existing_loggers=False,
    defaults={
        'logfilename': 'C:/Users/allan/Desktop/mlaas.log'
        })
