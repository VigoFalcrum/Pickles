#!/bin/bash

taskset -c 3 /usr/bin/time -v python3 RF_4_15_100.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_4_15_400.py >>log.txt 2>&1
taskset -c 3 /usr/bin/time -v python3 RF_4_15_1000.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_4_35_100.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_4_35_1000.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_4_35_10000.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_4_80_100.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_4_80_1000.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_4_80_10000.py >>log.txt 2>&1 

taskset -c 3 /usr/bin/time -v python3 RF_20_15_100.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_20_15_400.py >>log.txt 2>&1
taskset -c 3 /usr/bin/time -v python3 RF_20_15_1000.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_20_35_100.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_20_35_1000.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_20_35_10000.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_20_80_100.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_20_80_1000.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_20_80_10000.py >>log.txt 2>&1 

taskset -c 3 /usr/bin/time -v python3 RF_80_15_100.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_80_15_400.py >>log.txt 2>&1
taskset -c 3 /usr/bin/time -v python3 RF_80_15_1000.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_80_35_100.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_80_35_1000.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_80_35_10000.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_80_80_100.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_80_80_1000.py >>log.txt 2>&1 
taskset -c 3 /usr/bin/time -v python3 RF_80_80_10000.py >>log.txt 2>&1 

