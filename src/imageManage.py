import os
from src.mydocker import get_images_list, getAll_images_list, my_docker
from src.con import localfile_delete, main_con
from subprocess import check_call, check_output

def pimageid_to_pimagename(images, parent_imageId):
    for image in images:
        if parent_imageId == image.id:
            if image.attrs['Parent'] == '' or image.attrs['RepoTags'] != []:
                return image.attrs['RepoTags']
            elif image.attrs['Parent'] != '':
                return pimageid_to_pimagename(images, image.attrs['Parent'])
                

def image_list():
    main_condict = main_con()
    images_list = dict()
    images = get_images_list()
    for image in images:
        image = images[image]
        name = image.attrs['RepoTags'][0]
        images_list[name] = dict()
        images_list[name]['Id'] = image.attrs['Id'][7:19]
        if image.attrs['Parent'] != '':
            images_list[name]['parentName'] = pimageid_to_pimagename(getAll_images_list(), image.attrs['Parent'])
        else:
            images_list[name]['parentName'] = None
        try:
            images_list[name]['Labels'] = image.attrs['ContainerConfig']['Labels']['maintainer']
        except:
            images_list[name]['Labels'] = None
        images_list[name]['User'] = image.attrs['Config']['User']

        if main_condict['ImageTag'][0] in name.split(':')[1]:
            images_list[name]['imagetype'] = '衍生镜像'
        else:
            images_list[name]['imagetype'] = '基础镜像'
        images_list[name]['Size'] = image.attrs['Size']
        images_list[name]['Created'] = image.attrs['Created']
        images_list[name]['Architecture'] = image.attrs['Os'] + '-' + image.attrs['Architecture']
    return images_list

def image_backup(image_name):
    main_condict = main_con()
    images = get_images_list()
    backup_url = 'docker login -u=' + main_condict['HubUser'][0] + ' -p=' + main_condict['HubPasswd'][0] + ' ' + main_condict['HubUrl'][0]
    for key in images:
        if key == image_name:
            check_output(backup_url, shell = True)
            changed_name = 'docker tag ' + images[key].id[7:19] + ' ' + main_condict['HubUrl'][0] + '/' \
                + main_condict['HubRepository'][0] + '/' + key
            check_output(changed_name, shell=True)
            push_url = 'docker push ' + main_condict['HubUrl'][0] + '/' \
                + main_condict['HubRepository'][0] + '/' + key
            check_output(push_url, shell=True)
            rmi_url = 'docker rmi ' + main_condict['HubUrl'][0] + '/' \
                + main_condict['HubRepository'][0] + '/' + key
            check_output(rmi_url, shell=True)


def image_delete(image):
    main_condict = main_con()
    images = get_images_list()
    for key in images:
        if key == image:
            docker_temp = my_docker('--no-plugin', '--no-config', filecode='--no-filecode', images = False, containers = False)
            docker_temp.image_remove(images[key].id)
            localfile_delete(image, main_condict['ImagesPath'][0])
