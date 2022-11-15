# Generating multiple subscriber for Magma

## imsI: IMSI001010123456780 (100)

```bash
#!/usr/bin/python3.8

VAL=1010123456780

ADD_SUBS="subscriber_cli.py add --lte-auth-key 00112233445566778899aabbccddeeff --lte-auth-opc 63BFA50EE6523365FF14C1F45F88737D IMSI00"
UPDATE_SUBS="subscriber_cli.py update --lte-auth-key 00112233445566778899aabbccddeeff --lte-auth-opc 63BFA50EE6523365FF14C1F45F88737D --apn-config internet,5,15,1,1,1000,2000,0,,,,  IMSI00"

with open("myfile.txt", "w") as file1:
    for i in range(100):
        NEW_ADD_SUBS=ADD_SUBS+str(VAL)
        NEW_UPDATE_SUBS=UPDATE_SUBS+str(VAL)
        file1.writelines(NEW_ADD_SUBS + '\n')
        file1.writelines(NEW_UPDATE_SUBS + '\n')
        VAL=VAL+1
```
