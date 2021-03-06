#!/usr/bin/env python
import os
import time
import docker
from docker.errors import APIError, ImageNotFound

# Don't judge me, I don't have time to do a better code right now
cli = docker.DockerClient(base_url='unix://var/run/docker.sock', version='auto')
CONFIG = {}

def drop_container(container):
    """
    Drop containers with exit status
    """
    print "Removing container:{} with ID:{}".format(container.name, container.id[0:10])
    try:
        return container.remove(force=True)
    except APIError, e:
        print "Could not remove container:{}".format(container)
        print e.message


def clean_dangling_containers():
    """
    Cleaning all containers with status exited
    :return:
    """
    print "Cleaning dangling containers..."
    containers = cli.containers.list(filters={'status': 'exited'})
    for container in containers:
        drop_container(container)


def clean_dangling_images():
    """
    Clean all images that are not used
    :return:
    """
    print "Cleaning dangling images..."
    images = cli.images.list(filters={'dangling': 'true'})
    for image in images:
        print "Removing image:{}".format(image.id[7:19])
        cli.images.remove(image=image.id, force=True)


def order_images_by_date(images):
    """
    Sort image list by date
    :param images:
    :return:
    """
    return sorted(images, key=lambda img: img.attrs['Created'], reverse=True)


def clean_old_tags(image_name, keep=5):
    """
    Clean old tags keeping only the last 5 tags
    :param image_name: name of the docker image
    :param keep: Amount to keep
    :return:
    """
    print "Cleaning tags for image {}".format(image_name)
    images = order_images_by_date(cli.images.list(name=image_name))
    if len(images) > keep:
        images = images[keep::]

        for image in images:
            print "Removing {} with image tag:{} and ID:{}".format(image_name, image.tags[0], image.id[7:19])
            remove_image(image.id)


def remove_image(image_id):
    """
    Remove the docker image from Docker host
    :param image_id: ID of the image
    """
    try:
        cli.images.remove(image=image_id)
    except ImageNotFound:
        # I don't care
        pass

def configure():
    """"
    Configure the Docker Cleaner with the Environment
    variables
    """
    CONFIG['WAKEUP_TIME'] = os.getenv('WAKEUP_TIME', 30)
    CONFIG['DELETE_IMAGES'] = os.getenv('DELETE_IMAGES', None)
    CONFIG['KEEP_AMOUNT'] = os.getenv('KEEP_AMOUNT', 5)


def main():
    """
    Entrypoint for the execution
    """
    configure()
    while True:
        print "Executing Docker Cleaner...\n"
        images = CONFIG['DELETE_IMAGES']
        if images:
            for image in images.split(','):
                clean_old_tags(image, keep=CONFIG['KEEP_AMOUNT'])

        clean_dangling_containers()
        clean_dangling_images()
        time.sleep(float(CONFIG['WAKEUP_TIME'])*60)


if __name__ == '__main__':
    main()
