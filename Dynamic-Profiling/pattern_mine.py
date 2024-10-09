import os
import re
from collections import defaultdict



"""def parse_line(line):
    
    解析单行内容，返回文件名、行号和地址。
    
    match = re.match(r'(\w+\.c)\|(\d+)\|0x([0-9a-fA-F]+)\|Malloc', line)
    if match:
        filename, lineno, address = match.groups()
        return filename, int(lineno), address
    return None, None, None"""

def parse_line(line): #for malloc, free
    """
    将单行数据按竖线|分割成四部分，并返回文件名、行号、地址和操作的元组。
    如果行格式不正确，返回None。
    """
    parts = line.split('|')
    if len(parts) ==5:
        filename = parts[0]  # 文件名
        lineno = int(parts[1])  # 行号
        address = parts[2]  # 地址
        operation = parts[4]  # 操作（如Malloc）
        return filename, lineno, address, operation
    else:
        return None, None, None, None

def parse_line1(line): #for memory access
    """
    将单行数据按竖线|分割成四部分，并返回文件名、行号、地址和操作的元组。
    如果行格式不正确，返回None。
    """
    parts = line.split('|')
    if len(parts) == 10:
        filename = parts[0]  # 文件名
        lineno = int(parts[1])  # 行号
        address = parts[2]  # 地址
        base = parts[3]  # 地址
        offset = parts[4]  # 操作（如Malloc）
        return filename, lineno, base, offset
    else:
        return None, None, None, None

def process_file(file_path, first_file, global_allocation_id, memory_allocations, memory_access_pattern, memory_access_pattern1):
    """
    处理单个文件，解析内容并更新全局map。
    """
    #global global_allocation_id

    allocation_ID = defaultdict(dict) #ID:addr
    #print(file_path)
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            #filename = os.path.basename(file_path)
            # label allocation ID
            if "../include/c++" in line:
                continue
            if "Malloc" in line or "Free" in line:
                result = parse_line(line)
                if result:
                    filename, lineno, address, operation = result
                    if filename==None or lineno==None or address==None or operation==None:
                        continue
                    allocation_key = f"{filename}+{lineno}"
                    if allocation_key not in memory_allocations:
                        #print(line)
                        memory_allocations[allocation_key] =global_allocation_id
                        global_allocation_id += 1
                    allocation_ID[address] = memory_allocations[allocation_key]
            elif "1111" in line:
                result = parse_line1(line)
                if result:
                    filename, lineno, base, offset = result
                    if filename==None or lineno==None or base==None or offset==None:
                        continue
                    access_key = f"{filename}+{lineno}"
                    if base not in memory_access_pattern1:
                        memory_access_pattern1[base] = {
                            'accesses': {
                                access_key: offset
                            }
                        }
                    else:
                        memory_access_pattern1[base]['accesses'][access_key] = offset
            else:
                result = parse_line1(line)
                #print(line)
                if result:
                    #print(result)
                    filename, lineno, base, offset = result
                    if filename==None or lineno==None or base==None or offset==None:
                        continue
                    #print(base)
                    if not base in allocation_ID:
                        continue
                    TempID = allocation_ID[base]
                    #print(TempID)
                    access_key = f"{filename}+{lineno}"
                    #print(access_key)
                    if first_file:
                        if access_key not in memory_access_pattern:
                            memory_access_pattern[access_key] = {
                                'invariant': False,
                                'ids': [TempID],
                                'accesses':{
                                    TempID:[offset]
                                }
                            }
                        else:
                            if TempID not in memory_access_pattern[access_key]['ids']:
                                memory_access_pattern[access_key]['accesses'][TempID] = [offset]
                                memory_access_pattern[access_key]['ids'].append(TempID)

                            if offset not in memory_access_pattern[access_key]['accesses'][TempID]:
                                memory_access_pattern[access_key]['accesses'][TempID].append(offset)
                    else:#not the first_file,
                        if access_key not in memory_access_pattern:
                            memory_access_pattern[access_key] = {
                                'invariant': False,
                                'ids': [TempID],
                                'accesses': {
                                    TempID: [offset]
                                }
                            }
                        else:
                            if TempID not in memory_access_pattern[access_key]['ids']:
                                memory_access_pattern[access_key]['accesses'][TempID] = [offset]
                                memory_access_pattern[access_key]['ids'].append(TempID)
                            if offset not in memory_access_pattern[access_key]['accesses'][TempID]:
                                memory_access_pattern[access_key]['invariant'] = True
                                memory_access_pattern[access_key]['accesses'][TempID].append(offset)
    return
def list_files_in_directory(directory, filecasename):
    """
    遍历指定目录中的所有文件并打印它们的名称。
    """
    first_file = True
    # 全局内存分配ID，从1开始递增
    global_allocation_id = 1

    # 全局map，用于存储内存分配信息
    memory_allocations = defaultdict(dict)  # filename+line : ID
    memory_access_pattern1 = defaultdict(dict)  # filename+line : {base: , offset:[]}
    memory_access_pattern = defaultdict(dict)  # filename+line : {invariant:bool, ID:v, value:[]}
    for root, dirs, files in os.walk(directory):

        for file in files:
            print(file)
            if filecasename in file:
                print(file)
                file_path = os.path.join(root, file)
                process_file(file_path, first_file, global_allocation_id, memory_allocations, memory_access_pattern, memory_access_pattern1)
                if first_file:
                    first_file = False

    return memory_allocations, memory_access_pattern, memory_access_pattern1


def optimizeInstrumentation(filecase, filecasename):
    directory_path = "../logs"
    memory_allocations, memory_access_pattern, memory_access_pattern1 = list_files_in_directory(directory_path, filecasename)

    object_access_pattern = defaultdict(dict)  # Id: {access: filename+line, offset: v}

    original_instrumentation = []
    optimize_instrumentation = []
    optimize_instrumentation_by_func = []
    # 打印内存分配信息
    for allocation_key, allocation_info in memory_allocations.items():
        print(f"Key: {allocation_key}, ID: {memory_allocations[allocation_key]}")

    for access_key, access_info in memory_access_pattern.items():
        if access_key not in original_instrumentation:
            original_instrumentation.append(access_key)
        ids = access_info['ids']
        print(f"Key: {access_key}, invariant: {access_info['invariant']}, ids: {access_info['ids']}")
        for id in ids:
            if id not in object_access_pattern:
                object_access_pattern[id] = defaultdict(dict)
                object_access_pattern[id][access_key] = access_info['accesses'][id]  # offsets
            else:
                if access_key not in object_access_pattern[id]:
                    object_access_pattern[id][access_key] = access_info['accesses'][id]  # offsets
                else:
                    for offset in access_info['accesses'][id]:
                        if offset not in object_access_pattern[id][access_key]:
                            object_access_pattern[id][access_key].append(offset)  # offsets

    # print(memory_access_pattern)

    print("The number of Original Instrumention is %d!" % len(original_instrumentation))
    print("Start to Optimize Instrumention!*********************************************")

    # print(object_access_pattern)

    optimize_instrumentation_code = defaultdict(dict)
    optimize_instrumentation_code_func = defaultdict(dict)
    for access_id, access_info in object_access_pattern.items():
        max = 0
        max_access_key = ""
        min = 1000000000000
        min_access_key = ""

        optimize_instrumentation_code[access_id] = {"max": "", "min": ""}
        optimize_instrumentation_code_func[access_id] = {}
        for access_key, access_offset in object_access_pattern[access_id].items():
            print(access_key)
            parts = access_key.split('+')
            if 'c++' in access_key:
                # print(len(parts))
                # print(parts[3])
                assert len(parts) == 5
                funcname = parts[3]
            else:
                assert len(parts) == 3
                funcname = parts[1]
            # if not funcname in func_max_min:
            # func_max_min[funcname] = {"max": "", "min": "", "max_access_key":"", "min_access_key":""}
            if not funcname in optimize_instrumentation_code_func[access_id]:
                optimize_instrumentation_code_func[access_id][funcname] = {"max": 0, "min": 1000000000000,
                                                                           "max_access_key": "", "min_access_key": ""}
            for offset in object_access_pattern[access_id][access_key]:
                if int(offset) > max:
                    max = int(offset)
                    max_access_key = access_key
                if int(offset) < min:
                    min = int(offset)
                    min_access_key = access_key

                if int(offset) > optimize_instrumentation_code_func[access_id][funcname]["max"]:
                    optimize_instrumentation_code_func[access_id][funcname]["max"] = int(offset)
                    optimize_instrumentation_code_func[access_id][funcname]["max_access_key"] = access_key
                if int(offset) < optimize_instrumentation_code_func[access_id][funcname]["min"]:
                    optimize_instrumentation_code_func[access_id][funcname]["min"] = int(offset)
                    optimize_instrumentation_code_func[access_id][funcname]["min_access_key"] = access_key

        if max_access_key not in optimize_instrumentation:
            optimize_instrumentation.append(max_access_key)
        if min_access_key not in optimize_instrumentation:
            optimize_instrumentation.append(min_access_key)
        optimize_instrumentation_code[access_id]["max"] = max_access_key
        optimize_instrumentation_code[access_id]["min"] = min_access_key

    optimize_instrumentation_code_func_new = defaultdict(dict)
    for access_base, access_info in memory_access_pattern1.items():
        print(access_base)
        accesses = access_info['accesses']
        optimize_instrumentation_code_func_new[access_base] = {}
        max = 0
        max_access_key = ""
        min = 1000000000000
        min_access_key = ""
        for access_key, offset in accesses.items():
            if access_key not in original_instrumentation:
                original_instrumentation.append(access_key)
                print(f"Key: {access_key}, offset: {offset}")
            parts = access_key.split('+')
            if 'c++' in access_key:
                # print(len(parts))
                # print(parts[3])
                assert len(parts) == 5
                funcname = parts[3]
            else:
                assert len(parts) == 3
                funcname = parts[1]

            if not funcname in optimize_instrumentation_code_func_new[access_base]:
                optimize_instrumentation_code_func_new[access_base][funcname] = {"max": 0, "min": 1000000000000,
                                                                                 "max_access_key": "",
                                                                                 "min_access_key": ""}

            if int(offset) > max:
                max = int(offset)
                max_access_key = access_key
            if int(offset) < min:
                min = int(offset)
                min_access_key = access_key

            if int(offset) > optimize_instrumentation_code_func_new[access_base][funcname]["max"]:
                optimize_instrumentation_code_func_new[access_base][funcname]["max"] = int(offset)
                optimize_instrumentation_code_func_new[access_base][funcname]["max_access_key"] = access_key
            if int(offset) < optimize_instrumentation_code_func_new[access_base][funcname]["min"]:
                optimize_instrumentation_code_func_new[access_base][funcname]["min"] = int(offset)
                optimize_instrumentation_code_func_new[access_base][funcname]["min_access_key"] = access_key

        if max_access_key not in optimize_instrumentation_by_func:
            optimize_instrumentation_by_func.append(max_access_key)
        if min_access_key not in optimize_instrumentation_by_func:
            optimize_instrumentation_by_func.append(min_access_key)

    print("End Optimize Instrumention!*********************************************")

    #print("The number of Optimized Instrumention is %d!" % len(optimize_instrumentation))
    #print(optimize_instrumentation)
    #print(optimize_instrumentation_code)

    for access_id, access_info in optimize_instrumentation_code_func.items():
        for func, info1 in optimize_instrumentation_code_func[access_id].items():
            if optimize_instrumentation_code_func[access_id][func]["max_access_key"] not in optimize_instrumentation_by_func:
                optimize_instrumentation_by_func.append(optimize_instrumentation_code_func[access_id][func]["max_access_key"]) #max_access_key is: file+line
            if optimize_instrumentation_code_func[access_id][func]["min_access_key"] not in optimize_instrumentation_by_func:
                optimize_instrumentation_by_func.append(optimize_instrumentation_code_func[access_id][func]["min_access_key"])

    print(optimize_instrumentation_code_func)

    print(len(optimize_instrumentation_by_func))

    """optimize_instrumentation_results = "../results/optimize_instrumentation_results-"+filecasename +".txt"
    f =open(optimize_instrumentation_results,'w')

    for instrumentation in original_instrumentation:
        if instrumentation in optimize_instrumentation:
            f.write(instrumentation+"+Instrumented")
            f.write("\n")
        else:
            f.write(instrumentation + "+UnInstrumented")
            f.write("\n")
    f.close()

    optimize_instrumentation_results_byfunc = "../results/optimize_instrumentation_results_byfunc-"+filecasename+".txt"

    f =open(optimize_instrumentation_results_byfunc,'w')

    for instrumentation in original_instrumentation:
        if instrumentation in optimize_instrumentation_by_func:
            f.write(instrumentation+"+Instrumented")
            f.write("\n")
        else:
            f.write(instrumentation + "+UnInstrumented")
            f.write("\n")
    f.close()"""

    optimize_instrumentation_results_profile = "../results/" + filecasename + ".txt"
    f = open(optimize_instrumentation_results_profile, 'w')
    for instrumentation in original_instrumentation:
        if instrumentation in optimize_instrumentation_by_func:
            f.write(instrumentation+"+Instrumented")
            f.write("\n")
        else:
            f.write(instrumentation + "+UnInstrumented")
            f.write("\n")
    f.close()

# This is main function;
if __name__=="__main__":
    #cases = [401, 429, 433, 444, 445, 450, 453, 456, 458, 462, 470, 471, 482, 500, 502, 505, 507, 508, 510, 511, 519, 520, 531, 538, 541, 557, 600, 605, 620, 631, 641, 644, 657]
    cases = [541]
    cases_map = {401:'401.bzip2', 403: '403.gcc', 429: '429.mcf', 433: '433.milc', 444: '444.namd', 445: '445.gobmk', 447: '447.dealII',
                 450: '450.soplex', 453: '453.povray', 456: '456.hmmer', 458: '458.sjeng', 462: '462.libquantum', 464: '464.h264ref', 470: '470.lbm',
                 471: '471.omnetpp', 473: '473.astar', 482: '482.sphinx3', 500: '500.perlbench_r', 502: '502.gcc_r', 505: '505.mcf_r', 507: '507.cactuBSSN_r',
                 508: '508.namd_r', 510: '510.parest_r', 511: '511.povray_r', 519: '519.lbm_r', 520: '520.omnetpp_r',  523: '523.xalancbmk_r', 525: '525.x264_r',
                 531: '531.deepsjeng_r', 538: '538.imagick_r', 541: '541.leela_r', 544: '544.nab_r', 557: '557.xz_r', 600: '600.perlbench_s', 602: '602.gcc_s', 605: '605.mcf_s', 607: '607.cactuBSSN_s',
                 619: '619.lbm_s', 620: '620.omnetpp_s', 623: '623.xalancbmk_s', 625: '625.x264_s', 631: '631.deepsjeng_s', 638: '638.imagick_s', 641: '641.leela_s', 644: '644.nab_s',
                 657: '657.xz_s'}
    for case in cases:
        print(case)
        print(cases_map[case])
        optimizeInstrumentation(str(case), cases_map[case])