import docker
from docker.errors import APIError, ImageNotFound

# Don't judge me, I don't have time to do a better code right now
cli = docker.DockerClient(base_url='unix://var/run/docker.sock', version='auto')


def drop_container(container):
    print("Removing container:{} with ID:{}".format(container.name, container.id[0:10]))
    try:
        return container.remove(force=True)
    except APIError, e:
        print("Could not remove container:{}".format(container))
        print(e.message)


def clean_dangling_containers():
    """
    Cleaning all containers with status exited
    :return:
    """
    print("Cleaning dangling containers...")
    containers = cli.containers.list(filters={'status': 'exited'})
    for container in containers:
        drop_container(container)


def clean_dangling_images():
    """
    Clean all images that are not used
    :return:
    """
    print("Cleaning dangling images...")
    images = cli.images.list(filters={'dangling': 'true'})
    for image in images:
        print("Removing image:{}".format(image.id[7:19]))
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
    print("Cleaning tags for image {}".format(image_name))
    images = order_images_by_date(cli.images.list(name=image_name))[keep::]
    for image in images:
        print("Removing {} with image tag:{} and ID:{}".format(image_name, image.tags[0], image.id[7:19]))
        remove_image(image.id)


def remove_image(image_id):
    try:
        cli.images.remove(image=image_id)
    except ImageNotFound:
        # I don't care
        pass


def main(images):
    for image in images.split(','):
        clean_old_tags(image)
    clean_dangling_containers()
    clean_dangling_images()
