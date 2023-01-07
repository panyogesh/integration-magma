FROM ubuntu:20.04

ENV TZ=Asia/Kolkata

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update

RUN apt install -y tzdata

RUN apt-get update -y

RUN apt-get upgrade -y

RUN apt-get -y install build-essential cmake libfftw3-dev libmbedtls-dev libboost-program-options-dev libconfig++-dev libsctp-dev libzmq3-dev git net-tools

WORKDIR enb4GSim

RUN git clone https://github.com/srsRAN/srsRAN.git

WORKDIR /enb4GSim/srsRAN

RUN mkdir build

WORKDIR /enb4GSim/srsRAN/build/

RUN cmake /enb4GSim/srsRAN

RUN make

RUN make install

RUN ldconfig

RUN mkdir /root/.config

RUN mkdir /root/.config/srsran

RUN cp /enb4GSim/srsRAN/srsepc/epc.conf.example ~/.config/srsran/epc.conf

RUN cp /enb4GSim/srsRAN/srsepc/mbms.conf.example ~/.config/srsran/mbms.conf

RUN cp /enb4GSim/srsRAN/srsepc/user_db.csv.example ~/.config/srsran/user_db.csv

RUN cp /enb4GSim/srsRAN/srsue/ue.conf.example ~/.config/srsran/ue.conf

RUN cp /enb4GSim/srsRAN/srsenb/sib.conf.example ~/.config/srsran/sib.conf

RUN cp /enb4GSim/srsRAN/srsenb/rb.conf.example ~/.config/srsran/rb.conf

RUN cp /enb4GSim/srsRAN/srsenb/rr.conf.example ~/.config/srsran/rr.conf

RUN cp /enb4GSim/srsRAN/srsenb/sib.conf.mbsfn.example ~/.config/srsran/sib.conf.mbsfn

RUN cp /enb4GSim/srsRAN/srsenb/enb.conf.example ~/.config/srsran/enb.conf


CMD ["/bin/sh"]
