Overview
Welcome to the OLASan project! This README guide will walk you through setting up the environment and running our tool for dynamic profiling and detecting memory errors.

Table of Contents
Introduction
Setup Customized LLVM Environment
Compile and Run Tests on Juliet
Dynamic Profiling
Run SPEC Benchmarks
Run OLASan on Real CVEs
License
Contributing
Introduction
This repository contains tools and configurations for dynamic profiling and memory safety analysis using our custom LLVM-based sanitizer. It includes instructions for setting up the environment, compiling and running tests, and performing dynamic profiling on real-world CVE cases.

Setup Customized LLVM Environment
Download OLASan Release Version
Download the OLASan Release version from here.
Save it to a folder of your choice.
Set Environment Variables
Set the environment variables to use the custom LLVM installation.
bash
export LLVM_HOME=$OLASanRelease_folder/bin:$LLVM_HOME
export PATH=$OLASanRelease_folder/bin:$PATH
Compile and Run Tests on Juliet
Set Environment Variables
Set the necessary environment variables.
bash
export DATASET=Juliet
export SPECNAME=Juliet
Navigate to the Juliet Folder
Change into the Juliet folder.
bash
cd $Path/OLASan-Artifact/Juliet/testcases/CWE121_Stack_Based_Buffer_Overflow/s09/
Compile All Programs
Compile all the programs within the folder.
bash
make individuals
Run Programs in Batch
Set the directory variable in batch_run.py.
bash
深色版本
dir="$Path/OLASan-Artifact/Juliet/testcases/CWE121_Stack_Based_Buffer_Overflow/s09/"
Run the batch script.
bash
深色版本
python3 batch_run.py
View Detection Results
The detection results can be found in output.txt within the folder $Path/OLASan-Artifact/Juliet/testcases/CWE121_Stack_Based_Buffer_Overflow/s09/.
Note: CWE121_Stack_Based_Buffer_Overflow/s09/ includes intra-object overflow examples, which all ASan, ASan--, HWASan, and GiantSan fail to detect.
Dynamic Profiling
Download Profile Release Version of LLVM
Download the Profile Release version of LLVM from here.
Save it to a folder of your choice.
Set Environment Variables
Set the environment variables to use the profiling LLVM installation.
bash
深色版本
export LLVM_HOME=$ProfileRelease-LLVM/build/bin:$LLVM_HOME
export PATH=$ProfileRelease-LLVM/build/bin:$PATH
Create Profiling Folder
Create a folder to store profiling results.
bash
深色版本
mkdir /home/test/ProfileFolder/
Run Programs with Unit Tests
Run the programs with unit tests (workload).
The profiling results will be output to the folder /home/test/ProfileFolder/.
More Details: See the section on CVE real case analysis for more information on how to perform profiling.
Run SPEC Benchmarks
We use instrumentation-infra to run SPEC benchmarks with our LLVM compiler. Configuration files are also provided.

Install Dependencies
Install necessary dependencies.
bash
深色版本
sudo apt install ninja-build cmake gcc-9 autoconf2.69 bison build-essential flex texinfo libtool zlib1g-dev
pip3 install psutil terminaltables
Install Required Tools
Clone and checkout the required versions of tools.
bash
深色版本
git clone https://github.com/vusec/floatzone.git
cd floatzone
git checkout 9fc12ab
Run SPEC Benchmarks
Run individual SPEC 2006 or SPEC 2017 benchmarks.
bash
深色版本
python3 run-new.py run spec2006 default_O2 asan_O2 hwasan_O2--build --parallel=proc --parallelmax=1 --benchmarks 453.povray
python3 run-new.py run spec2017 default_O2 asan_O2 hwasan_O2 --build --parallel=proc --parallelmax=1 --benchmarks 500.perlbench_r
Run all SPEC 2006 or SPEC 2017 benchmarks.
bash
深色版本
python3 run-new.py run spec2006 default_O2 asan_O2 hwasan_O2 --build --parallel=proc --parallelmax=1
python3 run-new.py run spec2017 default_O2 asan_O2 hwasan_O2 --build --parallel=proc --parallelmax=1
Note: default_O2 refers to running SPEC with original LLVM, asan_O2 refers to running SPEC with AddressSanitizer, and hwasan_O2 refers to running SPEC with our enabled HWAddressSanitizer on x86_64.
Compute Time and Memory Overhead
To compute the respective time and memory overhead:
bash
深色版本
python3 run-new.py report spec2006 results/run.2023-06-20.15-37-32/ --aggregate geomean --field runtime:median maxrss:median
python3 run-new.py report spec2017 results/run.2023-06-20.15-37-32/ --aggregate geomean --field runtime:median maxrss:median
Run OLASan on Real CVEs
Taking Libtiff (CVE-2016-10271) as an example, we can easily download its test inputs from here, which is the latest archive of test images used by the Libtiff library.

Profile Phase
Set environment variables.
bash
深色版本
export DATASET=CVE
export SPECNAME=CVE
export PROFILING=YES
Build the profiled version of Libtiff in the CVE-2016-10271 folder.
bash
深色版本
run ./build-profile.sh
Run Libtiff with several test .tif inputs.
bash
深色版本
libtiff/tools/tiffcrop -i ./libtiffpic/caspian.tif /tmp/foo
libtiff/tools/tiffcrop -i ./libtiffpic/cramps.tif /tmp/foo
libtiff/tools/tiffcrop -i ./libtiffpic/dscf0013.tif /tmp/foo
libtiff/tools/tiffcrop -i ./libtiffpic/fax2d.tif /tmp/foo
libtiff/tools/tiffcrop -i ./libtiffpic/g3test.tif /tmp/foo
libtiff/tools/tiffcrop -i ./libtiffpic/jello.tif /tmp/foo
libtiff/tools/tiffcrop -i ./libtiffpic/oxford.tif /tmp/foo
libtiff/tools/tiffcrop -i ./libtiffpic/pc260001.tif /tmp/foo
libtiff/tools/tiffcrop -i ./libtiffpic/quad-lzw.tif /tmp/foo
Analyze the profiling logs using Python scripts and output the final profiling results.
bash
深色版本
python3 pattern_mine.py
Save the final results with the name libtiff10271 to the folder /home/test/ProfileResults/.
Sanitization Phase
Set environment variables.
bash
深色版本
export PROFILING=No
export PROFILERESULTS=/home/test/ProfileResults/
export SPECNAME=libtiff10271
Build the sanitized version of Libtiff in the CVE-2016-10271 folder.
bash
深色版本
run ./build.sh
Run Libtiff with PoC input.
bash
深色版本
libtiff/tools/tiffcrop -i ./00100-libtiff-heapoverflow-_TIFFFax3fillruns /tmp/foo
Heap overflow should be detected, and the details will be output.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
Contributions are welcome! Please read our CONTRIBUTING guidelines before contributing.
