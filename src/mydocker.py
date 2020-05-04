import docker, shutil
import random
import os, traceback
from src.config2 import tar_file, un_tar, dockerfile_built_only_image

#获取所有镜像，包括中间层
def getAll_images_list(client = docker.from_env()):
    try:
        images = client.images.list(all=True)
    except:
        return []
    else:
        return images
    finally:
        client.close()

def clear_none_image(client = docker.from_env()):
    try:
        images = client.images.list()
    except:
        return {}
    else:
        for image in images:
            if image.attrs['RepoTags'] == []:
                exit_flag = False
                while exit_flag == False:
                    try:
                        containers = client.containers.list(all = True)
                        client.images.remove(image.id)
                        exit_flag = True
                    except Exception as err:
                        print('clear_none_image : ', err)
                        err = str(err)
                        for container in containers:
                            if container.short_id == err[len(err) - 14: len(err) - 4]:
                                container.remove(v = True, force = True)
                                break
    finally:
        client.close()

#获取所有镜像，不包括中间层
def get_images_list(client = docker.from_env()):
    clear_none_image()
    dict_images = dict()
    try:
        images = client.images.list()
    except:
        return {}
    else:
        for image in images:
            if image.attrs['RepoTags'] != [] and image.attrs['RepoTags'][0] != None:
                dict_images[image.attrs['RepoTags'][0]] = image
    client.close()
    return dict_images

#获取所有容器内容
def getAll_containers_list(client = docker.from_env()):      
    dict_containers = dict()
    try:
        containers = client.containers.list(all = True)
    except:
        return {}
    else:
        for container in containers:
            dict_containers[container.name] = container
    client.close()
    return dict_containers

#获取所有容器
def get_containers_list(client = docker.from_env()):      
    dict_containers = dict()
    try:
        containers = client.containers.list(all = True)
    except:
        return {}
    else:
        for container in containers:
            dict_containers[container.name] = [container.short_id, container.id]
    client.close()
    return dict_containers


class my_docker:
    #类成员初始化
    def __init__(self, pluginname = '', main_config = None, filecode = '', images  = True, containers = True, plugin_config = None):
        self.filecode = filecode                                                                               #文件码
        self.pluginname = pluginname                                                              #接口名称
        self.main_config = main_config                                                                                      #接口配置信息       
        self.run_log = list()                                                                                      #执行日志                                               
        self.client = docker.from_env()                                                             #与docker守护进程交互的客户机
        if plugin_config != None:
            self.plugin_config = plugin_config
        if images  == True:
            self.image = self.get_client_images()                                                #属于该接口的镜像
        if containers == True:
            self.containers = self.get_client_containers()                                #该接口的容器列表
    
    def __delattr__(self):
        self.client.close()

    #获取所有镜像
    def get_images_lists(self):
        dict_images = dict()
        try:
            images = self.client.images.list()
        except:
            return {}
        else:
            for image in images:
                if image.attrs['RepoTags'] != [] and image.attrs['RepoTags'][0] != None:
                    dict_images[image.attrs['RepoTags'][0]] = image
        return dict_images

    #获取所有容器
    def get_containers_lists(self):      
        dict_containers = dict()
        try:
            containers = self.client.containers.list(all = True)
        except:
            return {}
        else:
            for container in containers:
                dict_containers[container] = [container.short_id, container.id]
        return dict_containers

    def containers_stop(self, container):
        container.stop()

    def containers_pause(self, container):
        container.pause()

    #获取该接口的镜像
    def get_client_images(self):
        try:
            images = self.client.images.list()
        except:
            return None
        else:
            for image in images:
                if image.attrs['RepoTags'] != [] and image.attrs['RepoTags'][0].split(':')[0] == self.pluginname:
                    return image
                elif image.attrs['RepoTags'] == []:
                    self.image_remove(image.id)
            #该接口没有镜像创建新镜像
            temp = self.image_build()
            return temp

    #创建镜像
    def image_build(self):
        #创建并返回该镜像
        old_path = os.getcwd()
        try:
            image = self.client.images.build(path = self.main_config['MoudlesPath'][0] + self.pluginname, 
                                                                                tag = self.pluginname + ':' + self.main_config['ImageTag'][0], nocache = True)
        except Exception as err:
            print('image_build: ', err)
            clear_none_image()
        else:
            # self.clear_none_image_container()
            image = image[0]
            return image
        finally:
            self.clear_test_container()
    
    def image_remove(self, image):
        containers = self.client.containers.list(all = True)
        exit_flag = False
        while exit_flag == False:
            try:
                self.client.images.remove(image, noprune = True)
                exit_flag = True
            except Exception as err:
                err = str(err)
                for container in containers:
                    if container.short_id == err[len(err) - 14: len(err) - 4]:
                        container.remove(v = True, force = True)
                        break

    def clear_test_container(self):
        containers = getAll_containers_list()
        for container in containers:
            try:
                containers[container].attrs['Config']['Healthcheck']
            except:
                pass
            else:
                containers[container].remove(v = True, force = True)
    
    # def clear_none_image_container(self):
    #     containers = getAll_containers_list()
    #     for container in containers:
    #         if containers[container].attrs['Image'][7:20] == None : 
    #             containers[container].remove(v = True, force = True)

    #获取该接口的所有工作容器
    def get_client_containers(self):
        temp_list = []              #存放该接口容器的临时列表
        try:
            containers = self.client.containers.list(all=True)
        except:
            pass
        else:
            for container in containers:
                if container.name[0:len(self.pluginname)] == self.pluginname:
                    temp_list.append(container)
        #该接口拥有工作容器数量少于默认数量则创建新容器
        for ran in range(int(self.main_config['InitPluginContainerNumber'][0]) - len(temp_list)):
            container_name = self.pluginname + '_' + ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 10))           #新容器名称
            container_t = self.container_ceate(container_name)                      #创建新容器
            if container_t != None:                                                         #创建容器成功
                temp_list.append(container_t)
            else:                                                                                              #创建容器失败
                ran -= 1
        #返回
        return temp_list

#创建容器
    def container_ceate(self, container_name):
        if self.image != None:
            try:
                con =  self.client.containers.run(self.image, 
                                                                                    name = container_name, 
                                                                                    command = self.main_config['ContainerSchemaTest'][0], 
                                                                                    detach=True)
            except Exception as err:
                print('container_ceate: ', err)
                return None
            else:
                con.pause()
                return con

    #从仓库中获取镜像
    def image_pull(self, basic_image):
        try:
            self.run_log.append('开始从Docker Hub拉取基础镜像' + basic_image +' ... ')
            self.client.images.pull(basic_image)
        except Exception as err:
            self.run_log.append('基础镜像拉取失败，可能原因如下 ： ')
            self.run_log.append('[1] 基础镜像' + basic_image + '不存在 ... ')
            self.run_log.append('[2] 网站服务器与Docker Hub服务器链接失败 ... ')
        else:
            self.run_log.append('基础镜像拉取成功 ... ')
    
    def basic_image_build(self, basic_image, new_image, sources, install_content):
        images = self.get_images_lists()
        try:
            self.run_log.append('新镜像名检测中 ... ')
            images[new_image + ':' + self.main_config['BasicImageTag'][0]]
        except Exception as err:
            if new_image == '' or new_image == None:
                self.run_log.append('新镜像名为空, 建立中止 ... ')
                return
            self.run_log.append('新镜像名' + new_image + ':' + self.main_config['BasicImageTag'][0] + '可使用 ... ')
            try:
                self.run_log.append('基础镜像检测中 ... ')
                images[basic_image]
            except Exception as err2:
                self.run_log.append('基础镜像不存在 ... ')
                self.image_pull(basic_image)
            else:
                 self.run_log.append('检测到基础镜像 ... ')
        else:
            self.run_log.append('新镜像名已被使用 ... ')
            return
        if not os.path.isdir(self.main_config['ImagesPath'][0] + new_image):
            os.makedirs(self.main_config['ImagesPath'][0] + new_image)
        try:
            shutil.copyfile(self.main_config['SourcesPath'][0] + sources + '/sources.list', self.main_config['ImagesPath'][0] + new_image + '/sources.list')
        except Exception as err:
            self.run_log.append('软件源复制失败:  '+ str(err))
            return
        else:
            self.run_log.append('软件源复制成功... ')
        with open(self.main_config['ImagesPath'][0] + new_image + '/Dockerfile', 'w+') as f:
            f.truncate()
            f.write(dockerfile_built_only_image(self.main_config, new_image, basic_image, install_content, sources))
        self.run_log.append('开始构建新镜像 ... ')
        try:
            self.client.images.build(path = self.main_config['ImagesPath'][0] + new_image, tag =new_image + ':' + self.main_config['BasicImageTag'][0] , nocache = True)
        except Exception as err:
            print(err)
            self.clear_test_container()
            self.run_log.append('构建失败: ' + str(err))
        else:
            self.run_log.append('构建新镜像成功 ... ')
        finally:
            self.clear_test_container()


    #启动容器
    def containers_start(self):
        t_container = None
        for container in self.containers:
            container.reload()
            if container.status == 'exited':
                t_container = container
                break
            elif container.status == 'paused':
                t_container = container
                break
        if t_container == None:
            container_name =  self.pluginname + '_' + ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 10))           #新容器名称
            t_container = self.container_ceate(container_name)
            self.containers.append(t_container)
        if t_container.status == 'exited':
            t_container.start()
        elif t_container.status == 'paused':
            t_container.unpause()
        t_container.reload()
        self.container_exec_run(t_container)

    def container_put_archive(self, container):
        container.exec_run('mkdir data', workdir = self.plugin_config['pluginrootpath'][0])
        container.exec_run('mkdir result', workdir = self.plugin_config['pluginrootpath'][0])
        tar_file(self.main_config['ContainerTarName'][0], self.filecode, self.pluginname)
        s_path = self.main_config['SDFilePath'][0] + self.pluginname + '/' + self.filecode + '/' + self.main_config['ContainerTarName'][0]
        d_path = self.main_config['ContainerSrcPath'][0]
        with open(s_path, 'rb') as f:
            datas = f.read()
            container.put_archive(d_path, datas)
        if os.path.isfile(s_path):
            os.remove(s_path)

    def container_get_archive(self, container):
        path = self.main_config['SDFilePath'][0]+ self.pluginname + '/' + self.filecode + '/result/'
        s_path = self.main_config['ContainerRelPath'][0]
        d_path = path+ self.main_config['ContainerRTarName'][0]
        if not os.path.isdir(path):
            os.makedirs(path)
        with open(d_path, 'wb') as f:
            bits, stat = container.get_archive(s_path)
            for bit in bits:
                f.write(bit)
        if os.path.isfile(d_path):
            un_tar(d_path, self.main_config['SDFilePath'][0]+ self.pluginname + '/' + self.filecode)
            os.remove(d_path)

    #移除容器
    def container_remove(self, status):
        for container in self.client.containers.list(all = True):
            if container.status == status:
                container.remove()

    def container_exec_run(self,  container):
        self.container_put_archive(container)
        try:
            print(container.exec_run(self.plugin_config['runcommand'][0], workdir = self.plugin_config['pluginrootpath'][0], demux = True))
            if self.pluginname == 'tedt1':
                input()
        except Exception as err:
            print('container_ceate: ', err)
        else:
            self.container_get_archive(container)
            container.exec_run('rm -rf data/', workdir = self.plugin_config['pluginrootpath'][0])
            container.exec_run('rm -rf result/', workdir = self.plugin_config['pluginrootpath'][0])
            self.containers_pause(container)
