sudo docker container stop $(sudo docker container ls -aq)
sudo docker container rm $(sudo docker container ls -aq)
sudo docker container prune
sudo docker image prune -a
sudo docker volume prune
sudo docker system prune -a
sudo docker system prune
