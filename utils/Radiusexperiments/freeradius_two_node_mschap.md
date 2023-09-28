# Few other combinations
*
## Specific message in response

* Radius Server
```
root@distro-magma:/usr/local/etc/raddb# sudo cat /usr/local/etc/raddb/users | grep alice -A2
"alice" Cleartext-Password := "passme"
    Reply-Message = "Hello, %{User-Name}"
root@distro-magma:/usr/local/etc/raddb#
```

* Radius Client
```
root@distro-magma:/home/vagrant# radtest -t mschap alice  "passme" 10.1.1.10 1812 my_Sup4r_SeCret_Pa$
Sent Access-Request Id 166 from 0.0.0.0:d1d5 to 10.1.1.10:1812 length 131
        User-Name = "alice"
        MS-CHAP-Password = "passme"
        NAS-IP-Address = 127.0.2.1
        NAS-Port = 1812
        Message-Authenticator = 0x00
        Cleartext-Password = "passme"
        MS-CHAP-Challenge = 0x0754c6ffc9482709
        MS-CHAP-Response = 0x0001000000000000000000000000000000000000000000000000a86e11df80ae89a29595dccf4bcee276de95c6ccc723f281
Received Access-Accept Id 166 from 10.1.1.10:714 to 10.1.1.1:53717 length 98
       ** Reply-Message = "Hello, alice"**   <<<<<<<<<< Response
        MS-CHAP-MPPE-Keys = 0x00000000000000008bc9ffb320eb72e0f8cb60f5dd7d53ee
        MS-MPPE-Encryption-Policy = Encryption-Allowed
        MS-MPPE-Encryption-Types = RC4-40or128-bit-Allowed
root@distro-magma:/home/vagrant# radtest -t mschap alice  "passme" 10.1.1.10 1812 my_Sup4r_SeCret_Pa$
