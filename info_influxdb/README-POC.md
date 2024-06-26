# Tuotorial for golang interaction with influx DB

## References
- [Medium-link](https://medium.com/spankie/getting-started-with-influxdb-with-golang-example-10990c5efee7)
## Checkout the docker image of influxdb
- git clone --depth=1 https://github.com/influxdata/influxdata-docker.git
- cd influxdata-docker
- git sparse-checkout set influxdb
- cd influxdb/1.8


## Build & Run the influxDB
- sudo docker build . -t influxdb_1_8
- sudo docker run -d --name influxdb18 -d -p 8086:8086 influxdb_1_8

## Interact with InfluxDB
- sudo docker exec -it influxdb18 influx


## Basic Understanding
- Database -> notion of database
- Measurement -> table in SQL
- Fields -> Comprised of fieldKeys and fieldValues. fields are required and not indexed
- Tags -> Comprises of tagKeys and tagValues. Tags are optional and can be indexed


## Creating databse in influx
- sudo docker exec -it influxdb18 influx
```
> create database go_influx
> show databases
...
...
go_influx  <<<< Newly created database
```

## Additional Accounts
* go get -u github.com/go-chi/chi/v5
* go get -u github.com/influxdata/influxdb-client-go/v2
```
> use go_influx
> select * from products
> select * from products
name: products
time                ProductID ProductName product
----                --------- ----------- -------
1714816503000000000 0         watch       watch
1714816524000000000 1         Camera      Camera
1714816529000000000 0         watch       watch
>

```
