# OLASan: Object-Level Address Sanitizer

## Overview
OLASan (Object-Level Address Sanitizer) is a memory sanitizer that enhances memory safety in C/C++ applications by focusing on object-level memory access aggregation. This approach reduces runtime overhead while improving detection accuracy, particularly for complex memory violations such as intra-object overflows.

## Table of Contents
- [Getting Started](#getting-started)
- [Setup Instructions](#setup-instructions)
- [Running Tests](#running-tests)
- [Dynamic Profiling](#dynamic-profiling)
- [Running SPEC Benchmarks](#running-spec-benchmarks)
- [Running OLASan on Real CVEs](#running-olasan-on-real-cves)
- [License](#license)
- [Contact](#contact)

## Getting Started
To use OLASan, please follow the instructions below to set up your environment and run tests.

### Setup Instructions

1. **Set Environment Variables for Customized LLVM**  
   Download the OLASanRelease version from [here](https://github.com/040840308-liu/OLASanRelease-Artifact) and save it to a folder.

   ```bash
   export LLVM_HOME=$OLASanRelease_folder/bin:$LLVM_HOME
   export PATH=$OLASanRelease_folder/bin:$PATH

2. **Compile and Run Tests on the Juliet Dataset**
   Set up the Juliet dataset environment:

   ```bash
   export DATASET=Juliet
   export SPECNAME=Juliet

