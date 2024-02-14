"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""
import logging

from ruck import exceptions
from ruck import utils
from ruck.plugins.base import Base
from ruck.schema import validate

SCHEMA = {
    "name": {"type": "string"},
    "action": {"type": "string"},
    "target": {"type": "string", "redquired": True},
}


class PackPlugin(Base):
    def __init__(self, state, config, action, workspace):
        self.state = state
        self.config = config
        self.action = action
        self.workspace = workspace
        self.logging = logging.getLogger(__name__)

    def run_actions(self):
        status = validate(self.action, SCHEMA)
        if status:
            name = self.action.get("name")
            self.logging.info(name)

            rootfs = self.workspace.joinpath("rootfs")
            if rootfs.exists() is None:
                raise exceptions.PluginError(
                    f"Unable to compress {rootfs}, unpack it first.")
            target = self.action.get("target")
            utils.run_command(
                ["tar", "-C", rootfs, "-czf", target],
                cwd=self.workspace)
