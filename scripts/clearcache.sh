#!/bin/bash
# Note, we are using "echo 3", but it is not recommended in production instead use "echo 1"
# script added in to keep memory from staying in buffer post run
echo 3 >'/proc/sys/vm/drop_caches' && swapoff -a && swapon -a && printf '\n%s\n' 'Ram-cache and Swap Cleared'
free -h
