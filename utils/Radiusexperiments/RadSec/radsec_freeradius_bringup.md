# Procedure for bringing up radsec using freeradius

## Topology
[radius-sec-server - 192.168.60.176] ----------- [192.168.60.177 radsec-proxy 127.0.0.1] ----- [127.0.0.1 radclient]

## Checkout freeradius version 3.2.x
https://github.com/FreeRADIUS/freeradius-server.git
cd freeradius
git checkout origin/v3.2.x

## Compiling freeradius
./configure --with-modules="rlm_sim" --with-modules="rlm_sim_files"
 make
sudo make install

## Configuration
radsec-server
 - apply RadSecServer.diff

radsec-client
 - apply RadSecProxy.diff

## Testing (3 terminals)
* Terminal-1
```
sudo radiusd -d raddb/ -fxxl /dev/stdout
```

* Terminal-2
```
sudo radiusd -d raddb/ -X
```

* Terminal-3
```
echo "User-Name = bob" | radclient 127.0.0.1 auth testing123
```

## Logs attached




