# Executing the commands

## Executing without debug mode (presense of -O)
sudo python3.8  -O ./eNB/eNB_LOCAL.py -i 192.168.62.154 -m 192.168.62.176 -I 724990000000008 -K 465B5CE8B199B49FAA5F0A2EE238A6BC -C E8ED289DEBA952E4283B54E88E6183CA -o 72499  --upper_limit 724990000000009

## Executing with debug mode (presense of -O)
sudo python3.8 ./eNB/eNB_LOCAL.py -i 192.168.62.154 -m 192.168.62.176 -I 724990000000008 -K 465B5CE8B199B49FAA5F0A2EE238A6BC -C E8ED289DEBA952E4283B54E88E6183CA -o 72499  --upper_limit 724990000000009

## Inside the container
python3.8 /app/eNB/SimLaunch.py --mme_ip ${MME_IP_ADDRESS} --imsi  ${IMSI_BASE} --mcc_mnc ${MCC_MNC_STR} --upper_limit_imsi  ${UPPER_LIMIT_IMSI} --service_request ${SERVICE_REQUEST}

