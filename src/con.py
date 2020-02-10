import os
import zipfile, tarfile
from src.mydocker import get_images_list

def configurations():
        return """
                        images = bmp,jpg,png,tif,gif,pcx,tga,exif,fpx,svg,psd,cdr,pcd,dxf,ufo,eps,ai,raw,WMF,webp
                        text = txt, c, cpp, html, py
                        world = world
                        excel = xls,xlsw

                        codestr = ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
                        filecode_length = 16
                        file_path = ./static/file/
                        moudles_path = ./moudles/
                        sources_path = ./sources/

                        image_tag = plugin
                        init_plugin_container_number = 3
                        container_src_path = /home/plugin/data/
                        container_rel_path = /home/plugin/result/
                        container_tar_name = data.tar.gz
                        container_rtar_name = result.tar.gz
                        container_schema_run = /bin/bash
                        container_schema_test = /bin/sh -c "while true;do echo hello;sleep 1;done"
                """

#判断变量是否存在列表中
def isexit(var, templist):
        for con_temp in templist:
                if var == con_temp:
                        return 1
        return 0

#读取接口配置文件
def read_obiect_config(mouname, main_condist):
        flag = -1
        empty_dict = dict()
        obj_name = ''
        obj_list = list()
        with open(main_condist['moudles_path'][0]+mouname+'/.Config', 'r') as cons:
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
def readlist(main_condist):
        moulists = dict()
        with open(main_condist['moudles_path'][0] + 'list', 'r') as fo:
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
        main_condist = main_con()
        list_sources = list()
        if os.path.isdir(main_condist['sources_path'][0]):
                for dirs in os.listdir(main_condist['sources_path'][0]):
                        if os.path.isfile(main_condist['sources_path'][0] + dirs + '/sources.list'):
                                t  = (dirs, dirs)
                                list_sources.append(t)
        list_sources.sort()
        return list_sources

#获取软件源：
def get_sources():
        main_condist = main_con()
        list_sources = list()
        if os.path.isdir(main_condist['sources_path'][0]):
                for dirs in os.listdir(main_condist['sources_path'][0]):
                        if os.path.isfile(main_condist['sources_path'][0] + dirs + '/sources.list'):
                                list_sources.append(dirs)
        list_sources.sort()
        return list_sources

def dict_sort(temp_dict):
        pass