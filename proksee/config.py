"""
Copyright Government of Canada 2021

Written by:

Eric Marinier
    National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import os
import json

from pathlib import Path

CONFIG_FILENAME = os.path.join(Path(__file__).parent.absolute(), "config", "config.json")
MASH_PATH = "mashPath"


def update(key, value):
    """
    Updates the Proksee config file with the passed (key, value).

    POST: The config file will be updated, such that the passed 'value', will be assigned to 'key'.
    """

    with open(CONFIG_FILENAME, 'r') as f:
        config = json.load(f)

    config[key] = value

    with open(CONFIG_FILENAME, 'w') as f:
        json.dump(config, f, indent=4)


def get(key):
    """
    Gets the value stored in the config file for 'key'.

    RETURNS
        value (string): the value stored in the config file for 'key'
    """

    with open(CONFIG_FILENAME, 'r') as f:
        config = json.load(f)

    value = config[key]

    return value
