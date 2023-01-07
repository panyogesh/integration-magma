# integration-magma
Quick Integration steps with Open source Magma Repository especially with AGW software.

Have written some small sample programmes helping to integrate mamga beyond the usual stuff.
Hopefully it helps some of the folks in the community 

- deployment-test-magma
    DHCP based testing for magma

- magma-unit-test-infra
    To capture how to do unit testing on bare-metal

- workarounds
    Various workarounds cheat-sheet in magma

- magma5g_cn-oai_gnb_ue_sim 
    Simple guide to provide Integration of core with open source GNB and UE Simulators
    References : https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/develop/docker/README.md
     - git pull origin main
     - git push  origin HEAD:master

- utils
    * Utilties beyond the one provided by Magma like cleaning up core and gz files at regular intervals
    * Workarounds to keep things up

- dockerized-magma-test
    This utlity provides the comibination of dockerized agw with S1AP testing possibility

- test-tool-4G
    4G test tool for scaling UEs and eNBs and testing magma. This is a tool based on fasferraz
    
- srs-ran-setup
    Docker files for srs-ran simulator
