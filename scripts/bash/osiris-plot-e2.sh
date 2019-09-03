#!/bin/bash 

basepath=$(dirname $0)
base=$(basename $0 .sh)

cmd="ipython $basepath/../python/$base.py $@"

echo $cmd

$cmd