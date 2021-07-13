docker compose down
docker rmi $(docker images -f reference="mcsim*" -q)
docker compose up