"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import logging
import shutil

from stevedore import driver
import yaml

from ruck.config import Config
from ruck import exceptions
from ruck.log import setup_log


class Runner(object):
    def __init__(self, state):
        self.state = state
        self.config = Config(self.state)
        self.logging = logging.getLogger(__name__)

    def run(self):
        setup_log()

        self.logging.info("Running ruck.")
        if not self.state.config.exists():
            exceptions.ConfigError(
                f"Failed to load configuration file: {self.state.config}")
        config = self.config.load_template(self.state.config)
        config = yaml.safe_load(config)

        self.logging.info("Setting up workspace.")
        name = config.get("name", None)
        if name is None:
            raise exceptions.ConfigError("Workspace name is not specified.")
        self.workspace = self.state.workspace.joinpath(name)

        self.logging.info("Copying configuration to workspace.")
        shutil.copytree(
            self.state.config.parent,
            self.workspace,
            dirs_exist_ok=True)

        actions = config.get("actions", None)
        if actions is None:
            raise exceptions.ConfigError(
                "Unable to determine actions.")

        self.logging.info(f"Running {name}.")
        for action in actions:
            act = action.get("action", None)
            if act is None:
                raise exceptions.ConfigError(
                    f"Unable to determine action: {act}.")

            try:
                mgr = driver.DriverManager(
                    namespace="ruck.plugins",
                    name=act,
                    invoke_on_load=True,
                    invoke_args=(self.state,
                                 config,
                                 action,
                                 self.workspace),
                )
                mgr.driver.run_actions()
            except Exception as err:
                self.logging.error(
                    f"Failed to import plugin: {act}: {err}.")
