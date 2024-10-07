# Basic information on Custom Resource Definition

## Refrences
* [Link-1](https://www.youtube.com/watch?v=u1X5Rf7fWwM)

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
  - Depoloyment is resource - API Object
* Custom Resources
  - Customized Resources are extension of the Kubernetes API
  - Resource which is not available by default
  - Once created, can be accessed using kubectl
  - Provides declarative API
* Definition
  - Declarative commands to API server in the form of YAML construct 

