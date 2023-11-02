# Quick Reference

## Run go test
* go test .  (running tests)
* go  test -v -run TestGenerateEutranVector ./ (prints logs on stdin and run single testcase)

## Running testcase in gdb mode
* go test -c  services/uesim/servicers/eap_aka_test.go services/uesim/servicers/eap_test.go (compile with debug symbols)
* Generates a file called : cwf/gateway/servicers.test
* gdb servicers.test
  




