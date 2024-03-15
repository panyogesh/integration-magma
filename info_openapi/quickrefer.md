# This reference is for all the learnings in openapi

## Generating different codes
java -jar openapi-generator-cli.jar generate -i  https://raw.githubusercontent.com/jdegre/5GC_APIs/master/TS29514_Npcf_PolicyAuthorization.yaml -g openapi-yaml  -o /app/standard/

## Code Generator for golang code
Best reference for golang client & server code for openapi : [go-opeanpi-client-server](https://medium.com/@MikeMwita/generating-go-code-from-openapi-specification-document-ae225e49e970)

* Few quick reference commands
```
oapi-codegen --package=main --generate types,client https://raw.githubusercontent.com/jdegre/5GC_APIs/master/TS29514_Npcf_PolicyAuthorization.yaml > openapi.gen.go
```
## Code generator using purely oapi-codegen
https://gerrit.o-ran-sc.org/r/gitweb?p=nonrtric%2Fplt%2Fsme.git;hb=refs%2Fchanges%2F27%2F11927%2F7;f=r1-sme-manager%2Fgenerate-service-publish-and-discovery.sh  
