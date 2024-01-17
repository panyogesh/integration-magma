# Document Purpose
Purpose of this document is to show how *.pb.go files are generated for feg related protos

## Build Feg Dockers
* cd ~/pmn-systems/feg/gateway/docker
* sudo docker-compose -f docker-compose.yml -f docker-compose.override.yml  build

## Run the docker images
* sudo docker ps : ```**20d89c280c56**   feg_gateway_go_base:latest   "bash" 35 minutes ago   Up 35 minutes ```
* sudo docker run -it --name radiusexperiments --security-opt apparmor=unconfined --cap-add CAP_SYS_ADMIN --cap-add=NET_ADMIN  --rm feg_gateway_go_base:latest bash
```
  root@20d89c280c56:/magma/feg/gateway/s# make gen  <<< There might be some errors

  sbi/gen.go:14: running "oapi-codegen": exec: "oapi-codegen": executable file not found in $PATH
  services/csfb/servicers/gen.go:14: running "bash": exit status 127

```

## Copy the pb.go file from container to local
sudo docker cp  20d89c280c56:/magma/feg/gateway/services/aaa/protos/context.pb.go feg/gateway/services/aaa/protos/
