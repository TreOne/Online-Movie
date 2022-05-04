#!/usr/bin/env bash

docker-compose exec mongocfg1 sh -c "mongosh <  /scripts/config_server.js"
docker-compose exec mongors1n1 sh -c "mongosh < /scripts/shard_1.js"
docker-compose exec mongors2n1 sh -c "mongosh  < /scripts/shard_2.js"
docker-compose exec mongos1 sh -c "mongosh < /scripts/router.js"
docker-compose exec mongos1 sh -c "mongosh < /scripts/init_db.js"
