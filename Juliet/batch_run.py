import os
from subprocess import PIPE, Popen
import difflib
import sys
import socket
import time

dete_num = 0
pass_num = 0
error_num = 0

run_testcases_list = []
run_states_list = []
listenning = False

def get_run_testcases():
    global run_testcases_list, run_states_list
    run_testcases_list = []
    run_states_list = []
    with open("output.txt", "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            line.strip()
                
            testcase = line.split(" ")[0]
            state = line.split(" ")[1]
            if testcase in run_testcases_list:# or "pass" in state:
                continue
            run_testcases_list.append(testcase)
            print("Finished-"+testcase)
            run_states_list.append(state)

def check_asan(testcase: str, stderr: bytes):
    global dete_num
    global pass_num
    global error_num
    if len(stderr) <= 1:
        pass_num = pass_num +1
        return "pass"
    for raw in stderr:
        
        if b"PrintfCheck-metadata" in raw:
            continue
        
        if b"tag-mismatch" in raw or b"CopyRightBy-wxl" or b"AddressSanitizer" in raw:
            dete_num = dete_num +1
            return "detected"
            
        if b"DEADLYSIGNAL" in raw or b"SEGV" in raw or b"The signal is caused by" in raw:
            error_num =  error_num +1
            return "error"
            
        #if b"Warning: Attempt_to_Access_Child_of_Non_Structure_Pointer!" in raw:
        #    dete_num = dete_num +1
        #    return "detected"'
        if b"CopyRightBy-wxl" in raw:
            #print("************3!")
            vuln_target = "-".join(testcase.lower().split("__")[0].split("_")[1:])
            vuln_check = "NULL"
            for s in raw.decode().split(" "):
                if "-" in s:
                    vuln_check = s.strip()
                    break
            similarity = difflib.SequenceMatcher(lambda x: x=="-", vuln_target, vuln_check).quick_ratio()
            if similarity > 0.6:
                dete_num = dete_num +1
                #print("************4!")
                return "detected"
            else:
                dete_num = dete_num +1
                #print("************5!")
                return "detected:"+vuln_check
    pass_num =  pass_num +1
    return "pass"

def run(dir):
    os.chdir(dir)
    print(dir)
    get_run_testcases()
    for root,dirs,files in os.walk(dir):
        for testcase in files:
            if testcase[-4:] == ".out":
                if testcase[:-4] in run_testcases_list or "good" in testcase or "listen_socket" in testcase:
                #if "connect_socket" not in testcase:
                    continue

                times = 10 if "rand" in testcase else 1
                states = []
                for _ in range(times):
                    if "fgets" in testcase or "fscanf" in testcase or "console" in testcase:
                        p = Popen("./"+testcase, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
                        if "CWE134" in testcase:
                            p.stdin.write(b"absdfa%s%ddafdasd\n")
                            p.stdin.close()
                        elif "Under" in testcase:
                            p.stdin.write(b"-10\n")
                            p.stdin.close()
                        else:
                            p.stdin.write(b"20\n")
                            p.stdin.close()
                    elif "connect_socket" in testcase:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        address = ('127.0.0.1', 27015)
                        s.connect(address)
                        s.send(testcase.encode())
                        s.shutdown(2)
                        s.close()
                        p = Popen("./"+testcase, shell=True, stdout=PIPE, stderr=PIPE)
                    elif "linsten_socket" in testcase:
                        p = Popen("./"+testcase, shell=True, stdout=PIPE, stderr=PIPE)
                        client = Popen("python3 /home/test/workspace-15/Juliet/dummy_client.py \'"+testcase+"\'", shell=True, stdout=PIPE, stderr=PIPE)
                        client.communicate()
                    elif "environment" in testcase:
                        if "CWE134" in testcase:
                            p = Popen("export ADD=dfada%s%ddfafda && ./"+testcase, shell=True, stdout=PIPE, stderr=PIPE)
                        else:
                            p = Popen("export ADD=TESTCASE && ./"+testcase, shell=True, stdout=PIPE, stderr=PIPE)
                    elif "char_file" in testcase:
                        if "CWE134" in testcase:
                            p = Popen("echo dfada%s%ddfafda > /tmp/file.txt && ./"+testcase, shell=True, stdout=PIPE, stderr=PIPE)
                        else:
                            p = Popen("echo TESTCASE > /tmp/file.txt && ./"+testcase, shell=True, stdout=PIPE, stderr=PIPE)
                    else:
                        p = Popen("./"+testcase, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
                        try:
                            p.stdin.write(b"-10\n")
                            p.stdin.close()
                        except:
                            pass
                    try:
                        p.wait(timeout=3)
                    except:
                        states.append("timeout")
                        break
                    states.append(check_asan(testcase, p.stderr.readlines()))

                if "socket" in testcase:
                    time.sleep(2)
                
                if "rand" in testcase:
                    state = "pass"
                    for s in states:
                        if (s == "error") or ("detected" in s):
                            state = s
                            break
                else:
                    state = states[0]
                
                testcase = testcase[:-4]
                print(testcase, state)
                with open("output.txt", "a") as f:
                    f.write(testcase + " "+state+"\n")

def main():
    global dete_num
    global pass_num
    global error_num
    dir="/home/test/OLASan-Artifact/Juliet/testcases/CWE122_Heap_Based_Buffer_Overflow/s11/"
    #logfilepath=dir+"/"+"output.txt"
    #logfile = open(logfilepath, "a")
    run(dir)
    #logfile.close()
    print(dete_num)
    print(pass_num)
    print(error_num)

if __name__ == "__main__":
    main()