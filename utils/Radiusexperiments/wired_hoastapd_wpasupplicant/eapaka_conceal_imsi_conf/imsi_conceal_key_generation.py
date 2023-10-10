#!/usr/bin/python3

import base64
import binascii
import time
import subprocess
import logging
logger = logging.getLogger()
from OpenSSL import crypto, SSL

class imsi_certs():
    def __init__(self, mnc='232', mcc='02', imsi='232010000000000', method_id='0',
                 base_path=''):
        self.mcc=mcc
        self.mnc=mnc
        self.imsi=imsi
        self.method_id=method_id
        self.realm=f"wlan.mnc{self.mnc}.mcc{self.mcc}.3gppnetwork.org"
        self.prefix='ap_wpa2_eap_aka_imsi_identity'
        self.permanent_id = self.method_id + self.imsi + '@' + self.realm
        self.PERM_ID_FILE= self.prefix + '.permanent-id'
        with open(self.PERM_ID_FILE, 'w') as f:
            f.write(self.permanent_id)

        self.ENC_ID_FILE= self.prefix + '.enc-permanent-id'
        self.PRIVACY_KEY_FILE="imsi-privacy-key.pem"
        self.PRIVACY_CERT_FILE="imsi-privacy-cert.pem"
        self.PUBKEY_FILE="ap_wpa2_eap_aka_imsi_identity.cert-pub.pem"

    def dispaly_fields(self):
        print(f'method_id={self.method_id}, \nrealm={self.realm}, \nprefix={self.prefix}\
                \npermanent_id={self.permanent_id}, \nperm_id={self.PERM_ID_FILE},\
                \nENC_ID_FILE={self.ENC_ID_FILE}\nPUBKEY_FILE={self.PUBKEY_FILE}')

#for generating code equivalent of
#openssl req -new -x509 -sha256 -newkey rsa:2048 -nodes -days 7500 -keyout imsi-privacy-key.pem -out imsi-privacy-cert.pem
# Can be verified using openssl x509 -inform pem -in imsi-privacy-cert.pem -noout -text
    def cert_gen(self,
        emailAddress="yogesh@mycompany.qmc",
        commonName="Yogesh Pandey",
        countryName="US",
        localityName="Santa Clara",
        stateOrProvinceName="California",
        organizationName="mycompany",
        organizationUnitName="quantum computing",
        serialNumber=0,
        validityStartInSeconds=0,
        validityEndInSeconds=365*24*60*60):

        #can look at generated file using openssl:
        #openssl x509 -inform pem -in selfsigned.crt -noout -text
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = countryName
        cert.get_subject().ST = stateOrProvinceName
        cert.get_subject().L = localityName
        cert.get_subject().O = organizationName
        cert.get_subject().OU = organizationUnitName
        cert.get_subject().CN = commonName
        cert.get_subject().emailAddress = emailAddress
        cert.set_serial_number(serialNumber)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(validityEndInSeconds)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)

        cert.sign(k, 'sha256')
        with open(self.PRIVACY_CERT_FILE, "wt") as f:
            f.write(
             crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
        with open(self.PRIVACY_KEY_FILE, "wt") as f:
            f.write(
             crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))


    def gen_public_key_enc_id(self):
        with open(self.PUBKEY_FILE, "w") as f:
            print(f'Creating fie {self.PUBKEY_FILE}')
        with open(self.ENC_ID_FILE, "w") as f:
            print(f'Creating fie {self.ENC_ID_FILE}')

        subprocess.check_call(
           ["openssl", "x509", "-in",
            self.PRIVACY_CERT_FILE,
            "-pubkey", "-noout",
            "-out", self.PUBKEY_FILE])

        subprocess.check_call(
           ["openssl", "pkeyutl",
            "-inkey", self.PUBKEY_FILE, "-pubin",
            "-in", self.PERM_ID_FILE,
            "-pkeyopt", "rsa_padding_mode:oaep",
            "-pkeyopt", "rsa_oaep_md:sha256",
            "-encrypt",
            "-out", self.ENC_ID_FILE])

        with open(self.ENC_ID_FILE, 'rb') as f:
            data = f.read()
            encrypted_id = base64.b64encode(data).decode()
            if len(encrypted_id) != 344:
                raise Exception("Unexpected length of the base64 encoded identity: " + b64)

gen_certs=imsi_certs(base_path='new_certs')
gen_certs.dispaly_fields()
gen_certs.cert_gen()
gen_certs.gen_public_key_enc_id()
