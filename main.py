# -*- coding: utf-8 -*-

import re
import os, string, sys, shutil
import fileinput
from contextlib import closing
import argparse

def MAIN(rem_file, omp_file, core, walltime, memory, queue):
    XYZ2INP(rem_file)
    INP2QSH(omp_file, core, walltime, memory, queue)
    print("done")


def XYZ2INP(rem_file):
    for lo in file_list_out:
        with open("{}".format(lo), "rt") as read_file:
            job_name = lo.split(".");
            re_file_name = job_name[0]+".inp"
            write_file = open(re_file_name, "wt")
            m_file = open(rem_file, "rt")
            write_file.write("$molecule \n" + str(args.charge) + " " + str(args.spin) + "\n")
            lines = read_file.readlines()
            del lines[0]
            del lines[0]
            a = ''.join(lines)
            write_file.writelines(a)
            m_lines = m_file.readlines()
            m = ''.join(m_lines)
            write_file.write("$end\n\n")
            write_file.write(m)
            read_file.close()

def INP2QSH(omp_file, core, walltime, memory, queue):
    run_file=open("run.sh","wt")
    for file in os.listdir(os.getcwd()):
        if file.endswith(".inp"):
            job_name = file.split(".");
            qsh_file_name = job_name[0]+".qsh"
    
            shutil.copyfile(omp_file,qsh_file_name)
    
            qsh_file=open(qsh_file_name,"rt")
            data=qsh_file.read()
            data=data.replace("test"            , job_name[0])
            data=data.replace("DATA_QUEUE"      , queue)
            data=data.replace("DATA_CORE"       , core)
            data=data.replace("DATA_WALLTIME"   , walltime)
            data=data.replace("DATA_MEMORY"     , memory)
            qsh_file.close()
    
            qsh_file=open(qsh_file_name,"wt")
            qsh_file.write(data)
            qsh_file.close()
    
            run_file.write("qsub "+qsh_file_name+"\n")
    
if __name__ == "__main__":

    file_list = os.listdir(os.getcwd())
    file_list_out = [file for file in file_list if file.endswith(".xyz")]
    
    parser = argparse.ArgumentParser(description='Argparse')
    
    parser.add_argument('--charge'  , type=int, default=0,      help='Molecular charge')
    parser.add_argument('--spin'    , type=int, default=1,      help='Total spin multiplicity')
    parser.add_argument('--core'    , type=int, default=4,      help='Number of cpu core')
    parser.add_argument('--walltime', type=str, default='96:00:00',  help='walltile')
    parser.add_argument('--memory'  , type=str, default='4gb',  help='memory usage')
    parser.add_argument('--queue'   , type=str, default='batch',help='Select queue')
    
    args    = parser.parse_args()
    
    rem_file = 'rem.txt' 
    omp_file = 'qchem_omp_v2.txt'
     
    MAIN(rem_file, omp_file, str(args.core), str(args.walltime), str(args.memory), str(args.queue))
