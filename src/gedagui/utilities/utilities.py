#!/usr/bin/python
# coding=utf-8

import imp
import os
import time

from appdirs import AppDirs

#===============================================================================
# Zupport common data

# Version information
__version_info__ = (0, 1, 0)
VERSION = '.'.join(map(str, __version_info__))


# Set the project paths
# WARNING! Because of this way of setting up the paths eggs must be created
# in zip-safe manner
# TODO: all configuration and ini-files should be moved to ~.zupport folder
APP_RESOURCES = os.path.join(os.path.dirname(__file__), 
                             'resources')
APP_ROOT = os.path.abspath(os.path.join(os.path.basename(APP_RESOURCES),
                                            '../'))
APP_DATA = os.path.join(APP_ROOT, 'data')
APP_DOCS = os.path.join(APP_ROOT, 'doc')
APP_PLUGINS = os.path.join(APP_ROOT, 'plugins')
APP_RESOURCES = os.path.join(APP_ROOT, 'resources')

appdirs = AppDirs('Zupport', 'HelsinkiUniversity', version=VERSION)

USER_DATA_DIR = appdirs.user_data_dir
USER_HISTORY_DIR = os.path.join(USER_DATA_DIR, 'history')
USER_PLUGINS_DIR = os.path.join(USER_DATA_DIR, 'plugins')
SITE_DATA_DIR = appdirs.site_data_dir
USER_CACHE_DIR = appdirs.user_cache_dir

LOGGING_INI = os.path.join(APP_RESOURCES, 'logging.ini')

