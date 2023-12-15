15. S1 Setup -> 4. Set Session type -> 4. Set Session type -> 20. Attach -> 35. E-RAB ModificationIndication (5G)

|  0. Show current settings                   |  2023-01-14 22:41:02.688237: S1AP: sending S1SetupRequest                                                    |
|  1. Set S1 Setup type                       |  2023-01-14 22:41:02.703258: S1AP: S1SetupResponse received                                                  |
|  2. Set Attach Mobile Identity              |  2023-01-14 22:41:17.116866: Session Type: NBIOT                                                             |
|  3. Set Attach PDN                          |  2023-01-14 22:41:22.900352: Session Type: 5G                                                                |
|  4. Set Session type                        |  2023-01-14 22:41:35.585195: S1AP: sending InitialUEMessage                                                  |
|  5. Set NBIOT PSM/eDRX                      |  2023-01-14 22:41:35.614600: S1AP: DownlinkNASTransport received                                             |
|  6. Set PDN type                            |  2023-01-14 22:41:35.618398: NAS: AuthenticatonRequest received                                              |
|  7. Set CPSR type                           |  2023-01-14 22:41:35.623920: S1AP: sending UplinkNASTransport                                                |
|  8. Set Attach type                         |  2023-01-14 22:41:35.632082: S1AP: DownlinkNASTransport received                                             |
|  9. Set TAU type (for option 22)            |  2023-01-14 22:41:35.635766: NAS: SecurityMode received                                                      |
| 10. Set Process Paging                      |  2023-01-14 22:41:35.639503: NAS: sending SecurityModeComplete                                               |
| 11. Set SMS (AdditionalUpdateType)          |  2023-01-14 22:41:35.643047: S1AP: sending UplinkNASTransport                                                |
| 12. Set eNB-CellID/TAC                      |  2023-01-14 22:41:35.680368: S1AP: InitialContextSetupRequest received                                       |
| 13. Set P-CSCF Restoration Support          |  2023-01-14 22:41:35.683882: S1AP: sending InitialContextSetupResponse                                       |
|                                             |  2023-01-14 22:41:35.687684: NAS: AttachAccept received                                                      |
| 15. S1 Setup                                |  2023-01-14 22:41:35.691065: [('apn', 'internet')]                                                           |
| 16. S1 Reset                                |  2023-01-14 22:41:35.694697: [('pdn type value', 1), ('ipv4', '192.168.128.12')]                             |
|                                             |  2023-01-14 22:41:35.704322: [('type of identity', 6), ('mcc', 724), ('mnc', 99), ('mme group id', 1), ('mme |
| 20. Attach                                  |  2023-01-14 22:41:35.704322:  code', 1), ('m-tmsi', 1011627997), ('s-tmsi', b'\x01<L7\xdd')]                 |
| 21. Detach                                  |  2023-01-14 22:41:35.708026: NAS: sending AttachComplete                                                     |
| 22. TAU                                     |  2023-01-14 22:41:35.711556: S1AP: sending UplinkNASTransport                                                |
| 23. TAU Periodic                            |  2023-01-14 22:41:35.927415: S1AP: DownlinkNASTransport received                                             |
| 24. Service Request                         |  2023-01-14 22:41:35.931529: NAS: EMMInformation received                                                    |
| 25. Release UE Context                      |  2023-01-14 22:41:40.711811: S1AP: sending E-RABModificationIndication                                       |
| 26. Send SMS                                |  2023-01-14 22:41:40.728245: S1AP: E-RABModificationConfirm received                                         |
| 30. Control Plane Service Request           |                                                                                                              |
| 35. E-RAB ModificationIndication (5G)       |                                                                                                              |
| 36. Secondary RAT Data Usage Report (5G)    |                                                                                                              |
|                                             |                                                                                                              |
| 40. PDN Connectivity                        |       


sudo python3.8 /home/vagrant/eNB/eNB_LOCAL.py -i 192.168.62.154 -m 192.168.62.176 -I 724990000000008 -K 465B5CE8B199B49FAA5F0A2EE238A6BC -C E8ED289DEBA952E4283B54E88E6183CA -o 72490

sudo docker exec magmad subscriber_cli.py  add --lte-auth-key 465B5CE8B199B49FAA5F0A2EE238A6BC --lte-auth-opc E8ED289DEBA952E4283B54E88E6183CA IMSI724990000000008
 sudo docker exec magmad subscriber_cli.py update --lte-auth-key 465B5CE8B199B49FAA5F0A2EE238A6BC --lte-auth-opc E8ED289DEBA952E4283B54E88E6183CA --apn-config internet,5,15,1,1,1000,2000,0,,,,  IMSI724990000000008
