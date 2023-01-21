from scapy.all import *
from scapy.contrib.gtp import (
      GTP_U_Header,
      GTPPDUSessionContainer)
sendp(Ether()/IP(src="192.168.62.154", dst='192.168.62.176')/UDP(sport=2152, dport=2152)/GTP_U_Header(teid=0x7fffffff)/GTPPDUSessionContainer(QFI=5)/IP(src='192.168.128.92', dst='8.8.8.8')/UDP(sport=56531, dport=5001)/Raw(load="5G! Hello world"), iface="enp0s8", count=8)
