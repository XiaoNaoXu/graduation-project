from src.mydocker import getAll_containers_list

def containers_list(main_condict):
    containers = getAll_containers_list()
    container_dict = dict()
    for container in containers:
        container_dict[container] = dict()
        container_attrs = containers[container].attrs
        container_dict[container]['id'] = containers[container].short_id
        container_dict[container]['status'] = container_attrs['State']['Status']
        container_dict[container]['pname'] = container.split('_')[0] + ':' + main_condict['image_tag'][0]
        container_dict[container]['pid'] = container_attrs['Image'][7:20]
        container_dict[container]['created'] =  container_attrs['Created']
        container_dict[container]['laststart'] =  container_attrs['State']['StartedAt']
    return container_dict

def container_add():
    pass

def container_delete(plugin):
    containers = getAll_containers_list()
    for container in containers:
        if plugin == container:
            containers[container].remove(v = True, force = True)

def container_pause():
    pass

def container_unpause():
    pass

def container_start():
    pass

def container_stop():
    pass