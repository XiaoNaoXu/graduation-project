import os
import zipfile, tarfile
from src.mydocker import get_images_list

def configurations():
        return """
                        images = bmp,jpg,png,tif,gif,pcx,tga,exif,fpx,svg,psd,cdr,pcd,dxf,ufo,eps,ai,raw,WMF,webp
                        text = txt, c, cpp, html, py
                        world = world
                        excel = xls,xlsw

                        CodeStr = ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
                        FileCodeLength = 16
                        SDFilePath = ./static/file/
                        MoudlesPath = ./moudles/
                        SourcesPath = ./sources/

                        ImageTag = plugin
                        InitPluginContainerNumber = 3
                        ContainerSrcPath = /home/plugin/data/
                        ContainerRelPath = /home/plugin/result/
                        ContainerTarName = data.tar.gz
                        ContainerRTarName = result.tar.gz
                        ContainerSchemaRun = /bin/bash
                        ContainerSchemaTest = /bin/sh -c "while true;do echo hello;sleep 1;done"
                """

#判断变量是否存在列表中
def isexit(var, templist):
        for con_temp in templist:
                if var == con_temp:
                        return 1
        return 0

def list_clear(plugin, main_condict):
        temp = list()
        moulists = readlist(main_condict)
        for key in list(moulists.keys()):
                for mou in moulists[key]:
                        if plugin == mou:
                                moulists[key].remove(plugin)
                                break
                if moulists[key] == []:
                        moulists.pop(key)
                else:
                        temp.append('[' + key + ']\n')
                        for mou in moulists[key]:
                                temp.append('    ' + mou + '\n')
        with open(main_condict['MoudlesPath'][0] + 'list', 'w+') as f:
                f.truncate()
                f.writelines(temp)

def localfile_delete(filename, path):
        if os.path.isdir(path + filename):
                for files in os .listdir(path + filename):
                        localfile_delete(files, path + filename + '/')
                try:
                        os.rmdir(path + filename)
                except Exception as err:
                        print('localfile_delete: ', err)
        elif os.path.isfile(path + filename):
                try:
                        os.remove(path + filename)
                except Exception as err:
                        print('localfile_delete: ', err)
        else:
                return


#读取接口配置文件
def read_obiect_config(mouname, main_condict):
        flag = -1
        empty_dict = dict()
        obj_name = ''
        obj_list = list()
        try:
                cons = open(main_condict['MoudlesPath'][0]+mouname+'/.Config', 'r')
        except:
                list_clear(mouname, main_condict)
                localfile_delete(mouname, main_condict['SDFilePath'][0])
                localfile_delete(mouname, main_condict['MoudlesPath'][0])
        else:
                for con in cons.readlines():
                        #----------------------读取接口配置-----------start
                        if con.strip() == '[arguments]' and flag == -1:
                                flag = 1
                                continue
                        if flag == 1:
                                for leng in range(len(con)):
                                        if con[leng] == '=':
                                                obj_name = con[0:leng].strip()
                                                obj_list = con[leng+1:len(con)].strip().split(',')
                                                obj_list.sort()
                                                empty_dict[obj_name] = obj_list
                        #----------------------读取接口配置-----------end

                        #----------------------读取接口详情-----------start
                        if con.strip() == '##################################' and flag  == 1:
                                flag += 1
                                empty_dict['detail'] = list()
                                continue
                        if flag == 2 and con.strip()[0] != '#':
                                empty_dict['detail'].append(con.strip() + '\n')
                        #-----------------------读取接口详情----------end
        return empty_dict

#读取接口列表
def readlist(main_condict):
        moulists = dict()
        with open(main_condict['MoudlesPath'][0] + 'list', 'r') as fo:
                for line in fo.readlines():
                        line = line.strip()
                        if line != '' and line != None:
                                if line[0] == '[':
                                        flag = line[1:len(line) - 1]
                                        moulists[flag] = list()
                                        continue
                                moulists[flag].append(line)
        for key in moulists:
                moulists[key].sort()
        return moulists

#读取框架配置参数
def main_con():
        empty_dict = dict()
        obj_name = ''
        obj_list = list()
        with open('./.Config', 'r') as cons:
                for con in cons.readlines():
                        if con.strip()[0:1] != '#':
                                for leng in range(len(con)):
                                        if con[leng] == '=':
                                                obj_name = con[0:leng].strip()
                                                obj_list = con[leng+1:len(con)].strip().split(',')
                                                empty_dict[obj_name] = obj_list
        return empty_dict

#判断格式是否存在
def type_find(ext, con_dict):
        values = list() 
        for key in con_dict:
                values = con_dict[key]
                for value in values:
                        if ext == value.strip():
                                return key

#文件压缩
def zip_file(zip_path, filecode, ztype):
        savepath = os.getcwd()
        filename = filecode + '.zip'
        if not os.path.isfile(zip_path + filename):
                my_zip = zipfile.ZipFile(zip_path + '/' + filename, ztype, zipfile.ZIP_DEFLATED)
                if os.path.isdir(zip_path + 'result/'):
                        os.chdir(zip_path + 'result/')
                        for filet in os.listdir('./'):
                                my_zip.write(filet)
                my_zip.close()
                os.chdir(savepath)
        return filename

def language_choices():
        dict_images = get_images_list()
        list_images = list()
        for key in dict_images:
                if key[len(key) - 6:len(key)] != 'plugin':
                        t = (key, key)
                        list_images.append(t)
        list_images.sort()
        return list_images

#获取软件源：
def sources_choices():
        main_condict = main_con()
        list_sources = list()
        if os.path.isdir(main_condict['SourcesPath'][0]):
                for dirs in os.listdir(main_condict['SourcesPath'][0]):
                        if os.path.isfile(main_condict['SourcesPath'][0] + dirs + '/sources.list'):
                                t  = (dirs, dirs)
                                list_sources.append(t)
        list_sources.sort()
        return list_sources

#获取软件源：
def get_sources():
        main_condict = main_con()
        list_sources = list()
        if os.path.isdir(main_condict['SourcesPath'][0]):
                for dirs in os.listdir(main_condict['SourcesPath'][0]):
                        if os.path.isfile(main_condict['SourcesPath'][0] + dirs + '/sources.list'):
                                list_sources.append(dirs)
        list_sources.sort()
        return list_sources

def dict_sort(temp_dict):
        pass

def sources_type(filepath):
    with open(filepath, 'r') as f:
        src_content = f.read().strip()
        if src_content == 'deb':
            return 'deb'
        else:
            return 'replace'

def dockerfile_built(main_condict, pluginname, image, dependon_install, sources):
        temp_str = ''
        temp_str2 = 'FROM ' + image + '\nCOPY * ' + main_condict['ContainerMoudelPath'][0]
        if dependon_install != ''  and dependon_install != None:
                temp_str = '\nRUN '
                dependon_install = dependon_install.split('\r\n')
                for run in dependon_install:
                        if run.strip() != '':
                                if temp_str == '\nRUN ':
                                        temp_str += run.strip() + ' -y \ '
                                else:
                                        temp_str += ' \n        && ' + run.strip() + ' -y \ '
                if sources_type(main_condict['SourcesPath'][0] + sources + '/sources.list') == 'deb':
                        with open(main_condict['MoudlesPath'][0] + pluginname + '/sources.list', mode='w+') as f:
                                with open(main_condict['SourcesPath'][0] + sources + '/sources.list', mode='r+') as f2:
                                        f.write(f2.read())
                        temp_str2 += '\nCOPY sources.list /etc/apt/' + '\nCOPY * ' + main_condict['ContainerMoudelPath'][0] + '\nRUN apt-get update  '                       
                else:
                        sel_sources = sources.split('-')[0] + 'SourcesReplace'
                        with open(main_condict['SourcesPath'][0] + sources + '/sources.list', mode='r+') as f2:
                                rep_content = f2.read().strip()
                                for length in range(len(main_condict[sel_sources])):
                                        if length == 0:
                                                temp_str2 += '\nRUN sed -i "s/' + main_condict[sel_sources][length].strip() +'/' + rep_content + '/g" /etc/apt/sources.list \ ' 
                                        else:
                                                temp_str2 += '\n\t&& sed -i "s/' + main_condict[sel_sources][length].strip() +'/' + rep_content + '/g" /etc/apt/sources.list \ ' 
                                temp_str2 += '\n\t&& apt-get update \ '
        return temp_str2 + temp_str