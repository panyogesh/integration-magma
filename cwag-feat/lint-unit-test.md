# This repository is to have lint and unit test for CWAG feature

## Lint test
- Directory: feg/gateway/docker
- sudo ./build.py --lint
- golangci-lint run -c  ~/PMN-SYSTEMS/pmn-systems//.golangci.yml (from feg/radius/src)

## Unit test
- Directory: feg/gateway/docker
- sudo ./build.py --test
- If the above step failes then
-   sudo docker exec -it test bash
-   go install gotest.tools/gotestsum@latest
-   make test
