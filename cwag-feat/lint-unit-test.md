# This repository is to have lint and unit test for CWAG feature

## Special Note
If docker version 24.0.5 is being used an additional plugin needs to be installed 'sudo apt install docker-compose-v2'
[issue-link](https://askubuntu.com/questions/1488582/docker-24-0-5-on-ubuntu-22-04-using-ubuntu-repositories-not-docker-official-pp)

## Lint test
- Directory: feg/gateway/docker
- sudo ./build.py --lint
- golangci-lint run -c  ~/PMN-SYSTEMS/pmn-systems//.golangci.yml (from feg/radius/src)
- If Lint test fails use the following command to fix the regular errors:
-   gofmt -s -w  ./gateway/services/aaa/servicers/accounting.go (from Host Machine)
-  go install golang.org/x/tools/cmd/goimports@latest
-  goimports -l -w .
  
## Another option
- cd feg/gateway/docker/
- export MAGMA_ROOT=/home/vagrant/pmn-systems/
- make lint

## Unit test
- Directory: feg/gateway/docker
- sudo ./build.py --test
- If the above step failes then
   * sudo docker exec -it test bash
   * go install gotest.tools/gotestsum@latest
   * make test
