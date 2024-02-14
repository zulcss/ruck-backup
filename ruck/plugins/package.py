"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""
import logging
import os

from ruck import exceptions
from ruck.plugins.base import Base
from ruck.schema import validate
from ruck import utils

SCHEMA = {
    "description": {"type": "string"},
    "action": {"type": "string"},
    "packages": {"type": "list"},
    "clean": {"type": "boolean"},
    "update": {"type": "boolean"},
    "recomends": {"type": "boolean"},
}


class PackagePlugin(Base):
    def __init__(self, state, config, action, workspace):
        self.state = state
        self.config = config
        self.action = action
        self.workspace = workspace
        self.logging = logging.getLogger(__name__)

    def run_actions(self):
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"

        status = validate(self.action, SCHEMA)
        if status:
            description = self.action.get("description")
            self.logging.info(description)

        packages = self.action.get("packages")

        rootfs = self.workspace.joinpath("rootfs")
        if rootfs.exists() is None:
            raise exceptions.PluginError(
                f"{rootfs} does not exist. Please use unpack first.")
        update = self.action.get("update", False)
        if update:
            cmd = ["apt-get", "update", "-y"]
            utils.run_chroot(cmd, rootfs, cwd=self.workspace)

        rec = "--no-install-recommends"
        recommends = self.action.get("recommends", False)
        if recommends:
            rec = ""

        if packages:
            cmd = ["apt", "install", rec, "-y"] + packages

        utils.run_chroot(cmd, rootfs, env=env, cwd=self.workspace)

        clean = self.action.get("clean", False)
        if clean:
            cmd = ["apt-get", "clean"]
            utils.run_chroot(cmd, rootfs, env=env, cwd=self.workspace)
