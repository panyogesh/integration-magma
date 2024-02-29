# Running the unit tests in open5gs

## Setting it up
- Follow the steps mentioned in [link](https://open5gs.org/open5gs/docs/guide/02-building-open5gs-from-sources/) to setup open5gs

## Running Unit tsets
- Run the command 'meson test -v' from open5gs/build

## Issues 
- Address already in use.
- **Option:1**
  -   Somehow meson test starts the process and does not kills it. Either we can comment out in 'src/main.c' the initialization part ```rv = app_initialize(argv_out);```
-  **Option:2**
  * kill -9 $(ps -eaf | grep open5gs | awk '{print $2}')
  * Run the cases:
```
./tests/attach/attach
./tests/vonr/vonr
ubuntu@dev-meson:~/open5gs/build$ ./tests/vonr/vonr
qos-flow-test       : SUCCESS
session-test        : SUCCESS
simple-test         : SUCCESS
af-test             : SUCCESS
video-test          : SUCCESS
All tests passed.
ubuntu@dev-meson:~/open5gs/build$ ls
```
