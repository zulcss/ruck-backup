"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""
import logging

from cerberus import Validator

from ruck.plugins.base import Base

from ruck.schemas.dummy import DUMMY_SCHEMEA


class DummyPlugin(Base):
    def __init__(self, state, config, action, workspace):
        self.state = state
        self.config = config
        self.action = action
        self.workspace = workspace
        self.logging = logging.getLogger(__name__)

    def run_actions(self):
        v = Validator()
        v.schema = DUMMY_SCHEMEA

        name = self.action.get("name")
        if not v.validate(self.action):
            raise Exception("Error in action: ", v.errors)
        else:
            self.logging.info(name)
            print(f"Action: {self.action.get('echo')}")
