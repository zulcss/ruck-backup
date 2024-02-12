"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import logging

from jinja2 import Template


class Config(object):
    def __init__(self, state):
        self.state = state
        self.logging = logging.getLogger(__name__)

    def load_template(self, config):
        self.logging.info(f"Loading {config}.")
        with open(config, "r") as f:
            return Template(f.read()).render()
