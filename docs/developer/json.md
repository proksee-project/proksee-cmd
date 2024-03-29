# Assembly Information JSON File

When Proksee assemble completes, a JSON-formatted file describing information about the reads, quality, and assembly is written. The intention of this file is to make the standard output of Proksee Assemble more easily machine-readable, for other applications that use assemblies generated by Proksee Assemble.

The assembly information JSON file is named "assembly_info.json". Please find below an overview of the format and an example output file.

<details>
  <summary>JSON File Format Specification</summary>  
  
```
{
    "Technology": <STRING: The sequencing technology.>,
    "Species":  <STRING: The estimated species.>,
    "Read Quality": {
        "Total Reads":  <INT: The total number of reads.>,
        "Total Bases": <INT: The total number of bases in all reads.>,
        "Q20 Bases": <INT: The total number of bases in all reads with quality score 20 or higher.>,
        "Q20 Rate": <FLOAT: The rate of Q20 bases; what fraction of all bases are at least Q20.>,
        "Q30 Bases": <INT: The total number of bases in all reads with quality score 30 or higher.>,
        "Q30 Rate": <FLOAT: The rate of Q30 bases; what fraction of all bases are at least Q30.>,
        "GC Content": <FLOAT: The GC-content of the reads. Between 0 and 1.>
    },
    "Assembly Quality": {
        "N50": <INT: The N50 of the expert assembly.>,
        "L50": <INT: The L50 of the expert assembly.>,
        "Number of Contigs": <INT: The number of contigs in the expert assembly.>,
        "Assembly Size": <INT: The assembly size of the expert assembly.>
    },
    "Heuristic Evaluation": {
        "Success": <BOOL: Whether or not the expert assembly passed a heuristic evaluation.>,
        "N50 Pass": <BOOL: Whether or not the N50 of the expert assembly passed a heuristic evaluation.>,
        "N50 Report": <STRING: A report on the N50 of the expert assembly.>,
        "Contigs Pass": <BOOL: Whether or not the number of contigs in the expert assembly passed a heuristic evaluation.>,
        "Contigs Report": <STRING: A report on the number of contigs in the expert assembly.>,
        "L50 Pass": <BOOL: Whether or not the L50 of the expert assembly passed a heuristic evaluation.>,
        "L50 Report": <STRING: A report on the L50 of the expert assembly.>,
        "Length Pass": <BOOL: Whether or not the assembly length of the expert assembly passed a heuristic evaluation.>,
        "Length Report": <STRING: A report on the length of the expert assembly.>
    },
    "Machine Learning Evaluation": {
        "Success": <BOOL: Whether or not the expert assembly was evaluated as a success by the machine learning algorithm.>,
        "Probability": <FLOAT: The probability of the expert assembly being a "good" assembly.>,
        "Report": <STRING: A report on the machine learning evaluation of the expert assembly.>
    }
}
```

</details>


<details>
  <summary>Example JSON File</summary>  
  
```
{
    "Technology": "Unidentifiable",
    "Species": "Unknown",
    "Read Quality": {
        "Total Reads": 352355,
        "Total Bases": 35587855,
        "Q20 Bases": 22752475,
        "Q20 Rate": 0.6393325756778542,
        "Q30 Bases": 18288469,
        "Q30 Rate": 0.5138963559337869,
        "GC Content": 0.299302
    },
    "Assembly Quality": {
        "N50": 2824,
        "L50": 298,
        "Number of Contigs": 1323,
        "Assembly Size": 2703272
    },
    "Heuristic Evaluation": {
        "Success": false,
        "N50 Pass": false,
        "N50 Report": "FAIL: The N50 is smaller than expected: 2824\n      The N50 lower bound is: 5000\n",
        "Contigs Pass": true,
        "Contigs Report": "PASS: The number of contigs is acceptable: 1323\n      The number of contigs lower bound is: 5000\n",
        "L50 Pass": true,
        "L50 Report": "PASS: The L50 is acceptable: 298\n      The L50 upper bound is: 500\n",
        "Length Pass": true,
        "Length Report": "PASS: The length is acceptable: 2703272\n      The length lower bound is: 5000\n"
    },
    "Machine Learning Evaluation": {
        "Success": false,
        "Probability": 0.0,
        "Report": "The species is not present in the database."
    }
}
```

</details>
