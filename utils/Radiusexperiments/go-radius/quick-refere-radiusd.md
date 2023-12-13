# This file is to bring up a radius server based on golang

## Installation steps

### Checkout the code
git clone https://github.com/mpdroog/radiusd.git
cd radiusd/test

### Install and configure mysql

* sudo apt install -y mysql-server
* sudo mysql
  ```
  ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';

  mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
   Query OK, 0 rows affected (0.01 sec)
   exit
   ```
* sudo mysql -u root -ppassword  (Adding other users)
  ```
  - ALTER USER 'root'@'localhost' IDENTIFIED WITH auth_socket;

  mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH auth_socket;
  Query OK, 0 rows affected (0.01 sec)

  mysql> CREATE USER 'user'@'%' IDENTIFIED BY 'password';
  mysql> grant all privileges on *.* to 'user'@'%' with grant option;
  mysql> CREATE DATABASE dbname;
  mysql> exit
  ``` 

* sudo mysql -uroot -ppassword dbname < vpnxs_radius.sql


### Install and build radiusd
```
cd radiusd
go build
sudo go run main.go control.go tcpKeepAliveListener.go
```

### Run the test
cd radiusd/test
./test.sh
