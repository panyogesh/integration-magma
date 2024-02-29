# Running the unit tests in open5gs

## Setting it up
- Follow the steps mentioned in [link](https://open5gs.org/open5gs/docs/guide/02-building-open5gs-from-sources/) to setup open5gs

## Enabling debug logs in open5gs
```
diff --git a/lib/core/abts.c b/lib/core/abts.c
index a81e6b870..c826936f5 100644
--- a/lib/core/abts.c
+++ b/lib/core/abts.c
@@ -576,7 +576,7 @@ int abts_main(int argc, const char *const argv[], const char **argv_out)

     argv_out[i++] = "-e";
     if (!optarg.log_level)
-        argv_out[i++] = "error"; /* Default LOG Level : ERROR */
+        argv_out[i++] = "debug"; /* Default LOG Level : ERROR */
     else
         argv_out[i++] = optarg.log_level;

vagrant@exp-open5gs:~/open5gs$
```

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

## Decoding HTTP2 packets of Open5gs
Following steps are tried in Ubuntu-22.0.4
- Follow : https://www.youtube.com/watch?v=yAbgQ0a_ikc
- Main Repo: https://github.com/telekom/OpenAPI-Dissector?tab=readme-ov-file
- Missing step for Ubuntu-22.04 : sudo apt install lua-rex-pcre2

- 
