Docker Host Cleaner
==================

This container will serve as a housekeeper for your Docker host. Map your `docker.sock` as a volume to make it work:

````
docker run -d --name maid \
-v /var/run/docker.sock:/var/run/docker.sock \
bernardovale/docker_cleaner
````


Configurations
==============
To customize the container use the following environment variables

##### WAKEUP_TIME
Amount of time in minutes to wait until next cleanup
Example: `WAKEUP_TIME=120` (2 hours)
Default: `WAKEUP_TIME=30`

##### DELETE_IMAGES
This container will not delete images **unless** specified in this variable, it accepts several images separated by comma.
Example: `DELETE_IMAGES=nginx,mysql`
Default: `DELETE_IMAGES=`

##### KEEP_AMOUNT
The amount of images to keep when using `DELETE_IMAGES`. It will preserve the last **KEEP_AMOUNT** of images.
Example: `KEEP_AMOUNT=10` (Keeping last 10 images)
Default: `KEEP_AMOUNT=5`


Full custom example
==========
```
 docker run -d --name maid \
-v /var/run/docker.sock:/var/run/docker.sock \
-e WAKEUP_TIME=60 \
-e KEEP_AMOUNT=10 \
-e DELETE_IMAGES=nginx,mysql \
bernardovale/docker_cleaner
```
