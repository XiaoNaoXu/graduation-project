import os
from src.mydocker import get_images_list, getAll_images_list, my_docker

def pimageid_to_pimagename(images, parent_imageId):
    if parent_imageId != None:
        for image in images:
            if parent_imageId == image.id:
                if image.attrs['Parent'] != '':
                    return pimageid_to_pimagename(images, image.attrs['Parent'])
                elif image.attrs['Parent'] == '':
                    if image.attrs['RepoTags'] != []:
                        return image.attrs['RepoTags'][0]
                    else:
                        return []

def image_list():
    images_list = dict()
    images = get_images_list()
    for image in images:
        image = images[image]
        name = image.attrs['RepoTags'][0]
        images_list[name] = dict()
        images_list[name]['Id'] = image.attrs['Id'][7:19]
        images_list[name]['parentName'] = pimageid_to_pimagename(getAll_images_list(), image.attrs['Parent'])
        try:
            images_list[name]['Labels'] = image.attrs['ContainerConfig']['Labels']['maintainer']
        except:
            images_list[name]['Labels'] = None
        images_list[name]['User'] = image.attrs['Config']['User']
        if name[len(name) - 6:len(name)] == 'plugin':
            images_list[name]['Os'] = '衍生镜像'
        else:
            images_list[name]['Os'] = '基础镜像'
        images_list[name]['Size'] = image.attrs['Size']
        images_list[name]['Created'] = image.attrs['Created']
        images_list[name]['Architecture'] = image.attrs['Os'] + '-' + image.attrs['Architecture']
    return images_list

def image_add():
    pass

def image_delete(image):
    images = get_images_list()
    for key in images:
        if key == image:
            docker_temp = my_docker('--no-plugin', '--no-config', filecode='--no-filecode', images = False, containers = False)
            docker_temp.image_remove(images[key].id)