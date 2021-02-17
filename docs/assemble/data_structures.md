# Proksee Assemble Data Structures

v1.0.0
2021-02-04

The following is a high-level overview of some of the data structures used in the pipeline.

## Assembler

*assembler.py, skesa_assembler.py, spades_assembler.py*

The Assembler class is an abstract base class and, importantly, is returned as part of the AssemblyStrategy object. Functions that use the Assembler class don't need to worry about the specific assembler implemented, but rather can just invoke the .assemble() method. This should allow for easier incorporation of other assemblers in the future.

The Assembler class is currently implemented by the SpadesAssembler and SkesaAssembler classes.

## AssemblyDatabase

*assembly_database.py*

The AssemblyDatabase class serves as an object wrapper for the assembly database file. It provides functions for interacting with the database file without the caller needing to worry about the specific implementation.

Currently, the class loads a CSV file where assembly metrics are organized by species.

## AssemblyEvaluator

*assembly_evaluator.py, heuristic_evaluation.py, machine_learning_evaluator.py*

An abstract class used to evaluate the quality of assembles. The .evaluate() function, which returns an Evaluation object, is used to evaluate the assemblies and must be implemented by classes implementing this abstract class. Currently, HeuristicEvaluator and MachineLearningEvaluator implement this abstract class.

## AssemblyQuality

*assembly_quality.py*

Encapsulates many assembly statistic measurements (ex: N50, L50, number of contigs, assembly length) into a single object to facilitate passing this information around the pipeline much easier.

## AssemblyStrategy

*assembly_strategy.py*

Encapsulates information about an assembly strategy to follow, including whether or not to proceed with the strategy, a plain-language report to provide the user about the strategy, and the assembler to use for assembly. The assembler object should be proconfigured with all necessary parameters, such that only .assemble() needs to be called to perform the determined assembly.

## ContaminationHandler

*contamination_handler.py*

Identifies, filters and otherwise handles contamination in assembled contigs. In particular, it's responsible for estimating contamination in the contigs, using MASH, and checking to see that the species estimated in individual contigs agrees with the species estimated for the entire read set. As contamination handling is very difficult and resource intense, this heuristic approach should help catch some of the worse cases of contamination in the assembled contig data.

## Evaluation

*evaluation.py*

A simple, generic class representing an evaluation. It encapsulates two attributes: success (whether or not the subject was evaluated positively or negatively) and report (a plain-language text report explaining the evaluation). This class functions as a way to return a boolean from a test / evaluation / check alongside an explanation of the result. Evaluation is extended by AssemblyEvaluation, which contains more specific attributes for sequence assembly statistic evaluations.

## ExpertSystem

*expert_system.py*

The ExpertSystem class represents a system for evaluating read data or assembly data in order to make decisions about how best to perform sequence assembly. It is principally responsible for creating AssemblyStrategy objects, which contain an Assembler object that can be used to perform an assembly.

## PlatformIdentifier

*platform_identify.py*

The PlatformIdentifier class attempts to identify the sequencing platform that was used to sequence the reads. This is accomplished by looking at the FASTQ file encoding and seeing if any of the information can be used to uniquely identify a sequencing platform. However, this process is not always successful and sometimes the platform will be declared as "Unidentifiable".

## ReadFilterer

*read_filterer.py*

Filters the reads using FASTP. The object encapsulates information about the input reads, and several output files created by running FASTP.

## ReadQuality

*read_quality.py*

The ReadQuality object encapsulates information about the quality of reads. It includes measures such as the number of reads, the rate of Q30 or higher bases, and the GC-content.

## Reads

*reads.py*

Encapsulates sequencing reads into a single object. This simplifies the need to pass forward and optionally reverse reads and accommodates a future possibility of having more than two read sets.

## Species

*species.py*

Represents a biological species. The name attribute should exactly match the scientific name for the species (including capitalization). The confidence attribute relates to the confidence of the species assignment, which may be derived from species estimation tools, such as MASH.

## SpeciesEstimation

*species_estimation.py*

Encapsulates a single "estimation" of a species. In particular, it is designed to encapsulate an estimation from RefSeq Masher into a single object that can be passed and operated on more easily.

## SpeciesEstimator

*species_estimator.py*

The SpeciesEstimator represents a tool used to estimate species from either sequencing reads or contigs. It is not designed to be a species classifier, but rather simply estimate the species, based on the information on hand (in particular, the RefSeq Masher database).
