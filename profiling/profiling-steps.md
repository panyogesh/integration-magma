# Profiling notes

## Installation
    sudo apt-get install linux-tools-common linux-tools-generic linux-tools-`uname -r`
    sudo apt install linux-tools-common

## Running the scripts
    sudo perf record -F 99 -g -p $(pidof mme)
    perf report
    perf report --stdio -n -g folded

## Reference 
   https://gist.github.com/tstellanova/8f813b7ab593b532a8e135215c1d5c5e
   https://www.brendangregg.com/perf.html
  
