# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_ruck
----------------------------------

Tests for `ruck` module.
"""

import os
import tempfile

from click.testing import CliRunner

from ruck.cmd.shell import cli
from ruck.tests import base


class TestCLI(base.TestCase):

    def setUp(self):
        super(TestCLI, self).setUp()

        self.dirname = tempfile.mkdtemp()

    def test_cli_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0

    def test_cli_workspace(self):
        with open(os.path.join(self.dirname, "workspace.yaml"), "w") as f:
            f.write(
                """
---
name: test
actions:
  - name: test 1
    action: dummy
    echo: test
"""
            )
        runner = CliRunner()
        result = runner.invoke(cli,
                               ["--workspace",
                                os.path.join(self.dirname, "test"),
                                "--config",
                                os.path.join(self.dirname, "workspace.yaml")])
        assert result.exit_code == 0
        assert os.path.exists(os.path.join(self.dirname, "test")) is True

    def test_cli_invalid_node(self):
        with open(os.path.join(self.dirname, "workspace.yaml"), "w") as f:
            f.write(
                """
---
name: test
actions:
  - name: test 1
    action: dummy
    echo: 1
"""
            )
        runner = CliRunner()
        result = runner.invoke(cli,
                               ["--workspace", os.path.join(
                                   self.dirname, "test"),
                                "--config", os.path.join(
                                   self.dirname, "workspace.yaml")])
        assert "Failed to import plugin:" in result.output
