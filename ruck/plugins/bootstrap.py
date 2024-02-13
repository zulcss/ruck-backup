"""
Copyright (c) 2024 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""
import logging

from ruck.plugins.base import Base
from ruck.schema import validate
from ruck import utils

SCHEMA = {
    "name": {"type": "string"},
    "action": {"type": "string"},
    "suite": {"type": "string", "required": True},
    "target": {"type": "string", "required": True},
    "packages": {"type": "list"},
    "variant": {"type": "string"},
    "components": {"type": "list"},
    "hooks": {"type": "list"},
    "setup-hooks": {"type": "list"},
    "extract-hooks": {"type": "list"},
    "customize-hooks": {"type": "list"},
    "essential-hooks": {"type": "list"},
}


class BootstrapPlugin(Base):
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

            # suite and target is required.
            suite = self.action.get("suite")
            target = self.action.get("target")

            cmd = [
                "mmdebstrap",
                "--architecture", "amd64"
            ]
            if self.state.debug:
                cmd.extend(["--debug"])
            else:
                cmd.extend(["--verbose"])

            # Install extra packages.
            packages = self.action.get("packages", None)
            if packages:
                cmd.extend([f"--include={','.join(packages)}"])

            # Enable extra components (main, non-free, etc).
            components = self.action.get("components", None)
            if components:
                cmd.extend([f"--components={','.join(components)}"])

            variant = self.action.get("variant", None)
            if variant:
                cmd.extend([f"--variant={variant}"])

            hooks = self.action.get("hooks", None)
            if hooks:
                cmd.extend([f"--hook-directory={hook}" for hook in hooks])

            setup_hooks = self.action.get("setup-hooks", None)
            if setup_hooks:
                cmd.extend([f"--setup-hook={hook}" for hook in setup_hooks])
            extract_hooks = self.action.get("extract-hook", None)
            if extract_hooks:
                cmd.extend(
                    [f"--extract-hook={hook}" for hook in extract_hooks])
            customize_hooks = self.action.get("customize-hooks", None)
            if customize_hooks:
                cmd.extend([f"--customize-hook={hook}" for hook in
                            customize_hooks])
            essential_hooks = self.action.get("essential-hooks", None)
            if essential_hooks:
                cmd.extend([f"--essential-hook={hook}" for hook in
                            essential_hooks])

            cmd.extend([suite, target])
            utils.run_command(cmd, cwd=self.workspace)
