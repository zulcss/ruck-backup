"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""
import logging

from ruck.plugins.base import Base
from ruck.schema import validate

SCHEMA = {
    "description": {"type": "string"},
    "action": {"type": "string"},
    "echo": {"type": "string"},
}


class DummyPlugin(Base):
    def __init__(self, state, config, action, workspace):
        self.state = state
        self.config = config
        self.action = action
        self.workspace = workspace
        self.logging = logging.getLogger(__name__)

    def run_actions(self):
        status = validate(self.action, SCHEMA)
        if status:
            description = self.action.get("description")
            self.logging.info(description)
            print(f"Action: {self.action.get("echo")}")
