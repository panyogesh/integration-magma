# Following steps for generating the ue sim proto pb.go files

## Make the following changes
1. Modify the file cwf/gateway/docker/go/Dockerfile

```
diff --git a/cwf/gateway/docker/go/Dockerfile b/cwf/gateway/docker/go/Dockerfile
index 6b339c56f..589ed6fd0 100644
--- a/cwf/gateway/docker/go/Dockerfile
+++ b/cwf/gateway/docker/go/Dockerfile
@@ -112,32 +112,6 @@ COPY cwf $MAGMA_ROOT/cwf
 COPY feg $MAGMA_ROOT/feg
 COPY lte/cloud $MAGMA_ROOT/lte/cloud
 COPY orc8r/lib/go $MAGMA_ROOT/orc8r/lib/go
+COPY orc8r/protos $MAGMA_ROOT/orc8r/protos
 COPY orc8r/cloud $MAGMA_ROOT/orc8r/cloud
 COPY orc8r/gateway/go $MAGMA_ROOT/orc8r/gateway/go
-
-# Enable make gen if proto gen is required
-# RUN make -C $MAGMA_ROOT/cwf/gateway gen
-RUN make -C $MAGMA_ROOT/cwf/gateway build
-
-# -----------------------------------------------------------------------------
-# Production image
-# -----------------------------------------------------------------------------
-FROM ${baseImage} AS cwag_go
-
-# Install envdir.
-RUN apt-get -y update && apt-get -y install daemontools curl arping
-
-# Copy the build artifacts.
-COPY --from=builder /var/opt/magma/bin /var/opt/magma/bin
-
-RUN mkdir -p /etc/magma
-# Copy the configs.
-COPY cwf/gateway/configs /etc/magma
-
-# Create empty envdir directory
-RUN mkdir -p /var/opt/magma/envdir
-
-RUN mkdir -p /var/opt/magma/configs
-
-COPY cwf/gateway/configs/gateway.mconfig /var/opt/magma/configs/gateway.mconfig
-COPY cwf/gateway/configs/service_registry.yml /etc/magma/service_registry.yml
```

2.  Have only uesim in the compose file
```
services:
  uesim:
    <<: *service
    container_name: uesim
    image: ${DOCKER_REGISTRY}cwag_go:${IMAGE_VERSION}
    command: envdir /var/opt/magma/envdir /var/opt/magma/bin/uesim -logtostderr=true -v=0
```
3. Build the imnage
sudo docker-compose -f docker-compose.uesim.yml -f docker-compose.override.yml  build


4. Launch the docker container
sudo docker run -it --name radiusexperiments --security-opt apparmor=unconfined --cap-add CAP_SYS_ADMIN --cap-add=NET_ADMIN --rm    cwf_cwag_go:latest bash


## Compiling the proto
protoc  --proto_path=/magma/cwf/protos --proto_path=/magma/  --go_out=plugins=grpc:/magma/cwf/cloud/go /magma/cwf/protos/*.proto

