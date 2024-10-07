# Basic information on Custom Resource Definition

## List resources with cluster
* kubectl api-resources
```
bindings                                         v1                                true         Binding
componentstatuses                   cs           v1                                false        ComponentS
configmaps                          cm           v1                                true         ConfigMap
endpoints                           ep           v1                                true         Endpoints
events                              ev           v1                                true         Event
limitranges                         limits       v1                                true         LimitRange
namespaces                          ns           v1                                false        Namespace
nodes                               no           v1                                false        Node
persistentvolumeclaims              pvc          v1                                true         Persistent
daemonsets                          ds           apps/v1                           true         DaemonSet
deployments                         deploy       apps/v1                           true         Deployment
.....
storageclasses                      sc           storage.k8s.io/v1                 false        StorageClass
volumeattachments                                storage.k8s.io/v1                 false        VolumeAttachment
```
* Resources
  - A resource is an end point in kubernetes api that store collection of API objects.
  - "apps/v1" is API Endpoint Group
