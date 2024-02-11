"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import logging

from ruck.log import setup_log


class Runner(object):
    def __init__(self, state):
        self.state = state
        self.logging = logging.getLogger(__name__)

    def run(self):
        setup_log()

        self.logging.info("Running ruck.")
