# This is to learn Bazel from Scratch

Reference: https://www.youtube.com/watch?v=toPWLiUq5Ps
Originator: Gisli Konradsson

##Commit-1
Only Basic : write_new_file_impl

###Command to execute
bazel build //:all

### Running Output
Starting local Bazel server and connecting to it...
WARNING: --enable_bzlmod is set, but no MODULE.bazel file was found at the workspace root. Bazel will create an empty MODULE.bazel file. Please consider migrating your external dependencies from WORKSPACE to MODULE.bazel. For more details, please refer to https://github.com/bazelbuild/bazel/issues/18958.
INFO: Analyzed target //:write_my_custom_message_into_file (4 packages loaded, 6 targets configured).
INFO: Found 1 target...
Target //:write_my_custom_message_into_file up-to-date (nothing to build)
INFO: Elapsed time: 10.166s, Critical Path: 0.06s
INFO: 1 process: 1 internal.
INFO: Build completed successfully, 1 total action


### Files Created
vagrant@ubuntu-jammy:~/GoPrograms/NEWBAZEL/integration-magma/utils/bazel-refers$ ls
BUILD         MODULE.bazel.lock  bazel-bazel-refers  bazel-out       my_custom_rule.bzl
MODULE.bazel  WORKSPACE          bazel-bin           bazel-testlogs
