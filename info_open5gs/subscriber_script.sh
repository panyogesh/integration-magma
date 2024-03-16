#!/bin/bash

IMSI=999700000000001
MSISDN=0000000001
KI=465B5CE8B199B49FAA5F0A2EE238A6BC
OPC=E8ED289DEBA952E4283B54E88E6183CA

mongo --eval "db.subscribers.update( { \"imsi\" : \"$IMSI\" },
    { \$setOnInsert:
        {
            \"imsi\" : \"$IMSI\",
            \"subscribed_rau_tau_timer\" : NumberInt(12),
            \"network_access_mode\" : NumberInt(2),
            \"subscriber_status\" : NumberInt(0),
            \"access_restriction_data\" : NumberInt(32),
            \"slice\" :
            [{
                \"sst\" : NumberInt(1),
                \"default_indicator\" : true,
                \"_id\" : new ObjectId(),
                \"session\" :
                [{
                    \"name\" : \"internet\",
                    \"type\" : NumberInt(3),
                    \"_id\" : new ObjectId(),
                    \"pcc_rule\" : [{
                        \"qos\" : { 
                            \"index\" : NumberInt(1),
                            \"gbr\" : {
                                \"uplink\" : { \"value\": NumberInt(1), \"unit\" : NumberInt(3) },
                                \"downlink\" : { \"value\": NumberInt(1), \"unit\" : NumberInt(3) }
                            },
                            \"mbr\" : {
                                \"uplink\" : { \"value\": NumberInt(1), \"unit\" : NumberInt(3) },
                                \"downlink\" : { \"value\": NumberInt(1), \"unit\" : NumberInt(3) }
                            },
                            \"arp\" : {
                                \"priority_level\" : NumberInt(2),
                                \"pre_emption_capability\" : NumberInt(2),
                                \"pre_emption_vulnerability\" : NumberInt(2)
                            }
                        },
                        \"flow\" : [
                            {
                                \"direction\" : NumberInt(1),
                                \"description\" : \"permit out udp from any 1-65535 to 45.45.45.45\",
                            },
                            {
                                \"direction\" : NumberInt(2),
                                \"description\" : \"permit out udp from any 1-65535 to 45.45.45.45\",
                            },
                        ]
                    }],
                    \"ambr\" :
                    {
                        \"uplink\" : { \"value\": NumberInt(1), \"unit\" : NumberInt(3) },
                        \"downlink\" : { \"value\": NumberInt(1), \"unit\" : NumberInt(3) },
                    },
                    \"qos\" :
                    {
                        \"index\" : NumberInt(9),
                        \"arp\" :
                        {
                            \"priority_level\" : NumberInt(8),
                            \"pre_emption_capability\" : NumberInt(1),
                            \"pre_emption_vulnerability\" : NumberInt(1),
                        },
                    },
                }],
            }],
            \"ambr\" :
            {
                \"uplink\" : { \"value\": NumberInt(1), \"unit\" : NumberInt(3) },
                \"downlink\" : { \"value\": NumberInt(1), \"unit\" : NumberInt(3) },
            },
            \"security\" :
            {
                \"k\" : \"$KI\",
                \"amf\" : \"8000\",
                \"op\" : null,
                \"opc\" : \"$OPC\",
                \"msisdn\" : [ \"$MSISDN\" ],
                \"schema_version\" : NumberInt(1),
            },
            \"__v\" : 0
        },
    },
    upsert=true);" open5gs
exit 0
