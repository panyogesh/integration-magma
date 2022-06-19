# integration-magma
Quick Integration steps with Open source Magma Repository especially with AGW software.

Have written some small sample programmes helping to integrate mamga beyond the usual stuff.
Hopefully it helps some of the folks in the community 

- MAGMA5GCN-OAIGNBUESim 
Simple guide to provide Integration of core with open source GNB and UE Simulators
   References : https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/docker/README.md
   git pull origin main
   git push  origin HEAD:master

- utils
    Utilties beyond the one provided by Magma like cleaning up core and gz files at regular intervals
 
- DockerizedMagmaTest
    This utlity provides the comibination of dockerized agw with S1AP testing possibility
