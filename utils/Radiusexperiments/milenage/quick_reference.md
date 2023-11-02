# This directory is for quick referencing milenage algoritm in eap-aka

## Milenage github Repo
* Magma Milenage
```
git clone https://github.com/magma/milenage.git
cd milenage/
go  test -v .
go  test -v -run TestGenerateEutranVector ./
```
wmnsk milenage
```
git clone https://github.com/wmnsk/milenage.git
cd milenage/
go  test -v -run TestGenerateEutranVector ./

