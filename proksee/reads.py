"""
Copyright Government of Canada 2020

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


class Reads:

    def __init__(self, forward, reverse):
        self.forward = forward
        self.reverse = reverse

    def get_file_locations(self):

        file_list = []

        if self.forward:
            file_list.append(self.forward)

        if self.reverse:
            file_list.append(self.reverse)

        return file_list
