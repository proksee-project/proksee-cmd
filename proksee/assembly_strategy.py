"""
Copyright Government of Canada 2020

Written by: Eric Marinier, National Microbiology Laboratory,
            Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""


class AssemblyStrategy:
    """
    This class represents the strategy for an assembly to follow.

    ATTRIBUTES
        proceed (bool): whether or not to proceed with assembly
        report (str): a plain-language report of the assembly strategy
    """

    def __init__(self, proceed, report):
        """
        Initialize the AssemblyStrategy object.

        PARAMETERS
            proceed(bool): whether or not to proceed with assembly
            report (str): a plain-language report of the assembly strategy
        """

        self.proceed = proceed
        self.report = report
