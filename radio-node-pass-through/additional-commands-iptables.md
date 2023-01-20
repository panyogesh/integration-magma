# Additional commands in iptables

## Logging
* sudo modprobe ipt_LOG
* Add : sudo iptables -A PREROUTING -t raw -p udp --dport 33434 -j LOG 
* Del : sudo iptables -D PREROUTING -t raw -p udp --dport 33434 -j LOG

- sudo iptables -I FORWARD --protocol udp --dport 33434 -j LOG
- sudo iptables -D FORWARD --protocol udp --dport 33434 -j LOG


## Scapy scrpit
sendp(Ether(src="08:00:27:d7:ba:1b", dst="08:00:27:12:4a:66")/IP(src="192.168.129.52", dst='8.8.8.8')/UDP(sport=5001, dport=5002)/Raw(load="5G! Hello world"), iface="enp0s9", count=8)

## Verification
- nslookup www.example.com
- sudo ip route add 93.184.216.34/32 via 192.168.60.142 dev enp0s8
- curl --interface 192.168.60.154 https://www.example.com/

## Useful commands
* Clearing counters : sudo iptables -t nat -nvL --zero
* Adding high priority rule : sudo iptables -I FORWARD 1 -i eth1 -o eth0 -p tcp  -s 192.168.60.154 --dport 443 -j ACCEPT
