# Bazel Commands
* sudo bazel test //lte/gateway/c/core/oai/test/s1ap_task:s1ap_mme_handlers_test
* bazel test //lte/gateway/c/core/oai/test/amf:amf_stateless_test --config=asan --compilation_mode=dbg
* bazel test //lte/gateway/c/core/oai/test/amf:amf_stateless_test --config=lsan
* bazel test //lte/gateway/c/core/oai/test/amf:amf_stateless_test
