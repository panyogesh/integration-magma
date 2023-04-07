# Few quick information about production level orchestrator

## Script for collecting logs from all orchestrator
```
#!/usr/bin/env bash

DEPLOYMENT=orc8r

for p in $(kubectl get pods | grep ^${DEPLOYMENT}- | cut -f 1 -d ' '); do
    echo ---------------------------
    echo $p
    echo ---------------------------
    #kubectl logs $p | grep -v error
    kubectl logs $p
done
```
