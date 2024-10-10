# OLASan: Object-Level Address Sanitizer

## Overview
OLASan (Object-Level Address Sanitizer) is a memory sanitizer that enhances memory safety in C/C++ applications by focusing on object-level memory access aggregation. This approach reduces runtime overhead while improving detection accuracy, particularly for complex memory violations such as intra-object overflows.

## Table of Contents
- [Getting Started](#getting-started)
- [Setup Instructions](#setup-instructions)
- [Running Juliet Tests](#running-juliet-tests)
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

   cd $Path/OLASan-Artifact/Juliet/testcases/CWE121_Stack_Based_Buffer_Overflow/s09/ in Juliet Folder
   
   #compile all programs
   
   make individuals;

   #run programs in batch
   
   #set dir="$Path/OLASan-Artifact/Juliet/testcases/CWE121_Stack_Based_Buffer_Overflow/s09/" in batch_run.py

   python3 batch_run.py

   #The detected results can be found in output.txt from Folder:
   
   $Path/OLASan-Artifact/Juliet/testcases/CWE121_Stack_Based_Buffer_Overflow/s09/
   
   #Note:CWE121_Stack_Based_Buffer_Overflow/s09/ include intra-object overflow examples, which all ASan, ASan--, HWASan and GiantSan fails to detect.

4. **Dynamic Profiling**

   Download ProfileRelease version llvm [here](https://github.com/040840308-liu/ProfileRelease-LLVM) and save to a folder

   #set environment variables to use profiling llvm

   ```bash
   export LLVM_HOME=$ProfileRelease-LLVM/build/bin:$LLVM_HOME
   export PATH=$ProfileRelease-LLVM/build/bin:$PATH
   mkdir /home/test/ProfileFolder/

   #Run programs with unittests (workload)
   
   And the profiling results will output to folder /home/test/ProfileFolder/.
   
   More details about how to do profiling, please see below CVE real case analysis.

5. **Run SPEC**
   
   #We adopt instrumentation-infra to run SPEC with our llvm, we also uploaded our config files.

   #First is to install xed@9fc12ab, instrumentation-infra@5bfbf68, mbuild@75cb46e, (or refer the install steps from https://github.com/vusec/floatzone).

   ```bash
   sudo apt install ninja-build cmake gcc-9 autoconf2.69 bison build-essential flex texinfo libtool zlib1g-dev

   pip3 install psutil terminaltables

   export DATASET=SPEC

   #1). run invidiual spec2006 or spec2017 benchmark with following command:

   python3 run-new.py run spec2006 default_O2 asan_O2 hwasan_O2--build --parallel=proc --parallelmax=1 --benchmarks 453.povray

   python3 run-new.py run spec2017 default_O2 asan_O2 hwasan_O2 --build --parallel=proc --parallelmax=1 --benchmarks 500.perlbench_r

   #2). run all spec2006 or spec2017 benchmark with following command:

   python3 run-new.py run spec2006 default_O2 asan_O2 hwasan_O2 --build --parallel=proc --parallelmax=1

   python3 run-new.py run spec2017 default_O2 asan_O2 hwasan_O2 --build --parallel=proc --parallelmax=1

   #Note here, default_O2 refers to run SPEC with origin LLVM, asan_O2 refers to run SPEC with AddressSanitizer, hwasan_O2 refers to run SPEC with our enable HWAddressSanitizer on x86_64.

   #To compute the respective time and memory overhead do: (substitute run.2023-06-20.15-37-32/ with your result folder)

   python3 run-new.py report spec2006 results/run.2023-06-20.15-37-32/ --aggregate geomean --field runtime:median maxrss:median or

   python3 run-new.py report spec2017 results/run.2023-06-20.15-37-32/ --aggregate geomean --field runtime:median maxrss:median or

6. **Run OLASan on real CVEs**
   
   #Take Libtiff (CVE-2016-10271) as an example, we could easily download its test inputs from https://download.osgeo.org/libtiff/pics-3.8.0.tar.gz., where the latest archive of test images used by Libtiff library.

   #1). First is Profile phrase

   #set environment variables

   ```bash
   export DATASET=CVE
   export SPECNAME=CVE
   export PROFILING=YES

   run ./build-profile.sh in CVE-2016-10271 folder to build profiled-version libtiff

   #then run libtiff with several test .tif inputs

   libtiff/tools//tiffcrop -i ./libtiffpic/caspian.tif /tmp/foo
   libtiff/tools//tiffcrop -i ./libtiffpic/cramps.tif /tmp/foo
   libtiff/tools//tiffcrop -i ./libtiffpic/dscf0013.tif /tmp/foo
   libtiff/tools//tiffcrop -i ./libtiffpic/fax2d.tif /tmp/foo
   libtiff/tools//tiffcrop -i ./libtiffpic/g3test.tif /tmp/foo
   libtiff/tools//tiffcrop -i ./libtiffpic/jello.tif /tmp/foo
   libtiff/tools//tiffcrop -i ./libtiffpic/oxford.tif /tmp/foo
   libtiff/tools//tiffcrop -i ./libtiffpic/pc260001.tif /tmp/foo
   libtiff/tools//tiffcrop -i ./libtiffpic/quad-lzw.tif /tmp/foo

   #The collected profiling logs have been uploaded

   run python scripts pattern_mine to analyze these profiling logs and output the final profiling results.

   #save the final results with name libtiff10271 to folder /home/test/ProfileResults/

   #2). Second is sanitization phrase

   #set environment variables

   export PROFILING=No

   export PROFILERESULTS=/home/test/ProfileResults/

   export SPECNAME=libtiff10271

   run ./build.sh in CVE-2016-10271 folder to build sanitized-version libtiff

   #then run libtiff with poc: libtiff/tools//tiffcrop -i ./00100-libtiff-heapoverflow-_TIFFFax3fillruns /tmp/foo

   #Heap overflow could be detected, the details are also output.
