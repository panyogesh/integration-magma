
# Postgres Dumps in postgresql 

## Dev Way of connections

### Orchetrator Table
```docker exec -it orc8r_postgres_1 psql -U magma_dev
magma_dev=# \dt
magma_dev=# \l
magma_dev=# \d+ bootstrapper
SELECT * FROM cfg_network_configs;

Connect to the database:
magma_dev=# \c magma_dev

```


### NMS Table
```docker compose exec postgres psql -U nms```


## Production Way of connections
```
kubectl exec -it postgresql-0 -- psql -U postgres <<< Password postgres
postgres=# \l
postgres=# \c magma                               <<<< Connect to Magma
You are now connected to database "magma" as user "postgres".
magma=#
```
