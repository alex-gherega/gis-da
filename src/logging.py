import logging
import logging.config
from pathlib import Path
import memoization

@memoization.cached
def access_mlogger(logger_name='GIS_DA',
                  logconfig=Path('logging.cfg').expanduser()):
    logging.config.fileConfig(fname=logconfig, disable_existing_loggers=False)
    return logging.getLogger(logger_name)

def access_logger(logger_name='GIS_DA',
                  logconfig=Path('logging.cfg').expanduser()):
    logging.config.fileConfig(fname=logconfig, disable_existing_loggers=False)
    return logging.getLogger(logger_name)


debug = access_mlogger().debug
info = access_mlogger().info
warning = access_mlogger().warning
error = access_mlogger().error
critical = access_mlogger().critical
exception = access_mlogger().exception
