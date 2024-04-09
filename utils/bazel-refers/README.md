# This is to learn Bazel from Scratch

## Reference: 
[youtube-link](https://www.youtube.com/watch?v=toPWLiUq5Ps)
* Content Creator: Gisli Konradsson

## Commit-1
Only Basic : write_new_file_impl

### Command to execute
bazel build //:all

### Running Output
```
Starting local Bazel server and connecting to it...
WARNING: --enable_bzlmod is set, but no MODULE.bazel file was found at the workspace root. Bazel will create an empty MODULE.bazel file. Please consider migrating your external dependencies from WORKSPACE to MODULE.bazel. For more details, please refer to https://github.com/bazelbuild/bazel/issues/18958.
INFO: Analyzed target //:write_my_custom_message_into_file (4 packages loaded, 6 targets configured).
INFO: Found 1 target...
Target //:write_my_custom_message_into_file up-to-date (nothing to build)
INFO: Elapsed time: 10.166s, Critical Path: 0.06s
INFO: 1 process: 1 internal.
INFO: Build completed successfully, 1 total action
```

### Files Created
```
vagrant@ubuntu-jammy:~/GoPrograms/NEWBAZEL/integration-magma/utils/bazel-refers$ ls
BUILD         MODULE.bazel.lock  bazel-bazel-refers  bazel-out       my_custom_rule.bzl
MODULE.bazel  WORKSPACE          bazel-bin           bazel-testlogs
```


## COMMIT-2

### Command 
```
bazel build //:write_my_custom_message_into_file
```

### Output
```
Starting local Bazel server and connecting to it...
ERROR: /home/vagrant/GoPrograms/NEWBAZEL/integration-magma/utils/bazel-refers/BUILD:3:15: in write_new_file rule //:write_my_custom_message_into_file:
/home/vagrant/GoPrograms/NEWBAZEL/integration-magma/utils/bazel-refers/my_custom_rule.bzl:1:5: The following files have no generating action:
my_output_awsome.txt
ERROR: /home/vagrant/GoPrograms/NEWBAZEL/integration-magma/utils/bazel-refers/BUILD:3:15: Analysis of target '//:write_my_custom_message_into_file' failed
ERROR: Analysis of target '//:write_my_custom_message_into_file' failed; build aborted
INFO: Elapsed time: 3.577s, Critical Path: 0.03s
INFO: 1 process: 1 internal.
ERROR: Build did NOT complete successfully
vagrant@ubuntu-jammy:~/GoPrograms/NEWBAZEL/integration-magma/utils/bazel-refers$
```

