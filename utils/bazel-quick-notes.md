# Bazel Commands

## Bazel Unit test infrastructure
* sudo bazel test //lte/gateway/c/core/oai/test/s1ap_task:s1ap_mme_handlers_test
* bazel test //lte/gateway/c/core/oai/test/amf:amf_stateless_test --config=asan --compilation_mode=dbg
* bazel test //lte/gateway/c/core/oai/test/amf:amf_stateless_test --config=lsan
* bazel test //lte/gateway/c/core/oai/test/amf:amf_stateless_test

## Bazel build command
* cd $MAGMA_ROOT && bazel/scripts/build_and_run_bazelified_agw.sh
  
## Bazel Command for adding subscriber
* /home/vagrant/magma/bazel-bin/lte/gateway/python/scripts/subscriber_cli add --lte-auth-key 465B5CE8B199B49FAA5F0A2EE238A6BC --lte-auth-opc E8ED289DEBA952E4283B54E88E6183CA IMSI001010000000008
* /home/vagrant/magma/bazel-bin/lte/gateway/python/scripts/subscriber_cli  update --lte-auth-key 465B5CE8B199B49FAA5F0A2EE238A6BC --lte-auth-opc E8ED289DEBA952E4283B54E88E6183CA --apn-config Internet,5,15,1,1,1000,2000,0,,,,  IMSI001010000000008
