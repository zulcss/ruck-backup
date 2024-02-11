"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import click

from ruck.cmd.options import debug_option
from ruck.cmd import pass_state_context
from ruck.runner import Runner


@click.command
@pass_state_context
@debug_option
def cli(state, debug):
    Runner(state).run()


def main():
    cli(prog_name="ruck")
