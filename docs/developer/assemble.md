# Assemble

v1.0.0
2021-02-04

The assemble command is responsible for assembling sequencing reads into contigs. It uses an expert system to guide decision-making through the various stages of assembly.

## Pipeline

![overview](images/overview.png)

The assemble pipeline consists of three major stages:

- **Stage 1: Pre-Assembly**: Attempts to estimate information about the reads and prepares the reads for sequence assembly.
- **Stage 2: Fast Assembly**: Assembles the reads hastily in order to derive more information for expert assembly.
- **Stage 3: Expert Assembly**: Assembles the reads in an expert manner using information gathered during the previous stages.

## Pre-Assembly

![pre-assembly](images/pre_assembly.png)

The pre-assembly stage is responsible for estimating information about the reads, including the species and sequencing technology, and preparing the reads for sequence assembly.

### Validate Inputs

The forward and reverse read inputs are validated in order to ensure that they are in valid FASTQ format. The pipeline will terminate if the inputs appear to be formatted incorrectly.

### Identify Sequencing Platform

The sequencing platform is estimated by looking at the encoding of the FASTQ input reads. If there is not enough information to estimate the sequencing platform, then the platform will be unidentifiable, but assembly will continue. This stage is skipped if the user provides the sequencing platform as a command-line argument.

### Filter Reads

The reads are filtered in order to remove low-quality sequencing content and improve the assembly. FASTP is used to filter the reads.

### Determine Read Quality

The read quality is determined from the filtered reads by parsing the output of FASTP in the previous step. Since FASTP provides some quality metrics of the reads after filtering, this information is parsed into the pipeline and used in later steps.

### Estimate Species

Attempts to estimate the species using MASH. Since MASH is not designed to be a classifier, we shouldn't say that the species is *classified*, but rather the species is *estimated* from  *k*-mer information in the reads. MASH output can be messy on real-world data and will often report multiple species present in the data. High thresholds are therefore used in order to only report species that are very likely to be present. As a consequence of this approach, we cannot confidently make claims about low levels of contamination in the reads and thus ignore contamination.

## Fast Assembly

![fast assembly](images/fast_assembly.png)

The fast assembly stage assembles the reads hastily in order to gather some approximate structural information that can be seen after assembling reads into contigs. It should provide the pipeline with more accurate information about which major species are present, approximately how large the assembly will be, and if there is any major contamination present.

### Create Strategy

Creates a fast assembly strategy for assembly using the information gathered during the pre-assembly stage. The sequencing platform, estimated species, and read quality are provided to the expert system, which creates a fast assembly strategy using this information.

It is possible that the expert system will decide that the best course of action is to terminate the pipeline because the provided information suggests no good assemble can be produced. This might happen if the read quality after filtering remains too low, or if there are too many major species present in the reads, suggesting major contamination.

### Assemble

Assembles the reads by executing the fast assembly strategy. Currently, this will always involve using SKESA. However, it is possible to expand this in the future.

### Evaluate Contamination

Evaluates possible contamination in the assembled reads. This is achieved using MASH to ensure that the five largest assembled contigs are estimated to have the same major species as the initial pipeline species estimation. This will not identify minor or medium levels of contamination, but should identify major levels of species contamination in the contigs.

The pipeline will terminate if there is a disagreement in the species estimations.

### Evaluate Assembly

Evaluates the assembly using QUAST. The pipeline uses a non-reference-based QUAST analysis, because of the difficulty of selecting a reference correctly and needing to maintain either a database of references or the ability to download references on the fly. Several assembly metrics are collected, including N50, number of contigs, L50, and total assembly size.

## Expert Assembly

![expert assembly](images/expert_assembly.png)

The expert assembly stage uses information collected in the pre-assembly and fast assembly stages to create an expert strategy for assembling the reads. The assembly generated in this stage should be higher quality than the assembly created in the fast assembly stage.

### Create Stategy

Creates a strategy using the expert system by analyzing the assembly metrics of the fast assembly (N50, L50, number of contigs, assembly length). The fast assembly metrics are compared against the sequence assembly database to see if the assembly metrics agree with what would be expect for the species. If these assembly metrics are in major disagreement with what would be expected for the species, then the pipeline is terminated.

### Assemble

Assembles the reads by executing the expert assembly strategy. Currently, this will always involve using SPAdes. However, it is possible to expand this in the future.

### Evaluate Assembly

Evaluates the assembly using QUAST, in the same manner as previously done in the fast assembly stage. The QUAST analysis is done without a reference, because of the difficulties of regularly selecting a good reference.

### Compare Assemblies

Compares all assembly metrics of all assemblies run in the pipeline (fast, expert) and reports them. These assembly metrics include N50, L50, number of contigs, and assembly length.

# Data Structures

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

An abstract class used to evaluatee the quality of assembles. The .evaluate() function, which returns an Evaluation object, is used to evaluate the assemblies and must be implemented by classes implementing this abstract class. Currently, HeuristicEvaluator and MachineLearningEvaluator implement this abstract class.

## AssemblyQuality

*assembly_quality.py*

Encapsulates many assembly statistic measurements (ex: N50, L50, number of contigs, assembly length) into a single object to facilitate passing this information around the pipeline much easier.

## AssemblyStrategy

*assembly_strategy.py*

Encapsulates information about an assembly stategy to follow, including whether or not to proceed with the strategy, a plain-language report to provide the user about the strategy, and the assembler to use for assembly. The assembler object should be proconfigured with all necessary parameters, such that only .assemble() needs to be called to perform the determined assembly.

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

The PlatformIdentifier class is attempts to identify the sequencing platform that was used to sequence the reads. This is accomplished by looking at the FASTQ file encoding and seeing if any of the information can be used to uniquely identify a sequencing platform. However, this process is not always successful and sometimes the platform will be declared as "Unidentifiable".

## ReadFilterer

*read_filterer.py*

Filters the reads using FASTP. The object encapsulates information about the input reads, and several ouput files created by running FASTP.

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

Encapsulates a single "estimation" of a species. In particular, it is designed to encapsulate an estimation from RefSeq Masher into a single onject that can be passed and operated on more easily.

## SpeciesEstimator

*species_estimator.py*

The SpeciesEstimator represents a tool used to estimate species from either sequencing reads or contigs. It is not designed to be a species classifier, but rather simply estimate the species, based on the information on hand (in particular, the RefSeq Masher database).
