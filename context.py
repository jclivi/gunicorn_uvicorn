import os
import sys

import log
import util

class Context(object):
    def __init__(self, etc):
        # config dict
        self.config = {}
        # load config
        self._load_config(etc)

    def _load_config(self, etc):
        # etc file
        if not os.path.exists(etc):
            sys.exit()

        # load options in json
        self.config = util.read_yml(etc)

