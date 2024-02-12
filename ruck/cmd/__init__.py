
"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import click


class State:
    def __init__(self):
        self.debug = False
        self.config = None
        self.workspace = None


# pass State between command and ruck sub-commands
pass_state_context = click.make_pass_decorator(State, ensure=True)
