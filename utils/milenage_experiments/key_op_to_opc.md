# Procedure to convert Key, OP to OPC Value

## Install the CryptoMobile
* [Link](https://github.com/panyogesh/integration-magma/blob/main/utils/milenage_experiments/package_install.md)  for installation

## Sample code
```
>>> from CryptoMobile.Milenage import make_OPc
>>> from CryptoMobile.Milenage import Milenage
>>> key=b'7036b407351a065d0044101080bc5210'
>>> OP=b'94c2c350b0f2e1de166a01710870b91d'
>>> make_OPc(key, OP).hex()
'cacbe2b40b61d73e0ec2e78306a6b4a319d8b21b77cf96ec207b43ed9f28c697'
```
