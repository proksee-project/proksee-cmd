"""
Copyright Government of Canada 2022

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


class ResourceSpecification:
    """
    A class representing the resource specifications that sub-programs in the Proksee pipeline should adhere to
    (ex:memory, threads).

    ATTRIBUTES
        threads (int): the number of threads to use
        memory (int): the amount of memory in gigabytes to use
    """

    def __init__(self, threads, memory):
        """
        Initializes the resource specification.

        PARAMETERS
            threads (int): the number of threads to use
            memory (int): the amount of memory in gigabytes to use
        """

        self.threads = threads
        self.memory = memory
