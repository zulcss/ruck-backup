"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import errno
import sys

import click

from ruck.cmd.options import config_option
from ruck.cmd.options import debug_option
from ruck.cmd.options import workspace_option
from ruck.cmd import pass_state_context
from ruck.runner import Runner


@click.command
@pass_state_context
@debug_option
@config_option
@workspace_option
def cli(state, debug, config, workspace):
    try:
        Runner(state).run()
    except KeyboardInterrupt:
        click.secho("\n" + ("Exiting at your request."))
        sys.exit(130)
    except BrokenPipeError:
        sys.exit()
    except OSError as error:
        if error.errno == errno.ENOSPC:
            sys.exit("error - No space left on device.")


def main():
    cli(prog_name="ruck")
