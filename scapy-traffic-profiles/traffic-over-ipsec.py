"""
vagrant@oai-gnb-ue-sim:~/scapy$ sudo ip xfrm state
src 192.168.62.154 dst 192.168.62.176
        proto esp spi 0xcef22b0e reqid 5 mode tunnel
        replay-window 0 flag af-unspec
        auth-trunc hmac(sha256) 0x3b117ca320583f1388925c6bb59c1219829d6f3d4bf82a2f363427cd467bcbac 128
        enc cbc(aes) 0xc58ce796880323e62ffd8f3b3ff029bf59bf5122b9d5a3f8a2c2bdfee32daace
        anti-replay context: seq 0x0, oseq 0x0, bitmap 0x00000000
src 192.168.62.176 dst 192.168.62.154
        proto esp spi 0xce301acf reqid 5 mode tunnel
        replay-window 32 flag af-unspec
        auth-trunc hmac(sha256) 0x662a48b66f4832e276bb1a39c13372a144fee57d6a9bc4f7fe1cbb13a779386c 128
        enc cbc(aes) 0x65d34bc144737dba4507fa5492b0a6056272c1e90bbf85c305844ed3e242797f
        anti-replay context: seq 0x0, oseq 0x0, bitmap 0x00000000
vagrant@oai-gnb-ue-sim:~/scapy$
"""

from scapy.all import *
from scapy.contrib.gtp import (
      GTP_U_Header,
      GTPPDUSessionContainer)

packet = IP(src="2.2.2.2", dst='1.1.1.1')
packet /= UDP(sport=2152, dport=2152)
packet /= GTP_U_Header(teid=0x7fffffff)
packet /= GTPPDUSessionContainer(QFI=5)
packet /= IP(src='192.168.128.92', dst='8.8.8.8')
packet /= UDP(sport=56531, dport=5001)
packet /= Raw(load="5G! Hello world")

sa = SecurityAssociation(ESP, spi=0xc0a85258,
                         crypt_algo='AES-CBC', crypt_key=b'e8cf19ce96ffeade995c0321a3837e5e',
                         auth_algo='SHA2-256-128', auth_key=b'0xd3dad60aff2d34d429b50d36bebcbcd4983c47cb0a76f58238ec46f138d89830')

e = sa.encrypt(packet)
sendp(Ether() / e, iface="lo", count=8)
print(e)
assert(isinstance(e, IP))
assert(e.src == '2.2.2.2' and e.dst == '1.1.1.1')

#send(Ether()/IP(src="2.2.2.2", dst='1.1.1.1')/UDP(sport=2152, dport=2152)/GTP_U_Header(teid=0x7fffffff)/GTPPDUSessionContainer(QFI=5)/IP(src='192.168.128.92', dst='8.8.8.8')/UDP(sport=56531, dport=5001)/Raw(load="5G! Hello world"), count=8)
