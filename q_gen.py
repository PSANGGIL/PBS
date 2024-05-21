# -*- coding: utf-8 -*-

import re
import os, string, sys, shutil
import fileinput
from contextlib import closing
import argparse

file_list = os.listdir(os.getcwd())
file_list_out = [file for file in file_list if file.endswith(".xyz")]

parser = argparse.ArgumentParser(description='Argparse')

parser.add_argument('--ch', type=int, default=0, help='Molecular charge')
parser.add_argument('--sm', type=int, default=1, help='Total spin multiplicity')

args    = parser.parse_args()

for lo in file_list_out:
    with open("{}".format(lo), "rt") as read_file:
        job_name = lo.split(".");
        re_file_name = job_name[0]+".inp"
        write_file = open(re_file_name, "wt")
        m_file = open("rem.txt", "rt")
        st1 = "$molecule \n"
        st2 = str(args.ch) + " " + str(args.sm) + "\n"
        st3 = "$end\n"
        write_file.write(st1)
        write_file.write(st2)
        lines = read_file.readlines()
        del lines[0]
        del lines[0]
        a = ''.join(lines)
        write_file.writelines(a)
        m_lines = m_file.readlines()
        m = ''.join(m_lines)
        write_file.write(st3)
        write_file.write('\n')
        write_file.write(m)
        read_file.close()
run_file=open("run","wt")
for file in os.listdir(os.getcwd()):
        if file.endswith(".inp"):
                job_name = file.split(".");
                qsh_file_name = job_name[0]+".qsh"

                template='qchem_omp.txt'
                shutil.copyfile(template,qsh_file_name)

                qsh_file=open(qsh_file_name,"rt")
                data=qsh_file.read()
                data=data.replace("test",job_name[0])
                qsh_file.close()

                qsh_file=open(qsh_file_name,"wt")
                qsh_file.write(data)
                qsh_file.close()

                run_file.write("qsub "+qsh_file_name+"\n")
