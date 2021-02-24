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


class Evaluation:
    """
    An abstract class representing a simple evaluation.

    ATTRIBUTES
        success (bool): whether or not the evaluation is successful
        report (str): a plain-language String describing the evaluation
    """

    def __init__(self, success, report):
        """
        Initializes the Evaluation.

        PARAMETERS
            success (bool): whether or not the evaluation is successful
            report (str): a plain-language String describing the evaluation
        """
        self.success = success
        self.report = report


class AssemblyEvaluation(Evaluation):
    """
    An evaluation of a sequence assembly.

    ATTRIBUTES
        n50_evaluation (Evaluation): an evaluation of the assembly's n50
        contigs_evaluation (Evaluation): an evaluation of the assembly's number of contigs
        l50_evaluation (Evaluation): an evaluation of the assembly's l50
        length_evaluation (Evaluation): an evaluation of the assembly's length
    """

    def __init__(self, n50_evaluation, contigs_evaluation, l50_evaluation, length_evaluation, success, report):
        """
        Initializes the AssemblyEvaluation.

        PARAMETERS
            n50_evaluation (Evaluation): an evaluation of the assembly's n50
            contigs_evaluation (Evaluation): an evaluation of the assembly's number of contigs
            l50_evaluation (Evaluation): an evaluation of the assembly's l50
            length_evaluation (Evaluation): an evaluation of the assembly's length
            success (bool): whether or not the evaluation is successful
            report (str): a plain-language String describing the assembly evaluation
        """

        super().__init__(success, report)

        self.n50_evaluation = n50_evaluation
        self.contigs_evaluation = contigs_evaluation
        self.l50_evaluation = l50_evaluation
        self.length_evaluation = length_evaluation
        self.success = success
        self.report = report


class MachineLearningEvaluation(Evaluation):
    """
    An evaluation of an assembly using a machine-learning algorithm.

    ATTRIBUTES
        success (bool): whether or not the evaluation is successful
        report (str): a plain-language String describing the evaluation
        probability (float): the probability of the assembly being a "good" assembly
        species_present (bool): whether or not the species is present in the ML database
    """

    def __init__(self, success, report, probability, species_present):
        """
        Initializes the MachineLearningEvaluation.

        PARAMETERS
           success (bool): whether or not the evaluation is successful
           report (str): a plain-language String describing the evaluation
           probability (float): the probability of the assembly being a "good" assembly
           species_present (bool): whether or not the species is present in the ML database
        """

        super().__init__(success, report)

        self.probability = probability
        self.species_present = species_present
