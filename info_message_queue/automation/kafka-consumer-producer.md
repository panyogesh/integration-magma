 volumeMounts:
    - name: crypto-config
      mountPath: <PATH IN CONTAINER>
    - name: channel-artifacts
      mountPath: /opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts
    - name: chaincode
      mountPath: /opt/gopath/src/github.com/chaincode
  volumes:
    - name: crypto-config
      hostPath:
        path: <YOUR LOCAL DIR PATH>
    - name: channel-artifacts
      hostPath:
        path: /Users/akshaysood/Blockchain/Kubernetes/Fabric/network/channel-artifacts
    - name: chaincode
      hostPath:
        path: /Users/akshaysood/Blockchain/Kubernetes/Fabric/network/chaincode
