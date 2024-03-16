# Adding subscriber in open5gs command line

## Two procedures for the same (apart from WebUI)

### 1. Installing mongosh
[Reference](https://www.mongodb.com/docs/mongodb-shell/install/)
```
wget -qO- https://www.mongodb.org/static/pgp/server-7.0.asc | sudo tee /etc/apt/trusted.gpg.d/server-7.0.asc
sudo apt-get install gnupg
wget -qO- https://www.mongodb.org/static/pgp/server-7.0.asc | sudo tee /etc/apt/trusted.gpg.d/server-7.0.asc
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-mongosh
```

### 1.1 Using the add command
[References](https://himanshup.hashnode.dev/5g-sa-lab-setup-using-srsran-open5gs)
```
wget https://raw.githubusercontent.com/open5gs/open5gs/main/misc/db/open5gs-dbctl
chmod +x open5gs-dbctl
./open5gs-dbctl add 999700000000001 465B5CE8B199B49FAA5F0A2EE238A6BC E8ED289DEBA952E4283B54E88E6183CA
```

### 2. Using the mongo direct command
