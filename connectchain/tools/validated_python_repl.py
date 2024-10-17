# Copyright 2023 American Express Travel Related Services Company, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.
"""A version of PythonREPLTool that sanitizes the input before running it in the REPL."""
#pylint: disable=no-name-in-module too-few-public-methods unused-argument
import re
from typing import Any, Callable, Optional
from langchain_core.callbacks.manager import CallbackManagerForToolRun
from langchain_community.tools import PythonREPLTool


def default_sanitize_input(query: str) -> str:
    """Example sanitizer; modifies the input by removing leading and trailing spaces and `python` keyword

    IMPORTANT: This is a simplified example designed to showcase concepts and should not used
    as a reference for production code. The features are experimental and may not be suitable for
    use in sensitive environments or without additional safeguards and testing.

    Any use of this code is at your own risk.
    """
    query = re.sub(r"^(\s|`)*(?i:python)?\s*", "", query)
    query = re.sub(r"(\s|`)*$", "", query)
    return query


class ValidPythonREPLTool(PythonREPLTool):
    """__init_ receives a function to sanitize and validate the inputs.
    function takes a str as argument and returns a str or throws exception"""
    def __init__(self, sanitize_input: Callable[[str], str] = default_sanitize_input, **kwargs):
        super().__init__(**kwargs)
        self.sanitize_input = sanitize_input

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        self.sanitize_input(query)
        return self.python_repl.run(query)

    async def _arun(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        self.sanitize_input(query)
        return self.python_repl.run(query)
