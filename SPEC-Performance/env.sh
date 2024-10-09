#Must call this with `source env.sh`

#FLOATZONE_MODE is used at compile time to configure the detection
#capabilities:
# - floatzone : enable FloatZone
# - double_sided : include underflow redzone
# - just_size : enable FloatZoneExt

#--- FloatZone ---
export FLOATZONE_MODE="floatzone double_sided"
#--- FloatZoneExt ---
#export FLOATZONE_MODE="floatzone double_sided just_size"

#CHANGME depending on where you cloned the floatzone repo!
export FLOATZONE_TOP=/home/test/workspace-floatzone/floatzone
export MESH_TOP=/home/test/workspace-15/llvm/
export HWASAN_TOP=/home/test/workspace-15/llvm/

export GIANTASAN_TOP=/home/test/GiantSan-Artifact/LLVM-GiantSan/

#ASAN--
export ASANOP_TOP=/home/test/workspace-ASAN--/ASAN---master/llvm-12.0.0-project/
#CHANGME depending on where you installed SPEC
#export FLOATZONE_SPEC06=/home/test/workspace-floatzone/SPEC2006Install/spec2006/

export FLOATZONE_SPEC06=/home/test/workspace-floatzone/floatzone/spec2006/
export FLOATZONE_SPEC17=/home/test/workspace-floatzone/floatzone/spec2017/install/

export FLOATZONE_LLVM=$FLOATZONE_TOP/floatzone-llvm-project/llvm/

export FLOATZONE_LLVM_BUILD=$FLOATZONE_TOP/llvm-floatzone/
export FLOATZONE_C=$FLOATZONE_LLVM_BUILD/bin/clang
export FLOATZONE_CXX=$FLOATZONE_LLVM_BUILD/bin/clang++

export MESH_LLVM_BUILD=$MESH_TOP/build/
export MESH_C=$MESH_LLVM_BUILD/bin/clang
export MESH_CXX=$MESH_LLVM_BUILD/bin/clang++

export HWASAN_LLVM_BUILD=$HWASAN_TOP/build/
export HWASAN_C=$HWASAN_LLVM_BUILD/bin/clang
export HWASAN_CXX=$HWASAN_LLVM_BUILD/bin/clang++

export GIANTASAN_LLVM_BUILD=$GIANTASAN_TOP
export GIANTASAN_C=$GIANTASAN_LLVM_BUILD/bin/clang
export GIANTASAN_CXX=$GIANTASAN_LLVM_BUILD/bin/clang++


export ASANOP_LLVM_BUILD=$ASANOP_TOP/build/
export ASANOP_C=$MESH_LLVM_BUILD/bin/clang
export ASANOP_CXX=$MESH_LLVM_BUILD/bin/clang++


export DEFAULT_LLVM_BUILD=$FLOATZONE_TOP/llvm-default/
#export DEFAULT_LLVM_BUILD=/home/test/workspace-15/llvm/build/
export DEFAULT_C=$DEFAULT_LLVM_BUILD/bin/clang
export DEFAULT_CXX=$DEFAULT_LLVM_BUILD/bin/clang++

export FLOATZONE_XED=$FLOATZONE_TOP/xed/
export FLOATZONE_XED_MBUILD=$FLOATZONE_TOP/mbuild/
export FLOATZONE_XED_LIB=$FLOATZONE_XED/obj/libxed.a
export FLOATZONE_XED_LIB_SO=$FLOATZONE_XED/obj/libxed.so
export FLOATZONE_XED_INC=$FLOATZONE_XED/include/public/xed/
export FLOATZONE_XED_INC_OBJ=$FLOATZONE_XED/obj/

export WRAP_DIR=$FLOATZONE_TOP/runtime/ 
export FLOATZONE_LIBWRAP_SO=$WRAP_DIR/libwrap.so


export FLOATZONE_INFRA=$FLOATZONE_TOP/instrumentation-infra/

export MESH_HEAP_ADDRESS=0x7fff77a2a000
export LLVM_HOME=/home/test/workspace-15/llvm/build/bin:$LLVM_HOME
export PATH=/home/test/workspace-15/llvm/build/bin:$PATH

#Suggested for better benchmarking
#echo "performance" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
#echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
